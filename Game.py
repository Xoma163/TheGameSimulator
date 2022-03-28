from typing import List

from Deck import Deck
from Player import Player
from Stack import Stack
from consts import PLAYERS, STACKS, MIN_PLAY_CARDS, MIN_PLAY_CARDS_EMPTY_DECK, MAX_CARDS


class Game:
    def __init__(self):
        from Strategies.MinMaxFixStrategy import MinMaxFixStrategy

        self.deck = Deck()

        up_stacks = [Stack(Stack.DIR_UP) for _ in range(STACKS // 2)]
        down_stacks = [Stack(Stack.DIR_DOWN) for _ in range(STACKS // 2)]
        self.stacks: List[Stack] = up_stacks + down_stacks

        self.players: List[Player] = [Player() for _ in range(PLAYERS)]
        self.active_player_index = 0
        self.strategy = MinMaxFixStrategy()

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

            self.strategy.refresh_data(self)
            try:
                played_cards = self.strategy.get_played_cards(cards_to_play)
            except RuntimeError:
                break
            for card_index, stack_index in played_cards:
                self.play_card(self.active_player, self.active_player.cards[card_index], self.stacks[stack_index])

            for _ in range(len(played_cards)):
                card = self.deck.get_card()
                if card:
                    self.active_player.add_card(card)

            self.pass_the_turn()

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

    @staticmethod
    def play_card(player, card, stack):
        player.play_card(card)
        stack.add_card(card)
