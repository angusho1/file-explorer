#!/usr/bin/env python3

import curses
from typing import List
from explorer.FileExplorer import FileExplorer
from explorer.FileEntry import FileEntry, Directory
from displays.DirectoryPad import DirectoryPad

def main(stdscr):
    stdscr.clear()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.curs_set(0)
    stdscr.refresh()

    DIR_COLOR = curses.color_pair(1)
    FILE_COLOR = curses.color_pair(2)
    SELECTED_COLOR = curses.color_pair(3)

    fe = FileExplorer()
    curr_dir_pad = DirectoryPad(fe.curr_dir_entries)

    # User interaction loop
    while True:
        stdscr.refresh()
        k = stdscr.getch()
        if k == curses.KEY_UP:
            fe.traverse_up()
            curr_dir_pad.traverse_up()
        elif k == curses.KEY_DOWN:
            fe.traverse_down()
            curr_dir_pad.traverse_down()
        elif k == curses.KEY_LEFT:
            curr_dir_pad.addstr("KEYED LEFT\n", DIR_COLOR)
        elif k == curses.KEY_RIGHT:
            curr_dir_pad.addstr("KEYED RIGHT\n", DIR_COLOR)
        elif k == 10:
            curr_dir_pad.addstr("KEYED ENTER\n", DIR_COLOR)
        if k == ord('q'):
            break


if __name__ == '__main__':
    curses.wrapper(main)
