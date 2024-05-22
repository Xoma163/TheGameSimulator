class Card:
    """
    Карта
    """

    def __init__(self, number: int):
        """
        Инициализация карты

        :param number: номер карты
        """
        self.number: int = number

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.number == other.number

    def __ne__(self, other) -> bool:
        return self.number != other.number

    def __lt__(self, other) -> bool:
        return self.number < other.number

    def __le__(self, other) -> bool:
        return self.number <= other.number

    def __gt__(self, other) -> bool:
        return self.number > other.number

    def __ge__(self, other) -> bool:
        return self.number >= other.number

    def __sub__(self, other) -> bool:
        return self.number - other.number

    def __add__(self, other) -> bool:
        return self.number + other.number
