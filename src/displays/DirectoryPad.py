import curses
from typing import List
from src.explorer.FileEntry import FileEntry, Directory
from src.explorer.FileExplorer import FileExplorer
import pyperclip


class DirectoryPad:
    def __init__(self, file_explorer: FileExplorer) -> None:
        self.DIR_COLOR = curses.color_pair(1)
        self.FILE_COLOR = curses.color_pair(2)
        self.SELECTED_COLOR = curses.color_pair(3)

        self.file_explorer = file_explorer
        self.file_entries = file_explorer.get_curr_file_entries()
        self.max_filename_len = self.get_max_filename_len()
        self.pad = self._create_pad()
        self.draw()
    
    def draw(self):
        """
        Render the file entries for the the current directory
        """
        cursor_coords = curses.getsyx()
        for i, entry in enumerate(self.file_entries):
            if type(entry) == Directory:
                self.pad.addstr(f'{entry.name}\n', self.DIR_COLOR)
            else:
                self.pad.addstr(f'{entry.name}\n', self.FILE_COLOR)
        self.noutrefresh()

    def refresh(self):
        self.pad.refresh(0,0,  0,0, self.get_num_entries(), self.max_filename_len)

    def noutrefresh(self):
        """
        Mark the pad for refresh. curses.doUpdate() must be called afterwards for the refresh to take place.
        """
        self.pad.noutrefresh(0,0,  0,0, self.get_num_entries(), self.max_filename_len)

    def traverse_down(self):
        """
        Deselect the current highlighted file entry, move the cursor to the following entry, and highlight it.
        """
        cursor_coords = curses.getsyx()
        self.deselect_curr_file()
        new_index = self.file_explorer.traverse_down()
        self.pad.move(new_index, cursor_coords[1])
        self.pad.chgat(self.SELECTED_COLOR)
        self.noutrefresh()

    def traverse_up(self):
        """
        Deselect the current highlighted file entry, move the cursor to the previous entry, and highlight it.
        """
        cursor_coords = curses.getsyx()
        self.deselect_curr_file()
        new_index = self.file_explorer.traverse_up()
        self.pad.move(new_index, cursor_coords[1])
        self.pad.chgat(self.SELECTED_COLOR)
        self.noutrefresh()

    def get_num_entries(self) -> int:
        return len(self.file_entries)

    def get_max_filename_len(self) -> int:
        return len(max(self.file_entries, key=lambda x: len(x.name)).name)

    def select_file(self, row: int):
        selected_file = self.file_explorer.select_by_index(row)
        if selected_file is None:
            pass
        else:
            self.pad.move(row, 0)
            self.pad.chgat(self.SELECTED_COLOR)
            self.noutrefresh()

    def deselect_curr_file(self):
        curr_file = self.file_explorer.get_selected_entry()
        if type(curr_file) == Directory:
            self.pad.chgat(self.DIR_COLOR)
        else:
            self.pad.chgat(self.FILE_COLOR)

    def _create_pad(self):
        num_entries = self.get_num_entries()
        max_filename_length = self.max_filename_len
        return curses.newpad(num_entries+1, max_filename_length+1)



    