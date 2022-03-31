#!/usr/bin/python

import curses
import game
from board import HIDE

def curses_main(stdscr):
    g = game.Game(['Michael','CPU'], is_random=True)
    curs_y = 3
    curs_x = 3
    stdscr.keypad(True)

    my_board_win = stdscr.subwin(12, 12, 5, 5)
    your_board_win = stdscr.subwin(12, 12, 5, 24)

    while True:
        stdscr.clear()
        stdscr.addstr(4,5,'OPP BOARD')
        stdscr.addstr(4, 24, 'YOUR BOARD')
        my_board_win.addstr(1, 1, str(g.players[0].opp.board.curses().translate(HIDE)))
        your_board_win.addstr(1, 1, str(g.players[0].board.curses()))
        my_board_win.border()
        your_board_win.border()
        stdscr.addstr(0,0, f'Cursor = ({curs_x}, {curs_y})')
        stdscr.move(curs_y + 6, curs_x + 6)
        key = stdscr.getkey()
        stdscr.refresh()
        if key   == "KEY_UP":
            curs_y -= 1 if curs_y > 0 else 0
        elif key == "KEY_DOWN":
            curs_y += 1 if curs_y < 9 else 0
        elif key == "KEY_LEFT":
            curs_x -= 1 if curs_x > 0 else 0
        elif key == "KEY_RIGHT":
            curs_x += 1 if curs_x < 9 else 0
        elif key in 'qQ':
            quitwin = stdscr.subwin(3, 27, 10, 10)
            quitwin.border()
            quitwin.addstr(1,1, 'Quit? are you sure? (y/N)')
            key = quitwin.getkey()
            quitwin.refresh()
            if key in 'yY':
                break
        elif key in '\n':
            g.players[0].shoot_at((curs_x,curs_y))
            g.players[1].take_turn()

if __name__ == '__main__':
    curses.wrapper(curses_main)
