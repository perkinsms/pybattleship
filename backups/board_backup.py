#!/usr/bin/python 

from random import (randrange, choice, randint)
import sys

BOARD_SIZE = 10
SHIPLEN_LIST = [5, 4, 3, 3, 2]
HIDE = ''.maketrans('O', '.')

SHIP_NAME = {
        5: 'Aircraft Carrier',
        4: 'Battleship',
        3: 'Destroyer',
        2: 'PT Boat',
        }

class Board():
    def __init__(self, board_size=BOARD_SIZE):
        self.board = [['.'] * board_size for i in range(board_size)]
        return None

    def __repr__(self):
        return '  1234567890\n' + '\n'.join(['{:2s}'.format(str(i + 1)) + ''.join(row) for i, row in enumerate(self.board)])

    def display_hidden(self):
        return '  1234567890\n' + '\n'.join(['{:2s}'.format(str(i + 1)) + ''.join(row).translate(HIDE) for i,row in enumerate(self.board)])

    def get_square(self, pos):
        #print(f'checking position in get_square {pos}')
        y = pos[1]
        x = pos[0]
        return self.board[y][x]

    def set_square(self, pos, value):
        y = pos[1]
        x = pos[0]
        self.board[y][x] = value

    def shoot_at(self, target, player):
        for ship in self.ship_list:
            if ship.shoot_at(target, player):
                self.set_square(target, 'X')
                return True
        self.set_square(target, '*')
        return False

    def set_ship_part(self, pos):
        if self.get_square(pos) in ['O']:
            return False
        else:
            self.set_square(pos, 'O')
            return True

    def random_board(self, shiplen_list=SHIPLEN_LIST):
        self.ship_list = []
        valid_board = False
        for shiplen in shiplen_list:
            #print(f'placing ship of length {shiplen}')
            self.ship_list.append(self.place_ship(shiplen))
        return self
                
    def check_ship_loc(self, ship):
        for i in range(ship.length):
            pos = (ship.pos[0] + ship.dir[0] * i, 
                   ship.pos[1] + ship.dir[1] * i)

            if pos[0] >= len(self.board):
                #print('invalid, off board')
                return False
            if pos[1] >= len(self.board):
                #print('invalid, off board')
                return False
            #print(f'checking position {pos} for ship')
            if self.get_square(pos) in ['O']:
                #print('not valid')
                return False
        #print('valid')
        return True

    def set_ship_loc(self, ship):
        for i in range(ship.length):
            pos = (ship.pos[0] + ship.dir[0] * i,\
                   ship.pos[1] + ship.dir[1] * i)
            self.set_ship_part(pos)
            ship.set_coord(pos)

    def place_ship(self,shiplen):
        while True:
            pos = (randrange(len(self.board)), randrange(len(self.board)))
            dir = choice([(0,1), (1,0)])
            s = Ship(self, pos, shiplen, dir)
            #print(f'checking location at {pos}')
            if self.check_ship_loc(s):
                #print(f'found valid location at {pos}')
                self.set_ship_loc(s)
                return s

class Ship():
    def __init__(self, board, pos, length, dir):
        self.board = board
        self.pos = pos
        self.length = length
        self.dir = dir
        self.coords = {}
        self.left = length

    def __repr__(self):
        return f' Ship at {self.pos} pointing to {self.dir}'

    def set_coord(self, pos):
        self.coords[pos] = 'O'

    def get_coords(self):
        #print('getting coords')
        #print(self.coords)
        return self.coords

    def hit_coord(self,pos,player):
        self.coords[pos] = 'X'
        self.left -= 1
        if self.left == 0:
            self.sink(player)
            player.sink()


    def shoot_at(self, target, player):
        for coord in self.coords:
            if target == coord:
                self.hit_coord(target, player)
                return True
        return False

    def sink(self,player):
        print(f'{player.name} sank a {SHIP_NAME[self.length]}')

class Player():
    def __init__(self, name):
        self.name = name
        self.board = None
        self.sunk_ships = 0
        self.shots = 0

    def __repr__(self):
        return f'Player {self.name} has {len(self.opp.board.ship_list) - self.opponent.sunk_ships} remaining'

    
    def sink(self):
        self.sunk_ships +=1
        if len(self.board.ship_list) == self.sunk_ships:
            self.win()

    def win(self):
        print(f'{self.name} wins!')
        print(f'{self.name} shot {self.shots} times')
        sys.exit()

class Game():
    def __init__(self, name1, name2):
        self.p1 = Player(name1)
        self.p2 = Player(name2)
        (self.p1.opp, self.p2.opp) = (self.p2, self.p1)
        return None

def player_turn(player):

    print('opponent board')
    print(player.opp.board.display_hidden())

    while True:

        x = input(f'x coordinate? 1 to {BOARD_SIZE} ') 
        y = input(f'y coordinate? 1 to {BOARD_SIZE} ')

        if x == 'q' or y == 'q':
            sys.exit()
        try: 
            x = int(x)
            y = int(y)
            if (x > BOARD_SIZE or x < 1 or\
            y > BOARD_SIZE or y < 1):
                print(f'invalid entry: ({x}, {y})')
                continue
        except ValueError:
            print(f'invalid entry: ({x}, {y})')
            continue

        if player.opp.board.get_square((x-1, y-1)) in ['X', '*']:
            print('already shot there!')
            continue

        player.shots += 1
        if player.opp.board.shoot_at((x-1, y-1), player):
            print("Hit")
            break
        else:
            print("Miss")
            break


def computer_turn(player):
    while True:
        x = randint(1,BOARD_SIZE)
        y = randint(1,BOARD_SIZE)

        if player.opp.board.get_square((x-1, y-1)) in ['X', '*']:
            continue


        player.shots +=1
        if player.opp.board.shoot_at((x-1, y-1), player):
            print('computer hits!')
            break
        else:
            print('computer misses!')
            break

    print(player.opp.board)

if __name__ == '__main__':

    print("welcome to battleship")
    name = input("what's your name? ")

    g = Game(name, 'Computer')

    player = g.p1
    computer = g.p2


    while True:
        b = Board()
        b.random_board()
        print(b)
        a = input("how does this board look? (y for yes, a for try again, q to quit): ")

        if a == 'q':
            sys.exit()

        if a == 'y':
            player.board = b
            break

    #print('setting my board')
    computer.board = Board().random_board()

    while True:
        player_turn(player)
        computer_turn(computer)
