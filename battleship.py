#!/usr/bin/python 
from game import Game
import curses as nc


import logging
logging.basicConfig(filename='log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main(stdscr):
    logger.info(f'starting game with {name} and CPU')
    g = Game([name, 'CPU'], stdscr)
    g.play_game()


if __name__ == '__main__':
    print("welcome to battleship")
    name = input("what's your name? (enter 'CPU' for CPU-CPU play) ")
    nc.wrapper(main)
