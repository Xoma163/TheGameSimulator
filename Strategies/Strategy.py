from copy import deepcopy
from typing import List, Tuple

from Game import Game
from Player import Player
from Stack import Stack


class Strategy:
    def __init__(self):
        self.player: Player = None
        self.stacks: List[Stack] = []
        self.played_cards: List[Tuple[int, int]] = []

    def refresh_data(self, game: Game):
        """
        deepcopy game занимает слишком много времени, поэтому забираем только нужное
        """
        self.player = deepcopy(game.active_player)
        self.stacks = deepcopy(game.stacks)
        self.played_cards = []

    def get_played_cards(self, min_cards) -> List[Tuple[int, int]]:
        """
        Основная логика.
        Необходимо реализовать этот метод и вернуть сыгранные карты списком, где
        - первый параметр индекс карты
        - второй параметр индекс колоды, в которую складываем карту
        """
        raise NotImplementedError

    def play_card(self, card_index, stack_index):
        """
        Имитация игры карты, чтобы спрогнозировать следующие ходы
        """
        card = self.player.cards[card_index]
        self.player.play_card(card)
        self.stacks[stack_index].add_card(card)
        self.played_cards.append((card_index, stack_index))
