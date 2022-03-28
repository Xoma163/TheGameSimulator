from typing import List

from Card import Card
from Deck import Deck
from Player import Player
from Stack import Stack
from consts import PLAYERS, STACKS, CARDS, MIN_PLAY_CARDS, MIN_PLAY_CARDS_EMPTY_DECK, MAX_CARDS, STRATEGY


class Game:
    def __init__(self):
        self.deck = Deck()

        up_stacks = [Stack(Stack.DIR_UP) for _ in range(STACKS // 2)]
        down_stacks = [Stack(Stack.DIR_DOWN) for _ in range(STACKS // 2)]
        self.stacks: List[Stack] = up_stacks + down_stacks

        self.players: List[Player] = [Player() for _ in range(PLAYERS)]
        self.active_player_index = 0

        self.strategy = STRATEGY

        # Так надо для условий, когда например по ошибке раздаётся карт больше, чем есть в колоде
        for _ in range(MAX_CARDS * len(self.players)):
            card = self.deck.get_card()
            if not card:
                break
            self.active_player.add_card(card)
            self.pass_the_turn()

    def play(self):
        while self.player_can_do_a_turn(self.active_player):
            if self.deck.can_get_card:
                cards_to_play = MIN_PLAY_CARDS
            else:
                cards_to_play = MIN_PLAY_CARDS_EMPTY_DECK

            # game logic here
            played_cards = 0
            while cards_to_play != 0:
                best_move = self.find_fix_move(self.active_player)
                if best_move:
                    card, stack = best_move
                    self.play_card(self.active_player, card, stack)
                    continue

                minimal_move = self.find_minimal_move(self.active_player)
                if minimal_move:
                    card, stack = minimal_move
                    self.play_card(self.active_player, card, stack)

                cards_to_play -= 1
                played_cards += 1

            for _ in range(played_cards):
                card = self.deck.get_card()
                if card:
                    self.active_player.add_card(card)

            self.pass_the_turn()
        # print(len(self.deck))
        # print("done")

    @property
    def active_player(self):
        return self.players[self.active_player_index]

    def player_can_do_a_turn(self, player):
        for card in player.cards:
            for stack in self.stacks:
                if stack.check_can_add_card(card):
                    return True
        return False

    def pass_the_turn(self):
        self.active_player_index += 1
        if self.active_player_index >= len(self.players):
            self.active_player_index = 0

    def find_fix_move(self, player) -> (Card, Stack):
        for card in player.cards:
            for stack in self.stacks:
                if stack.can_fix_stack(card):
                    return card, stack
        return None

    def find_minimal_move(self, player) -> (Card, Stack):
        minimal_delta = CARDS
        minimal_move = None

        for card in player.cards:
            for stack in self.stacks:
                if stack.check_can_add_card(card):
                    if stack.is_growing_stack:
                        delta = card.number - stack.last_card.number
                    else:
                        delta = stack.last_card.number - card.number
                    if delta < minimal_delta:
                        minimal_delta = delta
                        minimal_move = card, stack
        return minimal_move

    @staticmethod
    def play_card(player, card, stack):
        player.play_card(card)
        stack.add_card(card)
