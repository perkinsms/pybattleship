#!/usr/bin/python

from yaml import safe_load
from random import (randrange, choice)
from ship import Ship
import logging

logging.basicConfig(filename='log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


with open('config.yaml') as f:
    CFG = safe_load(f)

HIDE = ''.maketrans('O', '~')


class Board:
    def __init__(self, board_size=CFG['BOARD_SIZE']):
        self.ship_list = []
        self.board = [['~' * board_size] for _ in range(board_size)]


    def __repr__(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])


    def curses(self) -> str:
        return '\n '.join([''.join(row) for row in self.board])


    def display_hidden(self) -> str:
        return f' {CFG["X_AXIS"]}\n' + '\n'.join(['{:>2s}'.format(str(i)) + ''.join(row).translate(HIDE)
                                                  for i, row in enumerate(self.board)])


    def get_grid(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])


    def get_hidden_grid(self) -> str:
        return '\n'.join([''.join(row).translate(HIDE) for row in self.board])


    def get_square(self, pos) -> str:
        y = pos[1]
        x = pos[0]
        return self.board[y][0][x]


    def set_square(self, pos, value):
        x = pos[0]
        y = pos[1]
        output = ''.join(self.board[y][0][:x]) + value + ''.join(self.board[y][0][x+1:])
        self.board[y][0] = output
        return None


    def set_ship_part(self, pos):
        if self.get_square(pos) in 'O':
            return False
        else:
            self.set_square(pos, 'O')
            return True


    def random_board(self, ship_list=CFG['SHIP_LIST']):
        for ship in ship_list:
            self.ship_list.append(self.place_ship(ship))
        return self
                

    def check_ship_loc(self, ship):
        for i in range(ship.length):
            pos = (ship.pos[0] + ship.nsew[0] * i,
                   ship.pos[1] + ship.nsew[1] * i)
            if pos[0] >= len(self.board):
                return False
            if pos[1] >= len(self.board):
                return False
            if self.get_square(pos) in 'O':
                return False
        return True


    def set_ship_loc(self, ship):
        for i in range(ship.length):
            pos = (ship.pos[0] + ship.nsew[0] * i,
                   ship.pos[1] + ship.nsew[1] * i)
            self.set_ship_part(pos)
            ship.set_coord(pos)


    def place_ship(self, length):
        while True:
            pos = (randrange(len(self.board)), randrange(len(self.board)))
            nsew = choice([(0, 1), (1, 0)])
            ship = Ship(self, pos, length, nsew)
            if self.check_ship_loc(ship):
                self.set_ship_loc(ship)
                return ship

if __name__ == "__main__":
    b = Board()
    print(b)

    print()
    print(b.curses())