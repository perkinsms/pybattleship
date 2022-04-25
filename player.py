#!/usr/bin/python
from yaml import safe_load
from random import choice
from sys import exit
from board import HIDE
from utils import (poprandom, find_orthogonals, find_all_9_dirs)
from board import Board
import display

import logging
logging.basicConfig(filename='log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

with open('config.yaml') as f:
    CFG = safe_load(f)


weighted_list = []
for i in range(int(CFG['BOARD_SIZE']/3)):
    weighted_list += list(range(i, CFG['BOARD_SIZE'] - i))


class Player:
    def __init__(self, name, stdscr):
        self.name = name
        self.stdscr = stdscr
        self.display = display.Display(stdscr)
        self.board = None
        self.sunk_ships = []
        self.shots = 0
        self.nukes = 1
        self.curs_x = 6
        self.curs_y = 6
        self.next_shots = []
        stdscr.keypad(True)
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

                self.display.display_board(self.board, (1, 1))
                key = self.display.dialog('OK? Y for yes, a for try again, q to quit: ', (15, 5))
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


    def display_all(self):
        self.stdscr.clear()
        self.display.message('OPP  BOARD', (5, 3))
        self.display.message('YOUR BOARD', (25, 3))
        self.display.display_board(self.board, (25, 5))
        self.display.display_board(self.opp.board, (5, 5), hidden=True)
        if self.nukes >= 1:
            self.display.message(f'You have {self.nukes} nuke' + ('s' if self.nukes > 1 else '') + '. Hit N to nuke', (5, 17))
        display_string = ' '.join([CFG['SHIP_NAME'][ship.length] for ship in self.opp.board.ship_list])
        self.display.message(f'Remaining Ships: {display_string}', (5, 20))
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
            elif key in "N":
                if self.display.dialog(f"NUKE ({self.curs_x -6}, {self.curs_y -6})? You have {self.nukes} nukes remaining. Y to confirm", (5, 22)) == 'Y':
                    self.nuke((self.curs_x - 6, self.curs_y - 6))
            elif key in '\n':
                if self.opp.board.get_square((self.curs_x - 6, self.curs_y - 6)) in 'X*':
                    continue
                else:
                    return self.curs_x - 6, self.curs_y - 6


    def quit_window(self):
        key = self.display.dialog('Quit? are you sure? (y, N)', (10, 10))
        if key in 'yY':
            self.quit()
            return None


    def quit(self, string):
        if string in 'yY':
            exit()


    def shoot_at(self, pos):
        if self.opp.board.get_square(pos) in '~':
            self.opp.board.set_square(pos, '*')
            return False
        elif self.opp.board.get_square(pos) in 'X':
            return False
        elif self.opp.board.get_square(pos) in 'O':
            for ship in self.opp.board.ship_list:
                if ship.shoot_ship(pos):
                    self.opp.board.set_square(pos, 'X')
                    if ship.is_sunk():
                        self.sink(ship)
                    return True

    def nuke(self, pos):
        if self.nukes > 0:
            target_list = find_all_9_dirs(pos)
            for target in target_list:
                self.shoot_at(target)
            self.nukes -= 1
        self.display_all()


    def sink(self, ship):
        self.display.message(f'{self.name} sank a {CFG["SHIP_NAME"][ship.length]}', (10, 10))
        key = self.stdscr.getkey()
        self.sunk_ships.append(ship)
        self.opp.board.delete_ship(ship)
        if len(self.sunk_ships) == len(CFG['SHIP_LIST']):
            self.win()


    def take_turn(self):
        if self.player_type == 'CPU':
            return self.computer_turn()
        self.display_all()
        pos = self.get_target()
        self.shoot_at(pos)
        self.shots += 1
        self.display_all()


    def win(self):
        self.display.message(f'{self.name} wins!!', (10, 8))
        self.display.message(f'{self.name} shot {self.shots} times', (10, 10))

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
