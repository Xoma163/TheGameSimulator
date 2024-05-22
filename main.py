import logging
import random
import time

from player import Players, Player
from settings import PLAYERS_COUNT, GAMES_COUNT, RANDOM_SEED
from stack import Stacks, DecreaseStack, IncreaseStack
from strategies.min_max_strategy import MinMaxStrategy
from the_game import TheGame

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

random.seed(RANDOM_SEED)


def main():
    start_time = time.time()

    win_games_count = 0
    cards_count = []

    for _ in range(GAMES_COUNT):
        players = Players(*[Player(f"Игрок #{x}") for x in range(1, PLAYERS_COUNT + 1)])

        stacks = Stacks(
            IncreaseStack("Стопка #1"),
            IncreaseStack("Стопка #2"),
            DecreaseStack("Стопка #3"),
            DecreaseStack("Стопка #4")
        )
        strategy = MinMaxStrategy(players, stacks)

        the_game = TheGame(players, strategy=strategy, stacks=stacks)
        the_game.play()

        if the_game.is_win:
            win_games_count += 1
        cards_count.append(the_game.total_cards_count)

    logger.info(f"Выиграно игр - {win_games_count}/{GAMES_COUNT}")
    winrate = round(win_games_count / GAMES_COUNT * 100, 2)
    logger.info(f"Винрейт - {winrate}%")
    avg_cards_count = round(sum(cards_count) / len(cards_count), 2)
    logger.info(f"В среднем остаётся карт на руках и в колоде - {avg_cards_count}")

    end_time = time.time()
    logger.info(f"Время выполнения программы - {round(end_time - start_time, 3)} секунд")


if __name__ == "__main__":
    main()
