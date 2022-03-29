#!/usr/bin/python

BOARD_SIZE = 10
SHIPLEN_LIST = [5, 4, 3, 3, 2]
HIDE = ''.maketrans('O', '.')
X_AXIS = 'ABCDEFGHIJ'

class Board():
    def __init__(self, board_size=BOARD_SIZE):
        self.board = [['.' * board_size] for i in range(board_size)]
        return None

    def __repr__(self) -> str:
        return f'  {X_AXIS}\n' + '\n'.join(['{:>2s}'.format(str(i)) + ''.join(row) for i, row in enumerate(self.board)])

    def display_hidden(self) -> str:
        return f'  {X_AXIS}\n' + '\n'.join(['{:>2s}'.format(str(i)) + ''.join(row).translate(HIDE) for i,row in enumerate(self.board)])

    def get_grid(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])

    def get_hidden_grid(self) -> str:
        return '\n'.join([''.join(row).translate(HIDE) for row in self.board])

    def get_square(self, pos) -> str:
        #print(f'checking position in get_square {pos}')
        y = pos[1]
        x = pos[0]
        #print(f'DEBUG: {y}')
        #print(f'DEBUG: {x}')

        return self.board[y][0][x]

    def set_square(self, pos, value):
        y = pos[1]
        x = pos[0]
        newstring = ''.join(self.board[y][0][:x]) + value + ''.join(self.board[y][0][x+1:])
        self.board[y][0] = newstring
        return None

    def set_ship_part(self, pos):
        if self.get_square(pos) in 'O':
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
            if self.get_square(pos) in 'O':
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
