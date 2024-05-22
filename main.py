import logging
import multiprocessing
import random
import time

import matplotlib.pyplot as plt
from tqdm import tqdm

from player import Players, Player
from settings import PLAYERS_COUNT, GAMES_COUNT, RANDOM_SEED, TOTAL_CARDS_COUNT, PROCESS_WORKERS
from stack import Stacks, DecreaseStack, IncreaseStack
from strategies.min_max_strategy import MinMaxStrategy
from the_game import TheGame

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

random.seed(RANDOM_SEED)


def play_games():
    start_time = time.time()

    with multiprocessing.Pool(processes=PROCESS_WORKERS) as pool:
        # played_games = pool.map(play_game, range(GAMES_COUNT))

        played_games = []
        for _ in tqdm(
                pool.imap_unordered(
                    play_game,
                    range(GAMES_COUNT))
                ,
                total=GAMES_COUNT,
                mininterval=1.0,
                smoothing=0.2
        ):
            played_games.append(_)

    end_time = time.time()
    logger.info(f"Время выполнения программы - {round(end_time - start_time, 3)} секунд")

    return played_games


def play_game(_):
    players_list = [Player(f"Игрок #{x}") for x in range(1, PLAYERS_COUNT + 1)]
    players = Players(*players_list)

    stacks = Stacks(
        IncreaseStack("Стопка #1"),
        IncreaseStack("Стопка #2"),
        DecreaseStack("Стопка #3"),
        DecreaseStack("Стопка #4")
    )
    strategy = MinMaxStrategy(players, stacks)

    the_game = TheGame(players, strategy=strategy, stacks=stacks)
    the_game.play()

    return the_game


def main():
    played_games = play_games()
    log_statistics(played_games)
    draw_cards_count(played_games)


def log_statistics(played_games: list[TheGame]):
    win_games_count = len([_ for _ in played_games if _.is_win])
    cards_count = [x.total_cards_count for x in played_games]

    logger.info(f"Выиграно игр - {win_games_count}/{GAMES_COUNT}")
    winrate = round(win_games_count / GAMES_COUNT * 100, 2)
    logger.info(f"Винрейт - {winrate}%")
    avg_cards_count = round(sum(cards_count) / len(cards_count), 2)
    logger.info(f"В среднем остаётся карт на руках и в колоде - {avg_cards_count}")


def draw_cards_count(played_games: list[TheGame]):
    cards_count = [x.total_cards_count for x in played_games]

    ax = plt.subplot()

    ax.hist(cards_count, bins=[x for x in range(TOTAL_CARDS_COUNT)])

    ax.set_title("Оставшиеся карты в игре", size=20)
    ax.set_xlabel('Оставшиеся карты', size=15)
    ax.set_ylabel('Количество игр', size=15)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
