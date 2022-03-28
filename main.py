from Game import Game
from consts import CARDS, STACKS

GAMES = 10000


def main():
    played_cards_count = []
    game_stats = []
    max_played_cards = CARDS - 2

    for _ in range(GAMES):
        game = Game()
        game.play()

        cards_in_game = sum([len(stack.cards) for stack in game.stacks]) - STACKS
        played_cards_count.append(cards_in_game)

        is_win_game = cards_in_game == max_played_cards
        game_stats.append(is_win_game)

    avg_played_cards = sum(played_cards_count) / len(played_cards_count)
    avg_played_cards_perc = avg_played_cards / max_played_cards * 100
    median_played_cards = sorted(played_cards_count)[:GAMES // 2][0]
    median_played_cards_perc = median_played_cards / max_played_cards * 100
    win_games = sum(game_stats)
    win_games_perc = win_games / GAMES * 100
    print(f"avg played cards in game = {avg_played_cards} / {max_played_cards} ({avg_played_cards_perc}%)")
    print(f"median played cards in game = {median_played_cards} / {max_played_cards} ({median_played_cards_perc}%)")
    print(f"win games = {win_games} / {GAMES} ({win_games_perc}%)")


if __name__ == "__main__":
    main()
