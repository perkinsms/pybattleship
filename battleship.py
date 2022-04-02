#!/usr/bin/python 
from game import Game
import curses as nc


def main(stdscr):
    g = Game([name, 'CPU'], stdscr)
    g.play_game()


if __name__ == '__main__':
    print("welcome to battleship")
    name = input("what's your name? (enter 'CPU' for CPU-CPU play) ")
    nc.wrapper(main)

