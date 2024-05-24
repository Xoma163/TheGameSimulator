from card import Card


class Player:
    """
    Игрок
    """

    def __init__(self, name: str | None = None):
        self.name: str | None = name
        self.cards: list[Card] = []

    def set_cards(self, cards: list[Card]):
        self.cards = cards

    def add_cards(self, cards: list[Card]):
        self.cards += cards

    def play_card(self, card: Card) -> Card:
        card_index = self.cards.index(card)
        return self.cards.pop(card_index)

    @property
    def cards_count(self) -> int:
        return len(self.cards)

    @property
    def has_fix_on_hand(self) -> bool:
        for i, card_1 in enumerate(self.cards):
            if self.has_fix_for_card_abs(card_1):
                return True
        return False

    def has_fix_for_card_abs(self, card: Card) -> bool:
        for j, card_1 in enumerate(self.cards):
            if card_1 == card:
                continue
            if abs(card_1 - card) == 10:
                return True
        return False

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return self.__str__()


class Players:
    """
    Игроки
    """

    def __init__(
            self,
            *players: Player
    ):
        self._players: list[Player] = list(players)
        for i, player in enumerate(self._players):
            player.name = f"#{i + 1}"
        self._current_player_index: int = 0
        self.__iter_index: int = 0

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self) -> Player:
        if self.__iter_index < len(self._players):
            player = self._players[self.__iter_index]
            self.__iter_index += 1
            return player
        else:
            raise StopIteration

    def __getitem__(self, item) -> Player:
        return self._players[item]

    @property
    def current_player(self) -> Player:
        """
        Получение игрока чья очередь ходить
        """
        return self._players[self._current_player_index]

    def next_player(self) -> Player:
        """
        Следующий игрок
        """
        self._current_player_index += 1
        if self._current_player_index >= len(self._players):
            self._current_player_index = 0
        return self.current_player

    def __str__(self) -> str:
        return ", ".join([str(x) for x in self._players])

    def __repr__(self):
        return self.__str__()
