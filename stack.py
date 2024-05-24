from abc import ABC

from card import Card
from settings import MIN_CARD_VALUE, MAX_CARD_VALUE


class Stack(ABC):
    """
    Стопка
    """

    START_VALUE = None

    def __init__(self, name: str | None = None):
        self.name: str | None = name
        self._cards: list[Card] = []
        self._last_card: Card | None = None
        self._len_cards: int = 0

    def put(self, card: Card):
        if not self.can_put(card):
            self._raise_error(card)
        self._cards.append(card)
        self._len_cards += 1
        self._last_card = card

    @property
    def last_card(self) -> Card | None:
        return self._last_card

    @property
    def last_card_value(self) -> int:
        return self._last_card.number if self._last_card else self.START_VALUE

    def can_put(self, card: Card) -> bool:
        raise NotImplementedError

    def can_be_fixed(self, card: Card) -> bool:
        raise NotImplementedError

    def _raise_error(self, card: Card):
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self._last_card) if self._last_card else "None"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not self._last_card or not other._last_card:
            return None
        return self._last_card == other._last_card


class IncreaseStack(Stack):
    START_VALUE = MIN_CARD_VALUE - 1

    def can_put(self, card: Card) -> bool:
        if not self._last_card:
            return True
        return card > self._last_card or self.can_be_fixed(card)

    def can_be_fixed(self, card: Card) -> bool:
        if not self._last_card:
            return False
        return self._last_card - card == 10

    def _raise_error(self, card: Card):
        raise ValueError(
            f"Значение карты {card} должно быть больше значения верхней карты стопки {self._last_card}, либо на 10 меньше"
        )


class DecreaseStack(Stack):
    START_VALUE = MAX_CARD_VALUE + 1

    def can_put(self, card: Card) -> bool:
        if not self._last_card:
            return True
        return card < self._last_card or self.can_be_fixed(card)

    def can_be_fixed(self, card: Card) -> bool:
        if not self._last_card:
            return False
        return card - self._last_card == 10

    def _raise_error(self, card: Card):
        raise ValueError(
            f"Значение карты {card} должно быть меньше значения верхней карты стопки {self._last_card}, либо на 10 больше"
        )


class Stacks:
    def __init__(self, *stacks: Stack):
        self._stacks: list[Stack] = list(stacks)
        for i, stack in enumerate(self._stacks):
            stack.name = f"#{i + 1}"
        self.__iter_index: int = 0

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self) -> Stack:
        if self.__iter_index < len(self._stacks):
            stack = self._stacks[self.__iter_index]
            self.__iter_index += 1
            return stack
        else:
            raise StopIteration

    def __str__(self):
        return ", ".join([str(x) for x in self._stacks])

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self._stacks[item]
