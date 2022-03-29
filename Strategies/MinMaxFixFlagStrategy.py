from copy import copy
from typing import List, Tuple

from Flag import Flag
from Strategies.MinMaxStrategy import MinMaxStrategy


class MinMaxFixFlagStrategy(MinMaxStrategy):
    MINIMAL_WINDOW_MOVE = 4
    FLAG_DELTA = 15

    def __init__(self, game):
        super().__init__(game)

        self.temp_player_card: Tuple[int, int]

    def get_played_cards(self, min_cards) -> List[Tuple[int, int]]:
        for i in range(min_cards):
            card_index, stack_index = None, None

            best_move = self.find_fix_move(self.player)
            if best_move:
                card_index, stack_index = best_move
            else:
                flagged_stacks = self.check_flagged_stacks()
                minimal_move = self.find_minimal_move(self.player)
                if minimal_move:
                    card_index, stack_index = minimal_move
                    stack = self.stacks[stack_index]
                    flags = flagged_stacks.get(stack, None)
                    if flags:
                        if any([x[0] == Flag.HIGH_PRIORITY for x in flags]):
                            new_minimal_move = self.find_minimal_move(self.player, self.FLAG_DELTA,
                                                                      (card_index, stack_index))
                            if new_minimal_move:
                                card_index, stack_index = new_minimal_move

                        print

            if card_index is not None and stack_index is not None:
                self.play_card(card_index, stack_index)
            else:
                raise RuntimeError("Cant do a move")
        best_move = self.find_fix_move(self.player)
        while best_move is not None or best_move is not None:
            if best_move is not None:
                card_index, stack_index = best_move
                self.play_card(card_index, stack_index)
            best_move = self.find_fix_move(self.player)
        return self.played_cards

    def check_flagged_stacks(self):
        flagged_stacks = {}
        for stack in self.stacks:
            if stack.flags:
                flagged_stacks[stack] = stack.flags
        return flagged_stacks

    def play_card(self, card_index, stack_index):
        super().play_card(card_index, stack_index)
        self.check_someone_wanna_play_card()

    def check_someone_wanna_play_card(self):
        other_players = copy(self.game.players)
        other_players.remove(self.game.active_player)

        for player in other_players:
            fix_move = self.find_fix_move(player)
            if fix_move is not None:
                card_index, stack_index = fix_move
                flag = Flag.HIGH_PRIORITY
                self.stacks[stack_index].add_flag(flag, player)
                self.game.stacks[stack_index].add_flag(flag, player)

        for player in other_players:
            fix_move = self.find_minimal_move(player, self.MINIMAL_WINDOW_MOVE)
            if fix_move is not None:
                card_index, stack_index = fix_move
                flag = Flag.MEDIUM_PRIORITY
                self.stacks[stack_index].add_flag(flag, player)
                self.game.stacks[stack_index].add_flag(flag, player)

        for player in other_players:
            fix_move = self.find_minimal_move(player, self.MINIMAL_WINDOW_MOVE * 2)
            if fix_move is not None:
                card_index, stack_index = fix_move
                flag = Flag.LOW_PRIORITY
                self.stacks[stack_index].add_flag(flag, player)
                self.game.stacks[stack_index].add_flag(flag, player)
