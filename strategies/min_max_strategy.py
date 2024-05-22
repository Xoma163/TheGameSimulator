from copy import copy

from card import Card
from settings import MAX_CARD_VALUE
from stack import Stacks
from strategies.strategy import Strategy, StrategyStep


# 27.34% winrate
class MinMaxStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_player_steps(self) -> StrategyStep | None:
        player = self.players.current_player

        # if self.players.current_player.has_fix_on_hand:
        #     print

        # Отдельно проверяем есть ли фиксы

        strategy_step = self._get_next_step(player.cards, self.stacks)
        if not strategy_step:
            return strategy_step

        strategy_step.wanna_more_steps = self._wanna_next_step(player.cards, self.stacks, strategy_step)

        return strategy_step

    def _wanna_next_step(self, cards: list[Card], stacks: Stacks, strategy_step: StrategyStep):
        cards = copy(cards)
        cards.remove(strategy_step.card)

        next_step = self._get_next_step(cards, stacks)
        if not next_step:
            return False
        diff = abs(next_step.stack.last_card_value - next_step.card.number)
        if diff <= 5:
            return True

    @staticmethod
    def _get_next_step(cards: list[Card], stacks: Stacks) -> StrategyStep:
        for card in cards:
            for stack in stacks:
                if stack.can_fix(card):
                    return StrategyStep(card, stack)

        minimal_impact = MAX_CARD_VALUE
        strategy_step = None
        for card in cards:
            for stack in stacks:
                if stack.can_put(card):
                    diff = abs(stack.last_card_value - card.number)
                    if diff < minimal_impact:
                        minimal_impact = diff
                        strategy_step = StrategyStep(card, stack)
        return strategy_step
