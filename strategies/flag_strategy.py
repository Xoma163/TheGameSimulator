import logging
from copy import copy
from enum import Enum

from deck import Deck
from player import Player
from stack import Stack, Stacks
from strategies.min_max_strategy import MinMaxStrategy
from strategies.strategy import Strategy, StrategyStep

logger = logging.getLogger()


class FlagPriority(Enum):
    CRITICAL = 100
    HIGH = 50
    MEDIUM = 10
    LOW = 5


class Flag:
    def __init__(self, stack: Stack, player: Player, priority: FlagPriority):
        self.stack: Stack = stack
        self.player: Player = player
        self.priority: FlagPriority = priority

    @property
    def id(self) -> str:
        return f"{self.stack.name}_{self.player.name}_{self.priority}"

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other):
        return self.id == other.id


class Flags:
    def __init__(self, *flags: Flag):
        self._flags: list[Flag] = list(flags)
        self.__iter_index = 0

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self) -> Flag:
        if self.__iter_index < len(self._flags):
            flag = self._flags[self.__iter_index]
            self.__iter_index += 1
            return flag
        else:
            raise StopIteration

    def __len__(self):
        return len(self._flags)

    def __str__(self) -> str:
        return " ".join(str(flag) for flag in self._flags)

    def __repr__(self):
        return self.__str__()

    def remove_player_flags(self, player: Player):
        self._flags = [x for x in self._flags if x.player != player]

    def remove_stack_flags(self, stack: Stack):
        self._flags = [flag for flag in self._flags if flag.stack != stack]

    def add(self, flag: Flag):
        self._flags.append(flag)


# 70% winrate
class FlagStrategy(Strategy):
    FLAG_HIGH_DIFF = 5
    FLAG_MEDIUM_DIFF = 10

    IGNORE_FLAGS_DIFF = 31

    name = "Флаг стратегия"

    def __init__(self, *args, **kwargs):
        self.min_max_strategy: MinMaxStrategy = MinMaxStrategy(*args, **kwargs)
        self.flags: Flags = Flags()
        super().__init__(*args, **kwargs)

    def set_deck(self, deck: Deck):
        super().set_deck(deck)
        self.min_max_strategy.deck = deck

    def pre_player_step(self):
        """
        Действия стратегии перед ходом игрока
        """
        # remove flags
        if not self.flags:
            return
        player = self.players.current_player
        self.flags.remove_player_flags(player)
        logger.debug(f"Удалил флаги игрока {player}, так как его ход")

    def get_next_player_step(self, is_extra_step=False) -> StrategyStep | None:
        """
        Определение шага стратегии
        :return: StrategyStep
        """

        strategy_step = self.get_next_step()
        if strategy_step:
            logger.debug(f"Произведён ход по FlagStrategy")
        else:
            strategy_step = self.get_default_step()
            if strategy_step:
                self.flags.remove_stack_flags(strategy_step.stack)
                logger.debug(f"Удалил флаги стопки {strategy_step.stack}, так как сюда сделали ход")

            logger.debug(f"Произведён ход по MinMaxStrategy")
        return strategy_step

    def post_cards_draw(self):
        """
        Действия стратегии после добора карт игрока
        """
        for player in self.players:
            strategy_steps = []
            for i in range(2):
                if strategy_steps:
                    player_cards = copy(player.cards)
                    for strategy_step in strategy_steps:
                        player_cards.remove(strategy_step.card)
                else:
                    if i > 0:
                        continue
                    player_cards = player.cards

                if strategy_step := self.min_max_strategy.get_next_step(player_cards, self.stacks):
                    strategy_steps.append(strategy_step)
                    priority = None
                    if strategy_step.is_fix:
                        priority = FlagPriority.CRITICAL

                    if priority:
                        flag = Flag(strategy_step.stack, player, priority)
                        if flag not in self.flags:
                            self.flags.add(flag)
                        logger.debug(
                            f"Установлен флаг игроком {player}. "
                            f"Карта {strategy_step.card} в стопку {strategy_step.stack.name} "
                            f"({strategy_step.stack.last_card}). уровень {flag.priority}"
                        )

    def get_next_step(self) -> StrategyStep | None:
        if not self.flags:
            return None

        blocked_stacks_set = [x.stack for x in self.flags if x.priority == FlagPriority.CRITICAL]
        new_stacks_list = [stack for stack in self.stacks if stack not in blocked_stacks_set]
        new_stacks = Stacks(*new_stacks_list)
        cards = self.players.current_player.cards
        strategy_step = self.min_max_strategy.get_next_step(cards, new_stacks)

        if not strategy_step:
            return None

        if strategy_step.diff > self.IGNORE_FLAGS_DIFF:
            return None

        wanna_more_steps = self.min_max_strategy.wanna_next_step(
            self.players.current_player.cards,
            new_stacks,
            strategy_step
        )
        strategy_step.wanna_more_steps = wanna_more_steps
        return strategy_step

    def get_default_step(self) -> StrategyStep | None:
        strategy_step = self.min_max_strategy.get_next_step(self.players.current_player.cards, self.stacks)
        if strategy_step:
            strategy_step.wanna_more_steps = self.min_max_strategy.wanna_next_step(
                self.players.current_player.cards,
                self.stacks,
                strategy_step
            )
        return strategy_step
