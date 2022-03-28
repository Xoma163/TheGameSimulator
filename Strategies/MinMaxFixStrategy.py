from typing import List, Tuple

from Card import Card
from Stack import Stack
from Strategies.MinMaxStrategy import MinMaxStrategy
from consts import CARDS


class MinMaxFixStrategy(MinMaxStrategy):
    MINIMAL_WINDOW_MOVE = 4

    def get_played_cards(self, min_cards) -> List[Tuple[int, int]]:
        numbers_before_min_max = None

        while len(self.played_cards) < min_cards:
            fix_combination = self.has_fix_combination()
            if fix_combination:
                _min, _max = fix_combination
                numbers_before_min_max = sorted([x for x in self.player.cards if _min < x < _max])

            card_index, stack_index = None, None

            best_move = self.find_fix_move()
            if best_move:
                card_index, stack_index = best_move
            else:
                minimal_move = self.find_minimal_move()
                if minimal_move:
                    card_index, stack_index = minimal_move
            if card_index is not None and stack_index is not None:
                card = self.player.cards[card_index]
                stack = self.stacks[stack_index]
                if fix_combination:
                    if card in numbers_before_min_max:
                        if stack.is_falling_stack:
                            self.play_card(card_index, stack_index)
                            numbers_before_min_max.remove(card)

                            for card2 in reversed(numbers_before_min_max):
                                if card2 > fix_combination[0]:
                                    break
                                self.play_card(self.player.cards.index(card2), stack_index)
                                numbers_before_min_max.remove(card2)

                            self.play_card(self.player.cards.index(fix_combination[0]), stack_index)
                            self.play_card(self.player.cards.index(fix_combination[1]), stack_index)
                            for card2 in reversed(numbers_before_min_max):
                                self.play_card(self.player.cards.index(card2), stack_index)
                            continue
                        else:
                            self.play_card(card_index, stack_index)
                            numbers_before_min_max.remove(card)

                            for card2 in numbers_before_min_max:
                                if card2 > fix_combination[0]:
                                    break
                                self.play_card(self.player.cards.index(card2), stack_index)
                                numbers_before_min_max.remove(card2)

                            self.play_card(self.player.cards.index(fix_combination[1]), stack_index)
                            self.play_card(self.player.cards.index(fix_combination[0]), stack_index)
                            for card2 in numbers_before_min_max:
                                self.play_card(self.player.cards.index(card2), stack_index)
                            continue
                    elif card == fix_combination[0] and stack.is_falling_stack:
                        self.play_card(self.player.cards.index(fix_combination[0]), stack_index)
                        self.play_card(self.player.cards.index(fix_combination[1]), stack_index)
                        for card2 in reversed(numbers_before_min_max):
                            self.play_card(self.player.cards.index(card2), stack_index)
                        continue
                    elif card == fix_combination[1] and stack.is_growing_stack:
                        self.play_card(self.player.cards.index(fix_combination[1]), stack_index)
                        self.play_card(self.player.cards.index(fix_combination[0]), stack_index)

                        for card2 in numbers_before_min_max:
                            self.play_card(self.player.cards.index(card2), stack_index)
                        continue

                self.play_card(card_index, stack_index)
            else:
                raise RuntimeError("Cant do a move")

        best_move = self.find_fix_move()
        minimal_move = self.find_minimal_move(self.MINIMAL_WINDOW_MOVE)
        while best_move is not None or best_move is not None:
            if best_move is not None:
                card_index, stack_index = best_move
            else:
                card_index, stack_index = minimal_move
            self.play_card(card_index, stack_index)
            best_move = self.find_fix_move()
            minimal_move = self.find_fix_move()
        return self.played_cards

    def find_minimal_move(self, minimal_delta=CARDS) -> (Card, Stack):
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

    def has_fix_combination(self):
        for i, card1 in enumerate(self.player.cards):
            for j, card2 in enumerate(self.player.cards):
                if i == j:
                    continue
                if abs(card1 - card2) == 10:
                    return sorted([card1, card2])
        return False
