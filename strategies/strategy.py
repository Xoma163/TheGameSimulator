import dataclasses
from abc import ABC

from card import Card
from deck import Deck
from player import Players
from stack import Stacks, Stack


@dataclasses.dataclass
class StrategyStep:
    card: Card
    stack: Stack
    wanna_more_steps: bool = False


class Strategy(ABC):
    name = ""

    """
    Базовый класс стратегии
    """

    def __init__(self, players: Players, stacks: Stacks):
        self.players: Players = players
        self.stacks: Stacks = stacks
        self.deck: Deck | None = None

    def set_deck(self, deck: Deck):
        self.deck = deck

    def pre_player_step(self):
        """
        Действия стратегии перед ходом игрока
        """
        pass

    def get_next_player_step(self) -> StrategyStep | None:
        """
        :return: tuple
        :return Card - карта, которая будет разыграна.
        :return Stack - колода, в которую будет разыграна карта.
        :return bool - есть ли желание сходить повторно даже без необходимости.
        """

        raise NotImplementedError

    def post_player_step(self):
        """
        Действия стратегии после хода игрока, но до добора карт
        """
        pass

    def post_cards_draw(self):
        """
        Действия стратегии после добора карт игрока
        """
        pass
