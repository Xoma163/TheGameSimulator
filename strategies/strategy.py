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

    @property
    def diff(self) -> int:
        return abs(self.stack.last_card_value - self.card.number)

    @property
    def is_fix(self) -> bool:
        return self.stack.can_be_fixed(self.card)


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

    def get_next_player_step(self, is_extra_step=False) -> StrategyStep | None:
        """
        Определение шага стратегии
        :return: StrategyStep
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
