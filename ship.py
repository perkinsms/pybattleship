#!/usr/bin/python

class Ship:
    def __init__(self, board, pos, length, nsew):
        self.board = board
        self.pos = pos
        self.length = length
        self.nsew = nsew
        self.coords = {}
        self.left = length

    def __repr__(self):
        return f' Ship at {self.pos} pointing to {self.nsew}'

    def set_coord(self, pos):
        self.coords[pos] = 'O'

    def get_coords(self):
        return self.coords

    def record_hit(self, pos):
        self.coords[pos] = 'X'
        self.left -= 1

    def is_sunk(self):
        if self.left == 0:
            return True
        else:
            return False

    def shoot_ship(self, pos):
        for coord in self.coords:
            if pos == coord:
                self.record_hit(pos)
                return True
        return False
