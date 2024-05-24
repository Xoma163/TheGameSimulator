## Настройки игры

# Количество игроков
PLAYERS_COUNT = 4
# Количество карт на руках игроков
PLAYER_CARDS_COUNT = 6
# Минимальное значение карты
MIN_CARD_VALUE = 2
# Максимальное значение карты
MAX_CARD_VALUE = 99
# Минимум выложенных карт в обычный ход
MIN_STEPS = 2
# Минимум выложенных карт в ход, когда в колоде не осталось карт
MIN_STEPS_ON_EMPTY_DECK = 1

# Количество стопок на повышение и на понижение. Всего их будет в два раза больше
STACKS_COUNT = 2

## Условия

# Сколько должно остаться карт чтобы была зачтена победа
CARDS_LEFT_COUNT_TO_WIN = 10

# Сколько игр проводить
GAMES_COUNT = 100_000

## Служебное

# SEED
RANDOM_SEED = 1

TOTAL_CARDS_COUNT = MAX_CARD_VALUE - MIN_CARD_VALUE + 1

# Количество воркеров процессора
PROCESS_WORKERS = 16
# PROCESS_WORKERS = 1
USE_TQDM = False
