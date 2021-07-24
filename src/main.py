#!/usr/bin/env python3

import os
import curses
from typing import List
from explorer.FileExplorer import FileExplorer
from explorer.FileEntry import FileEntry, Directory

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    fe = FileExplorer()
    for entry in fe.get_curr_file_entries():
        if type(entry) == Directory:
            stdscr.addstr(f'{entry.name}\n', curses.color_pair(2))
        else:
            stdscr.addstr(f'{entry.name}\n', curses.color_pair(1))
    stdscr.refresh()

    while True:
        stdscr.refresh()
        k = stdscr.getch()
        if k == ord('q'):
            break
        elif k == curses.KEY_UP:
            stdscr.addstr("KEYED UP\n", curses.color_pair(1))
        elif k == curses.KEY_DOWN:
            stdscr.addstr("KEYED DOWN\n", curses.color_pair(1))
        elif k == curses.KEY_LEFT:
            stdscr.addstr("KEYED LEFT\n", curses.color_pair(1))
        elif k == curses.KEY_RIGHT:
            stdscr.addstr("KEYED RIGHT\n", curses.color_pair(1))
        elif k == 10:
            stdscr.addstr("KEYED ENTER\n", curses.color_pair(1))


if __name__ == '__main__':
    curses.wrapper(main)
