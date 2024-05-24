import dataclasses
import logging

from card import Card
from deck import Deck
from player import Players, Player
from settings import PLAYER_CARDS_COUNT, MIN_STEPS, MIN_STEPS_ON_EMPTY_DECK, CARDS_LEFT_COUNT_TO_WIN
from stack import Stacks, Stack
from strategies.strategy import Strategy

logger = logging.getLogger()


@dataclasses.dataclass
class TheGameReport:
    is_win: bool
    total_cards_count: int


class TheGame:
    """
    Игра
    """

    def __init__(self, players: Players, strategy: Strategy, stacks: Stacks):
        """
        :param players: игроки
        :param strategy: стратегия
        :param stacks: стопки
        """

        self.players: Players = players
        self.strategy: Strategy = strategy
        self.stacks: Stacks = stacks

        # Колода
        self.deck = Deck()
        self.strategy.set_deck(self.deck)

        for player in self.players:
            cards = self.deck.pop(PLAYER_CARDS_COUNT)
            player.set_cards(cards)

    def play_card(self, player: Player, card: Card, stack: Stack):
        """
        Розыгрыш карты.
        Положить карту в колоду
        """

        player.play_card(card)
        stack.put(card)
        logger.debug(f"Игрок \"{player}\" разыграл карту \"{card}\" в стопку \"{stack.name}\"")

        stacks = " ".join([str(x.last_card) for x in self.stacks])
        logger.debug(f"Значения стопок - \"{stacks}\"")

    def draw_cards(self, player: Player, count: int):
        """
        Добор карт
        """

        cards_to_draw = min(count, len(self.deck))
        logger.debug(f"Количество карт для добора - \"{cards_to_draw}\"")
        if cards_to_draw:
            cards = self.deck.pop(cards_to_draw)
            player.add_cards(cards)
            logger.debug(f"Игрок \"{player}\" добрал \"{cards_to_draw}\" карт")

    @property
    def total_cards_count(self) -> int:
        player_cards_count = sum([x.cards_count for x in self.players])
        deck_cards_count = len(self.deck)
        return player_cards_count + deck_cards_count

    @property
    def is_win(self) -> bool:
        return self.total_cards_count < CARDS_LEFT_COUNT_TO_WIN

    @property
    def is_lose(self) -> bool:
        return not self.is_win

    def get_report(self) -> TheGameReport:
        return TheGameReport(self.is_win, self.total_cards_count)

    def play(self):
        logger.debug("Начало новой игры")

        self._play()

        stacks = " ".join([str(x.last_card) for x in self.stacks])
        win_or_lose = "выиграна" if self.is_win else "проиграна"
        logger.debug(
            f"Игра закончена. Значения стопок - \"{stacks}\". Игра {win_or_lose}. Всего осталось карт на руках - \"{self.total_cards_count}\"")

    def _play(self):
        while True:
            # Определение количества шагов
            min_steps_count = MIN_STEPS if self.deck.can_get_card else MIN_STEPS_ON_EMPTY_DECK
            logger.debug(f"Минимальное количество шагов - {min_steps_count}")

            cards_str = " ".join([str(x) for x in sorted(self.players.current_player.cards)])
            logger.debug(f"Карты игрока \"{self.players.current_player}\" - \"{cards_str}\"")

            stacks = " ".join([str(x.last_card) for x in self.stacks])
            logger.debug(f"Значения стопок - \"{stacks}\"")

            # Действия перед ходом
            self.strategy.pre_player_step()

            # Ходы
            steps_count = 0
            wanna_more_steps = False

            while steps_count < min_steps_count or wanna_more_steps:
                is_extra_step = steps_count >= min_steps_count
                step = self.strategy.get_next_player_step(is_extra_step=is_extra_step)
                # Закончились ходы
                if not step:
                    # если ход был необязательным
                    if is_extra_step:
                        break
                    # поражение, невозможно совершить ход
                    return

                self.play_card(self.players.current_player, step.card, step.stack)
                steps_count += 1
                wanna_more_steps = step.wanna_more_steps

            # Действия после хода
            self.strategy.post_player_step()

            # Добор карт
            self.draw_cards(self.players.current_player, steps_count)

            # Действия после хода
            self.strategy.post_cards_draw()

            # Передача хода следующему игроку
            next_player = self.players.next_player()
            logger.debug(f"Передача хода игроку \"{next_player}\"")
            logger.debug(f"-----")
