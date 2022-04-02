#!/usr/bin/python

from yaml import safe_load
from random import choice
from sys import exit
from board import HIDE
from utils import (poprandom, find_orthogonals)
from board import Board

with open('config.yaml') as f:
    CFG = safe_load(f)

weighted_list = []
for i in range(int(CFG['BOARD_SIZE']/3)):
    weighted_list += list(range(i, CFG['BOARD_SIZE'] - i))


class Player:
    def __init__(self, name, stdscr):
        self.name = name
        self.board = None
        self.sunk_ships = []
        self.shots = 0
        self.curs_x = 5
        self.curs_y = 5
        self.next_shots = []
        self.stdscr = stdscr
        self.stdscr.keypad(True)
        if self.name == 'CPU':
            self.player_type = 'CPU'
        else:
            self.player_type = 'Human'


    def __repr__(self):
        return f'Player {self.name} has {len(self.opp.board.ship_list) - len(self.opp.sunk_ships)} remaining'


    def configure_board(self, random=False):
        if self.player_type == 'CPU':
            self.board = Board().random_board()
        else:
            while True:
                self.board = Board().random_board()
                if random:
                    break
                self.display_mine()
                self.stdscr.addstr(20, 5, 'How does this board look? (y for yes, a for try again, q to quit): ')
                key = self.stdscr.getkey()
                if key == 'q':
                    exit()
                elif key == 'a':
                    continue
                elif key == 'y':
                    break


    def display_mine(self):
        my_win = self.stdscr.subwin(12, 12, 5, 5)
        self.stdscr.addstr(4,5, 'YOUR BOARD')
        my_win.addstr(1, 1, str(self.board.curses()))
        my_win.border()
        self.stdscr.refresh()


    def display(self):
        my_win = self.stdscr.subwin(12, 12, 5, 5)
        your_win = self.stdscr.subwin(12, 12, 5, 24)
        self.stdscr.clear()
        self.stdscr.addstr(4, 5, 'OPP BOARD')
        self.stdscr.addstr(4, 24, 'YOUR BOARD')
        my_win.addstr(1, 1, str(self.opp.board.curses().translate(HIDE)))
        your_win.addstr(1, 1, str(self.board.curses()))
        my_win.border()
        your_win.border()
        self.stdscr.refresh()


    def get_target(self):
        while True:
            self.stdscr.move(self.curs_y, self.curs_x)
            self.stdscr.refresh()
            key = self.stdscr.getkey()
            if key == "KEY_UP":
                self.curs_y -= 1 if self.curs_y > 6 else 0
            elif key == "KEY_DOWN":
                self.curs_y += 1 if self.curs_y < 15 else 0
            elif key == "KEY_LEFT":
                self.curs_x -= 1 if self.curs_x > 6 else 0
            elif key == "KEY_RIGHT":
                self.curs_x += 1 if self.curs_x < 15 else 0
            elif key in 'qQ':
                self.quit_window()
            elif key in '\n':
                if self.opp.board.get_square((self.curs_x - 6, self.curs_y - 6)) in 'X*':
                    continue
                else:
                    return self.curs_x - 6, self.curs_y - 6


    def quit_window(self):
        quitwin = self.stdscr.subwin(3, 27, 10, 10)
        quitwin.border()
        quitwin.addstr(1, 1, 'Quit? are you sure? (y, N)')
        key = quitwin.getkey()
        quitwin.refresh()
        if key in 'yY':
            exit()


    def shoot_at(self, pos):
        if self.opp.board.get_square(pos) not in 'O':
            self.opp.board.set_square(pos, '*')
            return False
        else:
            for ship in self.opp.board.ship_list:
                if ship.shoot_ship(pos):
                    self.opp.board.set_square(pos, 'X')
                    if ship.is_sunk():
                        self.sink(ship)
                    return True


    def sink(self, ship):
        self.stdscr.addstr(5,5, f'{self.name} sank a {CFG["SHIP_NAME"][ship.length]}')
        self.stdscr.refresh()
        key = self.stdscr.getkey()
        self.sunk_ships.append(ship)
        if len(self.board.ship_list) == len(self.sunk_ships):
            self.win()


    def take_turn(self):
        if self.player_type == 'CPU':
            return self.computer_turn()
        self.display()
        pos = self.get_target()
        self.shoot_at(pos)
        self.shots += 1
        self.display()


    def win(self):
        self.stdscr.addstr(5,5, f'{self.name} wins!')
        self.stdscr.addstr(6,5, f'{self.name} shot {self.shots} times')
        self.stdscr.getkey()
        exit()


    def computer_turn(self):
        while True:
            if not self.next_shots:
                self.next_shots = []
                pos = (choice(weighted_list), choice(weighted_list))
                if self.shots >= 35:
                    spacing = 2
                else:
                    spacing = 3
                if (pos[0] + pos[1]) % spacing != 0:
                    continue
            else:
                (pos, self.next_shots) = poprandom(self.next_shots)
            if self.opp.board.get_square(pos) in ['X', '*']:
                continue
            self.shots += 1
            if self.shoot_at(pos):
                self.next_shots += find_orthogonals(pos)
                break
            else:
                break
        return None
