from functools import reduce

class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.hold = False
        self.dealer = False

    def get_hand(self):
        return self.hand

    def set_hand(self, hand):
        self.hand = hand

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def is_hold(self):
        return self.hold

    def set_hold(self, hold):
        self.hold = hold

    def is_dealer(self):
        return self.dealer

    def set_dealer(self, dealer):
        self.dealer = dealer

    def add_card_to_hand(self, card):
        self.hand.append(card)

    # "flips" all hidden cards
    def show_hand(self):
        for card in self.hand:
            if not card.is_shown():
                card.set_shown(True)

    # returns string of all of your shown cards
    def get_hand_as_str(self):
        handToShow = []
        for card in self.hand:
            if card.is_shown():
                cardVal = card.get_value()
                if(cardVal != "A"):
                    handToShow.append(cardVal)
                else:
                    if card.is_ace_high():
                        handToShow.append("A (high)")
                    else:
                        handToShow.append("A (low)")
        return ", ".join(handToShow)
