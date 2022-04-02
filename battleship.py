#!/usr/bin/python 
from game import Game

if __name__ == '__main__':
    print("welcome to battleship")
    name = input("what's your name? (enter 'CPU' for CPU-CPU play) ")
    g = Game([name, 'CPU'])
    g.play_game()
