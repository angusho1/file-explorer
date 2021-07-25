#!/usr/bin/env python3

import curses
from typing import List
from explorer.FileExplorer import FileExplorer
from explorer.FileEntry import FileEntry, Directory

def main(stdscr):
    stdscr.clear()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.curs_set(0)
    stdscr.refresh()

    fe = FileExplorer()
    curr_dir_pad = create_dir_pad(fe.curr_dir_entries)

    # User interaction loop
    while True:
        stdscr.refresh()
        k = stdscr.getch()
        if k == curses.KEY_UP:
            curr_dir_pad.addstr("KEYED UP\n", curses.color_pair(1))
        elif k == curses.KEY_DOWN:
            curr_dir_pad.addstr("KEYED DOWN\n", curses.color_pair(1))
        elif k == curses.KEY_LEFT:
            curr_dir_pad.addstr("KEYED LEFT\n", curses.color_pair(1))
        elif k == curses.KEY_RIGHT:
            curr_dir_pad.addstr("KEYED RIGHT\n", curses.color_pair(1))
        elif k == 10:
            curr_dir_pad.addstr("KEYED ENTER\n", curses.color_pair(1))
        if k == ord('q'):
            break


def create_dir_pad(file_entries: List[FileEntry]) -> curses.window:
    num_entries = len(file_entries)
    max_filename_length = len(max(file_entries, key=lambda x: len(x.name)).name)
    pad = curses.newpad(num_entries+1, max_filename_length+1)
    cursor_coords = curses.getsyx()
    for i, entry in enumerate(file_entries):
        if cursor_coords[0] == i:
            pad.addstr(f'{entry.name}\n', curses.color_pair(3))
        elif type(entry) == Directory:
            pad.addstr(f'{entry.name}\n', curses.color_pair(1))
        else:
            pad.addstr(f'{entry.name}\n', curses.color_pair(2))
    pad.refresh(0,0,  0,0,  num_entries, max_filename_length)
    return pad


if __name__ == '__main__':
    curses.wrapper(main)
