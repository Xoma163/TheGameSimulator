class Card:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return self.__str__()
