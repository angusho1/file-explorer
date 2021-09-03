import curses
from typing import List
from explorer.FileEntry import FileEntry, Directory
from explorer.FileExplorer import FileExplorer


class DirectoryPad:
    def __init__(self, file_explorer: FileExplorer) -> None:
        self.DIR_COLOR = curses.color_pair(1)
        self.FILE_COLOR = curses.color_pair(2)
        self.SELECTED_COLOR = curses.color_pair(3)

        self.file_explorer = file_explorer
        self.file_entries = file_explorer.curr_dir_entries
        self.max_filename_len = self.get_max_filename_len()
        self.pad = self._create_pad()
        self.draw()
    
    def draw(self):
        cursor_coords = curses.getsyx()
        for i, entry in enumerate(self.file_entries):
            if cursor_coords[0] == i:
                self.pad.addstr(f'{entry.name}\n', self.SELECTED_COLOR)
            elif type(entry) == Directory:
                self.pad.addstr(f'{entry.name}\n', self.DIR_COLOR)
            else:
                self.pad.addstr(f'{entry.name}\n', self.FILE_COLOR)
        self.noutrefresh()

    def refresh(self):
        self.pad.refresh(0,0,  0,0, self.get_num_entries(), self.max_filename_len)

    def noutrefresh(self):
        self.pad.noutrefresh(0,0,  0,0, self.get_num_entries(), self.max_filename_len)

    def traverse_down(self):
        cursor_coords = curses.getsyx()
        self.deselect_curr_file()
        self.pad.move(cursor_coords[0]+1, cursor_coords[1])
        self.pad.chgat(self.SELECTED_COLOR)
        self.noutrefresh()

    def traverse_up(self):
        cursor_coords = curses.getsyx()
        self.deselect_curr_file()
        self.pad.move(cursor_coords[0]-1, cursor_coords[1])
        self.pad.chgat(self.SELECTED_COLOR)
        self.noutrefresh()

    def get_num_entries(self) -> int:
        return len(self.file_entries)

    def get_max_filename_len(self) -> int:
        return len(max(self.file_entries, key=lambda x: len(x.name)).name)

    def deselect_curr_file(self):
        curr_file = self.file_explorer.get_selected_entry()
        if type(curr_file) == Directory:
            self.pad.chgat(self.DIR_COLOR)
        else:
            self.pad.chgat(self.FILE_COLOR)

    def go_to_start(self):
        self.pad.move(0,0)
        self.noutrefresh()

    def _create_pad(self):
        num_entries = self.get_num_entries()
        max_filename_length = self.max_filename_len
        return curses.newpad(num_entries+1, max_filename_length+1)



    