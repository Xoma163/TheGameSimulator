from typing import List

from Card import Card
from consts import CARDS


class Stack:
    DIR_UP = ">"
    DIR_DOWN = "<"

    def __init__(self, direction):
        if direction == self.DIR_UP:
            start_card = Card(1)
        elif direction == self.DIR_DOWN:
            start_card = Card(CARDS)
        else:
            raise RuntimeError("Unknown direction")

        self.cards: List[Card] = [start_card]
        self.direction = direction

    def __str__(self):
        return str(self.last_card)

    def add_card(self, card: Card):
        if not self.check_can_add_card(card):
            raise RuntimeError(f"Cant add card {card} to {self.direction} deck. Last card - {self.last_card}")
        self.cards.append(card)

    def check_can_add_card(self, card):
        if self.is_growing_stack:
            if card.number < self.last_card.number and not self.can_fix_stack(card):
                return False
        else:
            if card.number > self.last_card.number and not self.can_fix_stack(card):
                return False

        return True

    def can_fix_stack(self, card):
        if self.is_growing_stack:
            return self.last_card.number - card.number == 10
        else:
            return card.number - self.last_card.number == 10

    @property
    def is_growing_stack(self):
        return self.direction == self.DIR_UP

    @property
    def is_falling_stack(self):
        return self.direction == self.DIR_DOWN

    @property
    def last_card(self):
        return self.cards[-1]
