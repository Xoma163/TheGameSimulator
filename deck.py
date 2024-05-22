import random
from collections import deque

from card import Card
from settings import MAX_CARD_VALUE, MIN_CARD_VALUE


class Deck:
    """
    Колода
    """

    def __init__(
            self,
            min_val: int | None = None,
            max_val: int | None = None
    ):
        """
        Инициализация колоды карт

        :param min_val: минимальная карта в колоде
        :param max_val: максимальная карта в колоде
        """
        if not min_val:
            min_val = MIN_CARD_VALUE
        if not max_val:
            max_val = MAX_CARD_VALUE

        if min_val > max_val:
            raise ValueError("Минимальная карта в колоде больше максимальной карты")

        cards = [Card(x) for x in range(min_val, max_val + 1)]
        random.shuffle(cards)
        self._cards: deque = deque(cards)

    def pop(self, n=1) -> list[Card]:
        if n < 1:
            raise ValueError("n должен быть больше или равен 1")

        cards = []
        for i in range(n):
            cards.append(self._cards.pop())
        return cards

    @property
    def can_get_card(self) -> bool:
        return len(self._cards) > 0

    def __str__(self) -> str:
        return str(self._cards)

    def __repr__(self):
        return self.__str__()

    def __len__(self) -> int:
        return len(self._cards)
