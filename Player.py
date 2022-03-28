from typing import List

from Card import Card


class Player:
    def __init__(self):
        self.cards: List[Card] = []

    def __str__(self):
        return " ".join([str(x) for x in self.cards])

    def add_card(self, card):
        self.cards.append(card)

    def play_card(self, card):
        self.cards.remove(card)
