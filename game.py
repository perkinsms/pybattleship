#!/usr/bin/python

from player import Player
from random import shuffle

class Game():
    def __init__(self, names, is_random=False):
        self.players = [Player(name) for name in names]
        for player in self.players:
            player.configure_board(is_random)
        (self.players[0].opp, self.players[1].opp) = (self.players[1], self.players[0])
        return None

    def play_game(self):
        shuffle(self.players)
        while True:
            for player in self.players:
                player.take_turn()
