import logging
import multiprocessing
import random
import time

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from tqdm import tqdm

from player import Players, Player
from settings import PLAYERS_COUNT, GAMES_COUNT, RANDOM_SEED, TOTAL_CARDS_COUNT, PROCESS_WORKERS, USE_TQDM, STACKS_COUNT
from stack import Stacks, DecreaseStack, IncreaseStack
from strategies.flag_strategy import FlagStrategy
from strategies.min_max_strategy import MinMaxStrategy
from strategies.strategy import Strategy
from the_game import TheGame, TheGameReport

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

random.seed(RANDOM_SEED)

strategy_class = FlagStrategy

def play_games() -> list[TheGameReport]:
    start_time = time.time()
    if PROCESS_WORKERS == 1:
        played_games = [play_game(_) for _ in range(GAMES_COUNT)]
    else:
        with multiprocessing.Pool(processes=PROCESS_WORKERS) as pool:
            if USE_TQDM:
                pool = pool.imap_unordered(play_game, range(GAMES_COUNT))
                _tqdm = tqdm(pool, total=GAMES_COUNT, mininterval=1.0, smoothing=0.2)
                played_games = []
                for _ in _tqdm:
                    played_games.append(_)
            else:
                played_games = pool.map(play_game, range(GAMES_COUNT))

    end_time = time.time()
    logger.info(f"Время выполнения программы - {round(end_time - start_time, 3)} секунд")

    return played_games


def play_game(_) -> TheGameReport:
    players_list = [Player() for _ in range(PLAYERS_COUNT)]
    players = Players(*players_list)

    increase_stacks = [IncreaseStack() for _ in range(STACKS_COUNT)]
    decrease_stacks = [DecreaseStack() for _ in range(STACKS_COUNT)]

    stacks = Stacks(
        *increase_stacks,
        *decrease_stacks
    )
    strategy = strategy_class(players, stacks)

    the_game = TheGame(players, strategy=strategy, stacks=stacks)
    the_game.play()

    return the_game.get_report()


def main():
    played_games = play_games()
    log_statistics(played_games)
    draw_cards_count(played_games, strategy=strategy_class)


def log_statistics(played_games_reports: list[TheGameReport]):
    win_games_count = len([_ for _ in played_games_reports if _.is_win])
    cards_count = [x.total_cards_count for x in played_games_reports]

    logger.info(f"Выиграно игр - {win_games_count}/{GAMES_COUNT}")
    winrate = round(win_games_count / GAMES_COUNT * 100, 2)
    logger.info(f"Винрейт - {winrate}%")
    avg_cards_count = round(sum(cards_count) / len(cards_count), 2)
    logger.info(f"В среднем остаётся карт на руках и в колоде - {avg_cards_count}")


def draw_cards_count(played_games_reports: list[TheGameReport], strategy: type[Strategy]):
    cards_count = [x.total_cards_count for x in played_games_reports]

    ax = plt.subplot()

    ax.hist(cards_count, bins=[x for x in range(TOTAL_CARDS_COUNT)], density=True)

    # Форматирование оси Y в проценты
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))

    ax.set_title(f"{strategy.name}. {GAMES_COUNT} игр", size=20)
    ax.set_xlabel('Оставшиеся карты', size=15)
    ax.set_ylabel('Процент игр', size=15)

    ax.set_xlim([0, TOTAL_CARDS_COUNT])
    ax.set_ylim([0, 0.1])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
