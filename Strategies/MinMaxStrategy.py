from typing import List, Tuple

from Card import Card
from Stack import Stack
from Strategies.Strategy import Strategy
from consts import CARDS


class MinMaxStrategy(Strategy):
    def get_played_cards(self, min_cards) -> List[Tuple[int, int]]:
        played_cards = []
        for i in range(min_cards):
            card_index, stack_index = None, None

            best_move = self.find_fix_move()
            if best_move:
                card_index, stack_index = best_move
            else:
                minimal_move = self.find_minimal_move()
                if minimal_move:
                    card_index, stack_index = minimal_move
            if card_index is not None and stack_index is not None:
                self.play_card(card_index, stack_index)
                played_cards.append((card_index, stack_index))
            else:
                raise RuntimeError("Cant do a move")
        best_move = self.find_fix_move()
        while best_move is not None:
            card_index, stack_index = best_move
            self.play_card(card_index, stack_index)
            played_cards.append((card_index, stack_index))
            best_move = self.find_fix_move()
        return played_cards

    def find_fix_move(self) -> (Card, Stack):
        for card_index, card in enumerate(self.player.cards):
            for stack_index, stack in enumerate(self.stacks):
                if stack.can_fix_stack(card):
                    return card_index, stack_index
        return None

    def find_minimal_move(self) -> (Card, Stack):
        minimal_delta = CARDS
        minimal_move = None

        for card_index, card in enumerate(self.player.cards):
            for stack_index, stack in enumerate(self.stacks):
                if stack.check_can_add_card(card):
                    if stack.is_growing_stack:
                        delta = card.number - stack.last_card.number
                    else:
                        delta = stack.last_card.number - card.number
                    if delta < minimal_delta:
                        minimal_delta = delta
                        minimal_move = card_index, stack_index
        return minimal_move
