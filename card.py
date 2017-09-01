from random import randint

class Card(object):
    def __init__(self, value):
        self.value = value
        self.shown = True
        self.aceHigh = True

    def __str__(self):
        return "card value: " + self.value

    def is_shown(self):
        return self.shown

    def set_shown(self, bool):
        self.shown = bool

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def is_ace_high(self):
        return self.aceHigh

    def set_ace_high(self, bool):
        self.aceHigh = bool


def card_factory():
    # generate rand int between 1 - 13
    cardNum = randint(1, 13)

    # special exceptions
    if(cardNum == 1): return Card("A")
    if(cardNum == 11): return Card("J")
    if(cardNum == 12): return Card("Q")
    if(cardNum == 13): return Card("K")

    # convert int to string and set it
    return Card(str(cardNum))
