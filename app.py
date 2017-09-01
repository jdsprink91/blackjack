from player import Player
from card import Card, card_factory
from blackjack import Blackjack
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master, players):
        super().__init__(master)
        self.blackjack = Blackjack(players)
        self.master = master
        self.create_widgets()

    def get_row_in_grid(self, row):
        for children in self.master.children.values():
            info = children.grid_info()
            if info['row'] == str(row):
                print(info)
                return children
        return None

    def create_active_player_label_text(self):
        self.active_player_label_text.set("It is " + self.blackjack.get_active_player().get_name() + "'s turn")

    def create_widgets(self):
        self.master.title("Blackjack")
        players = self.blackjack.get_players()
        dealer = self.blackjack.get_dealer()

        tk.Label(self.master, text="name").grid(row=0, column = 0, sticky="W")
        tk.Label(self.master, text="hand").grid(row=0, column=1, sticky="W")
        tk.Label(self.master, text="score").grid(row=0, column=2, sticky="W")

        # setup players and dealer
        self.player_to_row = dict()
        for idx, player in enumerate(players):
            real_row_val = idx + 1
            self.setup_player_row(player, real_row_val)

        dealer_row = len(players) + 1
        self.setup_player_row(dealer, dealer_row)

        # setup special buttons and such
        self.last_row_idx = len(players) + 3

        self.hit_btn = tk.Button(self.master, text="Hit", command=self.hit_active_player, width=10)
        self.hit_btn.grid(row=self.last_row_idx, column=0, stick="W")

        self.hold_btn = tk.Button(self.master, text="Hold", command=self.hold_active_player, width=10)
        self.hold_btn.grid(row=self.last_row_idx, column=1, stick="W")

        self.active_player_label_text = tk.StringVar()
        self.create_active_player_label_text()
        self.active_player_label = tk.Label(self.master, textvariable=self.active_player_label_text)
        self.active_player_label.grid(row=self.last_row_idx, column=3, stick="W")

        self.split_btn = tk.Button(self.master, text="Split", command=self.split_active_player, width=10)
        if(self.blackjack.can_split_hand(self.blackjack.get_active_player())):
            self.split_btn.grid(row=self.last_row_idx, column=2)

    def write_player_name(self, player, label, index, color):
        label.config(fg=color)
        label.grid(row=index, column = 0, sticky="W")

    def write_player_hand(self, player, label, index, color):
        label.config(text = player.get_hand_as_str(), fg = color)
        label.grid(row=index, column=1, sticky="W")

    def write_player_score(self, player, label, index, color):
        label.config(text = str(player.get_score()), fg = color)
        label.grid(row=index, column=2, sticky="W")

    def setup_player_row(self, player, index, color="black"):
        self.player_to_row[player] = dict()
        self.player_to_row[player]["name"] = tk.Label(self.master, text=player.get_name() + ": ")
        self.player_to_row[player]["hand"] = tk.Label(self.master, text=player.get_hand_as_str())
        self.player_to_row[player]["score"] = tk.Label(self.master, text=str(player.get_score()))
        self.player_to_row[player]["row_ind"] = index

        self.write_player_info(player)

    def write_player_info(self, player, color="black"):
        player_info = self.player_to_row[player]
        self.write_player_name(player, player_info["name"], player_info["row_ind"], color)
        self.write_player_hand(player, player_info["hand"], player_info["row_ind"], color)
        self.write_player_score(player, player_info["score"], player_info["row_ind"], color)

    def write_after_hand_move_no_bust_hold(self, player, color="black"):
        player_info = self.player_to_row[player]
        self.write_player_hand(player, player_info["hand"], player_info["row_ind"], color)
        self.write_player_score(player, player_info["score"], player_info["row_ind"], color)

    def hit_active_player(self):
        active_player = self.blackjack.get_active_player()
        self.blackjack.hit(active_player)
        if(active_player.get_score() > 21):
            self.write_player_info(active_player, "red")
        else:
            self.write_after_hand_move_no_bust_hold(active_player)
        self.blackjack.set_next_active_player()
        if(self.blackjack.is_game_over()):
            self.end_game()
            return
        self.create_active_player_label_text()

    def hold_active_player(self):
        active_player = self.blackjack.get_active_player()
        self.blackjack.hold(active_player)
        self.write_player_info(active_player, "green")
        self.blackjack.set_next_active_player()
        if(self.blackjack.is_game_over()):
            self.end_game()
            return
        self.create_active_player_label_text()

    def split_active_player(self):
        pass
        
    def end_game(self):
        self.hit_btn.grid_remove()
        self.hold_btn.grid_remove()
        self.active_player_label.grid_remove()

        self.blackjack.play_dealer_hand()
        dealer = self.blackjack.get_dealer()
        if(dealer.get_score() > 21):
            self.write_player_info(dealer, "red")
        else:
            self.write_player_info(dealer)

        winners = [x.get_name() for x in self.blackjack.get_winners()]
        final_text = "No one"
        if(len(winners) > 0):
            final_text = "Winners: "
            final_text += ", ".join(winners)

        tk.Label(self.master, text=final_text).grid(row=self.last_row_idx, column=0, stick="W")


if __name__ == '__main__':
    num_players = input("Number of Players: ")
    while(not num_players.isdigit() or int(num_players) < 1):
        num_players = input("Please enter a positive number: ")

    # generate players and give each of them a hand
    players = [Player(input("Player " + str(x) + " name: ")) for x in range(1, int(num_players) + 1)]

    root = tk.Tk()
    app = Application(root, players)
    app.mainloop()
