from player import Player
from card import Card, card_factory
from functools import reduce

class Blackjack(object):
    def __init__(self, players):
        self.players = players
        self.setup()

    def setup(self):
        self.active_player = self.players[0] if self.players else None
        for player in self.players:
            player.add_card_to_hand(card_factory())
            player.add_card_to_hand(card_factory())

        self.active_player.set_hand([Card("A"), Card("2")])

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
        if(player.get_score() > 21):
            aces = [x for x in player.get_hand() if x.get_value() == "A"]
            if(len(aces) > 0):
                for i in range(1, len(aces)): aces[i].set_ace_high(False)
                if(player.get_score() > 21 and len(aces)):
                    aces[0].set_ace_high(False)

    def hold(self, player):
        player.set_hold(True)

    def get_players(self):
        return self.players

    def get_dealer(self):
        return self.dealer

    def get_active_player(self):
        return self.active_player

    def set_next_active_player(self):
        # get the players that can play and get the next player
        player_len = len(self.players)
        player_idx = self.players.index(self.active_player)
        for i in range(1, player_len + 1):
            next_player = self.players[(i + player_idx) % player_len]
            if(not next_player.get_score() > 21 and not next_player.is_hold() and not next_player.is_dealer()):
                self.active_player = next_player
                return

        self.active_player = None

    def is_game_over(self):
        return self.active_player == None

    def play_dealer_hand(self):
        self.dealer.show_hand()
        while(self.dealer.get_score() < 16):
            self.dealer.add_card_to_hand(card_factory())

    def get_winners(self):
        possible_winners = [x for x in self.players if x.get_score() <= 21]
        if(self.dealer.get_score() > 21):
            return possible_winners
        else:
            result = []
            ties = []
            for player in possible_winners:
                if(player.get_score() > self.dealer.get_score()):
                    result.append(player)
                elif(player.get_score() == self.dealer.get_score()):
                    ties.append(player)
            if(len(result) != 0):
                return result
            elif(len(ties) != 0):
                ties.append(self.dealer)
                return ties
            else:
                return [self.dealer]
