#!/usr/bin/python
import curses as nc
import logging
logging.basicConfig(filename='log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HIDE = ''.maketrans('O', '~')


class Display():
    def __init__(self, root):
        self.root = root

    def message(self, string, pos):
        logger.debug(f'{self.root}, {string}, {pos}')
        width = len(string) + 2
        height = 3
        win = self.root.subwin(height, width, pos[1], pos[0])
        win.border()
        win.addstr(1, 1, string)
        win.refresh()

    def display_board(self, board, pos, hidden=False):
        logger.debug(f'{self.root}, {board}, {pos}, {hidden}')
        height = len(board.board) + 2
        width = len(board.board) + 2
        logger.debug(f'height = {height}, width = {width}')
        win = self.root.subwin(height, width, pos[1], pos[0])
        if hidden:
            win.addstr(1, 1, board.curses().translate(HIDE))
        else:
            win.addstr(1, 1, board.curses())
        win.border()
        win.refresh()

    def dialog(self, string, pos):
        logger.debug(f'{self.root}, {string}, {pos}')
        height = 3
        width = len(string) + 3
        logger.debug(f'{height}, {width}, {pos[1]}, {pos[0]}')
        win = self.root.subwin(height, width, pos[1], pos[0])
        logger.debug(f'({1}, {1}), {string}')
        win.addstr(1, 1, string)
        win.border()
        i = win.getkey()
        win.refresh()
        return i


def curses_main(stdscr):
    d = Display(stdscr)
    d.root.clear()
    d.root.keypad(True)
    d.dialog('do you want to quit?', (5, 5))
    d.root.getkey()


if __name__ == "__main__":
    print('testing in __name__ == __main__')
    nc.wrapper(curses_main)
    print('after nc.wrapper')
