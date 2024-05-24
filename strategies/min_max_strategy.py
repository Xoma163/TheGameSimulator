import logging
from copy import copy, deepcopy

from card import Card
from settings import MAX_CARD_VALUE
from stack import Stacks
from strategies.strategy import Strategy, StrategyStep

logger = logging.getLogger()


# 50 % winrate
class MinMaxStrategy(Strategy):
    name = "MinMax стратегия"

    MAX_DIFF_NEXT_STEP = 4
    MAX_DIFF_NEXT_STEP_NO_DECK = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_player_step(self, is_extra_step=False) -> StrategyStep | None:
        # Получаем желаемый шаг
        strategy_step = self.get_next_step(self.players.current_player.cards, self.stacks)

        # Если нет никакого шага - возвращаем None
        if not strategy_step:
            return strategy_step

        strategy_step.wanna_more_steps = self.wanna_next_step(
            self.players.current_player.cards,
            self.stacks,
            strategy_step
        )

        return strategy_step

    def wanna_next_step(
            self, cards: list[Card],
            stacks: Stacks,
            strategy_step: StrategyStep
    ) -> bool:
        """
        :return: параметр, отвечающий за желание сходить ещё раз
        """

        # Имитация cards и stacks, якобы мы уже сходили
        if strategy_step:
            _cards = copy(cards)
            _cards.remove(strategy_step.card)
            cards = _cards

            stacks = deepcopy(stacks)
            for stack in stacks:
                if stack == strategy_step.stack:
                    stack.put(strategy_step.card)

        next_step = self.get_next_step(cards, stacks)

        # Если в принципе нет следующего хода
        if not next_step:
            return False

        # Пробуем проставить следующий шаг

        # Если карта - фикс
        if next_step.stack.can_be_fixed(next_step.card):
            logger.debug("wanna_next_step: fix")
            return True

        max_diff = self.MAX_DIFF_NEXT_STEP_NO_DECK if len(self.deck) == 0 else self.MAX_DIFF_NEXT_STEP

        # Если карта меньше значения стопки на MAX_DIFF_NEXT_STEP
        diff = abs(next_step.stack.last_card_value - next_step.card.number)
        if diff <= max_diff:
            logger.debug(f"wanna_next_step: diff={diff}, max_diff={max_diff}")

            return True

        # Иначе нет
        return False

    @staticmethod
    def get_next_step(cards: list[Card], stacks: Stacks) -> StrategyStep | None:
        minimal_impact = MAX_CARD_VALUE
        strategy_step = None
        for stack in stacks:
            for card in cards:
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
