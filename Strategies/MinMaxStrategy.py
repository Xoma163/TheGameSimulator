from typing import List, Tuple

from Card import Card
from Stack import Stack
from Strategies.Strategy import Strategy
from consts import CARDS


class MinMaxStrategy(Strategy):
    MINIMAL_WINDOW_MOVE = 4

    def get_played_cards(self, min_cards) -> List[Tuple[int, int]]:
        for i in range(min_cards):
            card_index, stack_index = None, None

            best_move = self.find_fix_move(self.player)
            if best_move:
                card_index, stack_index = best_move
            else:
                minimal_move = self.find_minimal_move(self.player)
                if minimal_move:
                    card_index, stack_index = minimal_move
            if card_index is not None and stack_index is not None:
                self.play_card(card_index, stack_index)
            else:
                raise RuntimeError("Cant do a move")
        best_move = self.find_fix_move(self.player)
        minimal_move = self.find_minimal_move(self.player, self.MINIMAL_WINDOW_MOVE)
        while best_move is not None or best_move is not None:
            if best_move is not None:
                card_index, stack_index = best_move
            else:
                card_index, stack_index = minimal_move
            self.play_card(card_index, stack_index)
            best_move = self.find_fix_move(self.player)
            minimal_move = self.find_fix_move(self.player)
        return self.played_cards

    def find_fix_move(self, player) -> (Card, Stack):
        for card_index, card in enumerate(player.cards):
            for stack_index, stack in enumerate(self.stacks):
                if stack.can_fix_stack(card):
                    return card_index, stack_index
        return None

    def find_minimal_move(self, player, minimal_delta=CARDS, ban_card_stack_index=None) -> (Card, Stack):
        if ban_card_stack_index is None:
            ban_card_stack_index = []
        minimal_move = None

        for card_index, card in enumerate(player.cards):
            for stack_index, stack in enumerate(self.stacks):
                if ban_card_stack_index and card_index == ban_card_stack_index[0] and stack_index == \
                        ban_card_stack_index[1]:
                    continue
                if stack.check_can_add_card(card):
                    if stack.is_growing_stack:
                        delta = card.number - stack.last_card.number
                    else:
                        delta = stack.last_card.number - card.number
                    if delta < minimal_delta:
                        minimal_delta = delta
                        minimal_move = card_index, stack_index
        return minimal_move
