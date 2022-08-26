#!/usr/bin/env python3

import curses
from typing import List
from src.explorer.FileExplorer import FileExplorer
from src.explorer.FileEntry import FileEntry, Directory
from src.displays.DirectoryPad import DirectoryPad
from src.displays.PadList import PadList

def main():
    curses.wrapper(start)

def start(stdscr):
    stdscr.clear()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, 143, -1) # Darker yellow
    curses.curs_set(0)
    stdscr.refresh()    # Need to call this before rendering anything

    DIR_COLOR = curses.color_pair(1)
    FILE_COLOR = curses.color_pair(2)
    SELECTED_COLOR = curses.color_pair(3)

    fe = FileExplorer()
    directory_view = PadList(fe)

    # User interaction loop
    while True:
        curses.doupdate()   # Change physical screen to match previous update
        k = stdscr.getch()  # Wait for user to hit key
        if k == curses.KEY_UP:
            directory_view.traverse_up()
        elif k == curses.KEY_DOWN:
            directory_view.traverse_down()
        elif k == curses.KEY_LEFT:
            directory_view.traverse_left()
        elif k == curses.KEY_RIGHT:
            directory_view.traverse_right()
        elif k == 10:
            if type(fe.get_selected_entry()) == Directory:
                fe.copy_path()
            else:
                fe.open_file()
            break
        if k == ord('q'):
            break

if __name__ == '__main__':
    main()