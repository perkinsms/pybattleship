#!/usr/bin/python
from player import Player
from random import shuffle


class Game:
    def __init__(self, names, is_random=False):
        self.players = [Player(name) for name in names]
        self.players[0].opp, self.players[1].opp = (self.players[1], self.players[0])
        for player in self.players:
            player.configure_board(is_random)

    def play_game(self):
        shuffle(self.players)
        while True:
            for player in self.players:
                player.take_turn()
