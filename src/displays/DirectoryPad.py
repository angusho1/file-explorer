import curses
from typing import List
from src.explorer.FileEntry import FileEntry, Directory
from src.explorer.FileExplorer import FileExplorer
import pyperclip


class DirectoryPad:
    """
    A view of the files in a directory built using a curses pad.

    Attributes:

    - file_explorer : :class:`FileExplorer` --> the FileExplorer object used to read file entries for the current directory
    - directory : :class:`Directory` --> the directory being rendered in this view
    - max_filename_len : :class:`int` --> the length of the longest filename in the file entries list for this directory
    - start_index : :class:`int` --> the row to start rendering at
    - pad --> the curses pad
    """
    def __init__(self, directory: Directory) -> None:
        self.DIR_COLOR = curses.color_pair(1)
        self.FILE_COLOR = curses.color_pair(2)
        self.SELECTED_COLOR = curses.color_pair(3)

        self.directory = directory
        self.max_filename_len = self.get_max_filename_len()
        self.start_index = 0
        self.pad = self._create_pad()

    def draw(self):
        """
        Render the file entries for the the current directory
        """
        cursor_coords = curses.getsyx()
        for i, entry in enumerate(self._get_file_entries()):
            if type(entry) == Directory:
                self.pad.addstr(f'{entry.name}\n', self.DIR_COLOR)
            else:
                self.pad.addstr(f'{entry.name}\n', self.FILE_COLOR)
        self.noutrefresh()

    def noutrefresh(self):
        """
        Mark the pad for refresh. curses.doUpdate() must be called afterwards for the refresh to
        take place.
        """
        total_entries = self.get_num_entries()
        num_rows_to_display = total_entries-1 if total_entries <= curses.LINES else curses.LINES-1
        # (upper-left of pad start, upper-left of window, lower-right of window)
        self.pad.noutrefresh(self.start_index,0,  0,0, num_rows_to_display, self.max_filename_len)

    def select_at_index(self, curr_index: int):
        """
        Highlight the row of the file at curr_index
        """
        cursor_coords = curses.getsyx()
        self.pad.move(curr_index, cursor_coords[1])  # Move cursor vertically
        self.pad.chgat(self.SELECTED_COLOR)
        self._update_start_index(curr_index)
        self.noutrefresh()  # Mark for refresh

    def get_num_entries(self) -> int:
        return len(self._get_file_entries())

    def get_max_filename_len(self) -> int:
        return len(max(self._get_file_entries(), key=lambda x: len(x.name)).name)

    def deselect_file(self, curr_file: FileEntry):
        # Remove the selection highlight from the currently selected file
        if type(curr_file) == Directory:
            self.pad.chgat(self.DIR_COLOR)
        else:
            self.pad.chgat(self.FILE_COLOR)

    def _create_pad(self):
        # Create a new pad with size based on number of file entries and the longest file name in
        # the file entry list
        num_entries = self.get_num_entries()
        max_filename_length = self.max_filename_len
        return curses.newpad(num_entries+1, max_filename_length+1)

    def _get_file_entries(self):
        return self.directory.children

    def _update_start_index(self, new_index: int):
        # Shift the file entry list up or down if it doesn't fit entirely within the screen
        if new_index - self.start_index >= curses.LINES:
            self.start_index = new_index - curses.LINES + 1
        elif new_index < self.start_index:
            self.start_index = new_index
    