#!/usr/bin/python

from yaml import safe_load
from random import choice
from sys import exit

with open('config.yaml') as f:
    CFG = safe_load(f)

from utils import (parse_input, poprandom, sum_points, out_of_bounds, find_orthogonals, find_all_9_dirs)
from board import Board
from ship import Ship

weighted_list = []
for i in range(int(CFG['BOARD_SIZE']/3)):
    weighted_list += list(range(i, CFG['BOARD_SIZE'] - i))

class Player():
    def __init__(self, name):
        self.name = name
        self.board = None
        self.sunk_ships = 0
        self.shots = 0
        self.next_shots = []
        if self.name == 'CPU':
            self.player_type = 'CPU'
        else:
            self.player_type = 'Human'


    def __repr__(self):
        return f'Player {self.name} has {len(self.opp.board.ship_list) - self.opp.sunk_ships} remaining'

    
    def configure_board(self):

        if self.player_type == 'CPU':
            self.board = Board().random_board()
        else:
            while True:
                b = Board().random_board()
                print(b)
                a = input("how does this board look? (y for yes, a for try again, q to quit): ")

                if a == 'q':
                    exit()

                if a == 'y':
                    self.board = b
                    break

    def shoot_at(self, pos):
        for ship in self.opp.board.ship_list:
            if ship.shoot_ship(pos):
                self.opp.board.set_square(pos, 'X')
                if ship.is_sunk():
                    self.sink(ship)
                return True
            else:
                self.opp.board.set_square(pos, '*')
        return False

    def sink(self, ship):
        print(f'{self.name} sunk a {CFG["SHIP_NAME"][ship.length]}')
        self.sunk_ships +=1
        #self.next_shots = []
        if len(self.board.ship_list) == self.sunk_ships:
            self.win()

    def win(self):
        print(f'{self.name} wins!')
        print(f'{self.name} shot {self.shots} times')
        exit()

    def take_turn(self):
        if self.player_type == 'CPU':
            return self.computer_turn()

        print('opponent board')
        print(self.opp.board.display_hidden())

        while True:

            pos = self.get_target()

            if not pos:
                continue

            self.shots += 1
            if self.shoot_at(pos):
                print("Hit")
                break
            else:
                print("Miss")
                break

    def get_target(self):
        inp = input(f'enter target coordiates: (e.g., A7, QQ to quit) ') 
        if str(inp).upper() == 'QQ':
            exit()

        pos = parse_input(inp)
        if pos[0] in [CFG['INVALID_STRING'], CFG['OUT_OF_BOUNDS']]:
            print('Invalid Entry')
            return False

        if self.opp.board.get_square(pos) in ['X', '*']:
            print('already shot there!')
            return False

        else:
            return pos

    def computer_turn(self):
        while True:
            if not self.next_shots:
                self.next_shots = []
                pos = (choice(weighted_list), choice(weighted_list))
                if (pos[0] + pos[1]) % 3 != 0:
                    continue
                #print(f'DEBUG: shooting randomly, target = {pos}')
            else:
                #print(f'DEBUG: next shots: {self..next_shots}')
                (pos, self.next_shots) = poprandom(self.next_shots)
                #print(f'DEBUG: shooting at target = {pos}')
            if self.opp.board.get_square(pos) in ['X', '*']:
                continue
            self.shots +=1
            if self.shoot_at(pos):
                self.next_shots += find_orthogonals(pos)
                #print(f'DEBUG: appending next shots: {find_orthogonals(pos)}')
                print('computer hits!')
                break
            else:
                print('computer misses!')
                break

        print('your board')
        print(self.opp.board)
        return None
