#!/usr/bin/python

import curses
import sys

class Board():
    def __init__(self):
        self.local = [[0 for i in range(10)] for j in range(10)]
        self.remote = [[0 for i in range(10)] for j in range(10)]
        return None

    def set_ship(x_pos, y_pos):
        self.local[y_pos][x_pos] = 1

    def check_target(x_pos, y_pos):
        return self.local[y_pos][x_pos]

class Player():
    def __init__(self, name):
        self.board = Board()
        self.name = name
        return None

    def check_lose(self):
        score = 0
        for i in range(10):
            for j in range(10):
                score += self.board.local[i][j]
        if score <= -17:
            return True

class Game():
    def __init__(self, player_a_name, player_b_name):
        self.a = Player(player_a_name)
        self.b = Player(player_b_name)
        return None

    def check_loser(self, player):
        for player in [self.a, self.b]:
            if player.check_lose():
                print("Player {} Lost!".format(player.name)
        print("no player has lost ... yet!")

    def status(self):
        print("{} is playing against {}".format(self.a.name, self.b.name))

    def board_display(self):
        for y_pos in range(10):
            for x_pos in range(10):

    def end_game(self):

if __name__ == "__main__":
    player_a_name = input("what is player 1's name? ")
    player_b_name = input("what is player 2's name? ")

    g = Game(player_a_name, player_b_name)

    g.addstr("{}, set your ship positions")
        
    g.status()
