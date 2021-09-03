#!/usr/bin/env python3

import curses
from typing import List
from explorer.FileExplorer import FileExplorer
from explorer.FileEntry import FileEntry, Directory
from displays.DirectoryPad import DirectoryPad

def main(stdscr):
    stdscr.clear()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.curs_set(0)
    stdscr.refresh()    # Need to call this before rendering anything

    DIR_COLOR = curses.color_pair(1)
    FILE_COLOR = curses.color_pair(2)
    SELECTED_COLOR = curses.color_pair(3)

    fe = FileExplorer()
    curr_dir_pad = DirectoryPad(fe)
    curr_dir_pad.select_file(0)

    # User interaction loop
    while True:
        curses.doupdate()
        k = stdscr.getch()
        if k == curses.KEY_UP:
            curr_dir_pad.traverse_up()
        elif k == curses.KEY_DOWN:
            curr_dir_pad.traverse_down()
        elif k == curses.KEY_LEFT:
            stdscr.addstr("KEYED LEFT\n", DIR_COLOR)
        elif k == curses.KEY_RIGHT:
            stdscr.addstr("KEYED RIGHT\n", DIR_COLOR)
        elif k == 10:
            stdscr.addstr("KEYED ENTER\n", DIR_COLOR)
        if k == ord('q'):
            break


if __name__ == '__main__':
    curses.wrapper(main)
