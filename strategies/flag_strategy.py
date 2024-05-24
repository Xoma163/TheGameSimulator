import logging
from enum import Enum

from deck import Deck
from player import Player
from stack import Stack, Stacks
from strategies.min_max_strategy import MinMaxStrategy
from strategies.strategy import Strategy, StrategyStep

logger = logging.getLogger()


class FlagPriority(Enum):
    CRITICAL = 100
    HIGH = 15
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

    def add(self, flag: Flag):
        self._flags.append(flag)

    def pop(self):
        pass


# 54.3% winrate
class FlagStrategy(Strategy):
    name = "Флаг стратегия"

    def __init__(self, *args, **kwargs):
        self.min_max_strategy: MinMaxStrategy = MinMaxStrategy(*args, **kwargs)
        self.flags: Flags = Flags()
        super().__init__(*args, **kwargs)

    def set_deck(self, deck: Deck):
        self.deck = deck
        self.min_max_strategy.deck = deck

    def pre_player_step(self):
        # remove flags
        if not self.flags:
            return
        player = self.players.current_player
        self.flags.remove_player_flags(player)
        logger.debug(f"Удалил флаги игрока {player}, так как его ход")

    def get_next_player_step(self) -> StrategyStep | None:
        logger.debug(f"Текущие флаги: {self.flags}")

        strategy_step = self.get_next_step()
        if strategy_step:
            logger.debug(f"Произведён ход по FlagStrategy")
            return strategy_step

        strategy_step = self.get_default_step()
        logger.debug(f"Произведён ход по MinMaxStrategy")
        return strategy_step

    def get_next_step(self) -> StrategyStep | None:
        player = self.players.current_player

        strategy_step = None
        if len(self.flags):
            blocked_stacks = [x.stack for x in self.flags]
            new_stacks_list = [stack for stack in self.stacks if stack not in blocked_stacks]
            new_stacks = Stacks(*new_stacks_list)
            strategy_step = self.min_max_strategy.get_next_step(player.cards, new_stacks)
            if strategy_step:
                wanna_more_steps = self.min_max_strategy.wanna_next_step(new_stacks, strategy_step)
                strategy_step.wanna_more_steps = wanna_more_steps
        return strategy_step

    def post_cards_draw(self):
        # Установка флагов
        for player in self.players:
            for stack in self.stacks:
                for card in player.cards:
                    if not stack.can_be_fixed(card):
                        continue
                    flag = Flag(stack, player, FlagPriority.CRITICAL)
                    if flag not in self.flags:
                        self.flags.add(flag)
                        logger.debug(
                            f"Установлен флаг игроком {player}. Карта {card} в стопку {stack.name} ({stack.last_card})")

    def get_default_step(self) -> StrategyStep | None:
        cards = self.players.current_player.cards
        stacks = self.stacks
        strategy_step = self.min_max_strategy.get_next_step(cards, stacks)
        if strategy_step:
            wanna_more_steps = self.min_max_strategy.wanna_next_step(stacks, strategy_step)
            strategy_step.wanna_more_steps = wanna_more_steps
        return strategy_step
