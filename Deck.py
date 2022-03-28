from random import shuffle

from Card import Card
from consts import CARDS


class Deck:
    def __init__(self):
        self.cards = [Card(x) for x in range(2, CARDS)]
        shuffle(self.cards)

    def __str__(self):
        return " ".join([str(x) for x in self.cards])

    def __len__(self):
        return len(self.cards)

    def get_card(self):
        if not self.can_get_card:
            return None
        return self.cards.pop()

    @property
    def can_get_card(self):
        return len(self.cards) > 0
