#!/usr/bin/python

import logging
logging.basicConfig(filename='log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Ship:
    def __init__(self, board, pos, length, nsew):
        logger.info(f"making a new ship: pos: {pos} length: {length}")
        self.board = board
        self.pos = pos
        self.length = length
        self.nsew = nsew
        self.coords = {}
        self.left = length

    def __repr__(self):
        return f' Ship at {self.pos} pointing to {self.nsew}'

    def set_coord(self, pos):
        logger.info(f'setting content to "O"')
        self.coords[pos] = 'O'

    def get_coords(self):
        return self.coords

    def record_hit(self, pos):
        self.coords[pos] = 'X'
        self.left -= 1

    def is_sunk(self):
        logger.info(f'ship is sunk: {self}')
        if self.left == 0:
            return True
        else:
            return False

    def shoot_ship(self, pos):
        logger.info(f'shooting at {self}')
        for coord in self.coords:
            if pos == coord:
                self.record_hit(pos)
                return True
        return False
