from player import Player
from card import Card, card_factory
from functools import reduce

class Blackjack(object):
    def __init__(self, players):
        # set numbers in case you want to change these easily
        self.upper_limit = 21
        self.dealer_limit = 16
        self.players = players
        self.setup()

    # private, only needed in this class
    def __getNumValue(self, card):
        cardVal = card.get_value()
        if(cardVal in ["J", "Q", "K"]):
            return 10
        elif(cardVal == "A"):
            return 11 if card.is_ace_high() else 1
        elif cardVal.isdigit():
            return int(cardVal)
        else:
            return 0


    def get_players(self):
        return self.players

    def get_dealer(self):
        return self.dealer

    def get_active_player(self):
        return self.active_player

    def setup(self):
        self.active_player = self.players[0] if self.players else None
        for player in self.players:
            # in case we get two aces
            player.add_card_to_hand(card_factory())
            player.add_card_to_hand(card_factory())
            self.configure_aces(player, self.upper_limit)

        # generate the dealer
        self.dealer = Player("Dealer")
        self.dealer.set_dealer(True)
        self.dealer.add_card_to_hand(card_factory())
        dealer_hidden_card = card_factory()
        dealer_hidden_card.set_shown(False)
        self.dealer.add_card_to_hand(dealer_hidden_card)

    def hit(self, player):
        # get next card and see if they've busted
        player.add_card_to_hand(card_factory())

        # check the aces and set them accordinglys
        if(self.get_score(player) > self.upper_limit):
            self.configure_aces(player, self.upper_limit)

    def hold(self, player):
        player.set_hold(True)

    def get_score(self, player):
        return reduce(
            lambda acc, curr: acc + self.__getNumValue(curr) if curr.is_shown() else acc,
            player.get_hand(),
            0)

    # function to see how many high aces you can have in your hand
    def configure_aces(self, player, limit):
        aces = [x for x in player.get_hand() if x.get_value() == "A"]
        if(len(aces) > 0):
            for i in range(1, len(aces)): aces[i].set_ace_high(False)
            if(self.get_score(player) > limit):
                aces[0].set_ace_high(False)

    # modifies internal state. specifically the active_player
    def set_next_active_player(self):
        player_len = len(self.players)
        player_idx = self.players.index(self.active_player)
        for i in range(1, player_len + 1):
            next_player = self.players[(i + player_idx) % player_len]
            if(not self.get_score(next_player) > self.upper_limit
                and not next_player.is_hold()
                and not next_player.is_dealer()):
                self.active_player = next_player
                return

        # will be here if game is over
        self.active_player = None

    def play_dealer_hand(self):
        self.dealer.show_hand()
        while(self.get_score(self.dealer) < self.dealer_limit):
            self.dealer.add_card_to_hand(card_factory())
            self.configure_aces(self.dealer, self.dealer_limit)

    def can_split_hand(self, player):
        hand = player.get_hand()
        # can only split if you have two cards
        return len(hand) == 2 and hand[0].get_value() == hand[1].get_value()

    def is_game_over(self):
        return self.active_player == None

    def get_winners(self):
        possible_winners = [x for x in self.players if self.get_score(x) <= self.upper_limit]
        if(self.get_score(self.dealer) > self.upper_limit):
            return possible_winners
        else:
            result = []
            ties = []
            for player in possible_winners:
                if(self.get_score(player) > self.get_score(self.dealer)):
                    result.append(player)
                elif(self.get_score(player) == self.get_score(self.dealer)):
                    ties.append(player)
            if(len(result) != 0):
                return result
            elif(len(ties) != 0):
                ties.append(self.dealer)
                return ties
            else:
                return [self.dealer]
