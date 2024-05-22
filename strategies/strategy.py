import dataclasses

from card import Card
from player import Players
from stack import Stacks, Stack


@dataclasses.dataclass
class StrategyStep:
    card: Card
    stack: Stack
    wanna_more_steps: bool = False


class Strategy:
    """
    Базовый класс стратегии
    """

    def __init__(self, players: Players, stacks: Stacks):
        self.players: Players = players
        self.stacks: Stacks = stacks

    def get_next_player_steps(self) -> StrategyStep | None:
        """
        :return: tuple
        :return Card - карта, которая будет разыграна.
        :return Stack - колода, в которую будет разыграна карта.
        :return bool - есть ли желание сходить повторно даже без необходимости.
        """

        raise NotImplementedError
