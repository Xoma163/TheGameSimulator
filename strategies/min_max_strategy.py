from copy import copy

from card import Card
from settings import MAX_CARD_VALUE
from stack import Stacks
from strategies.strategy import Strategy, StrategyStep


# 31.95% winrate
class MinMaxStrategy(Strategy):
    name = "MinMax стратегия"

    MAX_DIFF_NEXT_STEP = 4
    MAX_DIFF_NEXT_STEP_NO_DECK = 11

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_player_step(self) -> StrategyStep | None:
        player = self.players.current_player

        # Получаем желаемый шаг
        strategy_step = self.get_next_step(player.cards, self.stacks)

        # Если нет никакого шага - возвращаем None
        if not strategy_step:
            return strategy_step

        # Пробуем проставить следующий шаг
        strategy_step.wanna_more_steps = self.wanna_next_step(self.stacks, strategy_step)

        return strategy_step

    def wanna_next_step(self, stacks: Stacks, strategy_step: StrategyStep) -> bool:
        """
        :return: параметр, отвечающий за желание сходить ещё раз
        """
        cards = copy(self.players.current_player.cards)
        cards.remove(strategy_step.card)

        next_step = self.get_next_step(cards, stacks)

        # Если в принципе нет следующего хода
        if not next_step:
            return False

        # Если карта - фикс
        if next_step.stack.can_be_fixed(next_step.card):
            return True

        max_diff = self.MAX_DIFF_NEXT_STEP_NO_DECK if len(self.deck) == 0 else self.MAX_DIFF_NEXT_STEP

        # Если карта меньше значения стопки на MAX_DIFF_NEXT_STEP
        diff = abs(next_step.stack.last_card_value - next_step.card.number)
        if diff <= max_diff:
            return True

        # Иначе нет
        return False

    @staticmethod
    def get_next_step(cards: list[Card], stacks: Stacks) -> StrategyStep | None:
        minimal_impact = MAX_CARD_VALUE
        strategy_step = None
        for card in cards:
            for stack in stacks:
                # Фикс
                if stack.can_be_fixed(card):
                    return StrategyStep(card, stack)
                # Ищем наименьший дифф
                if stack.can_put(card):
                    diff = abs(stack.last_card_value - card.number)
                    if diff < minimal_impact:
                        minimal_impact = diff
                        strategy_step = StrategyStep(card, stack)
        return strategy_step
