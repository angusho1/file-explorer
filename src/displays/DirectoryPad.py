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
    - width : :class:`int` --> the total width (columns) for this directory pad, based on the longest filename in the directory
    - start_index : :class:`int` --> the row to start rendering at
    - offset : :class:`int` --> the column to start rendering at
    - max_cols: :class:`int` --> the max number of columns to render
    - render_from_left :class:`bool` --> True if the pad should be rendered to show content from left to right. If False, render columns from right to left. Default is True
    - pad --> the curses pad
    """
    def __init__(self, directory: Directory) -> None:
        self.DIR_COLOR = curses.color_pair(1)
        self.FILE_COLOR = curses.color_pair(2)
        self.SELECTED_COLOR = curses.color_pair(3)
        self.DEEP_DIR_COLOR = curses.color_pair(4)

        self.directory = directory
        self.width = self.get_width()
        self.start_index = 0
        self.offset = 0
        self.max_cols = self.width
        self.render_from_left = True
        self.pad = self._create_pad()

    def draw(self):
        """
        Render the file entries for the the current directory
        """
        self.pad.move(0, 0)
        self.pad.clear()
        for i, entry in enumerate(self._get_file_entries()):
            if type(entry) == Directory:
                self.pad.addstr(f'{entry.name}\n', self.DIR_COLOR)
            else:
                self.pad.addstr(f'{entry.name}\n', self.FILE_COLOR)
        self.drawn = True
        self.noutrefresh()

    def noutrefresh(self):
        """
        Mark the pad for refresh. curses.doUpdate() must be called afterwards for the refresh to take place.
        """
        pad_col_start = 0 if self.width == self.max_cols or self.render_from_left else self.width - self.max_cols

        # (upper-left of pad start, upper-left of window, lower-right of window)
        self.pad.noutrefresh(self.start_index, pad_col_start, 0, self.offset, curses.LINES-1, self.max_cols - 1 + self.offset)

    def render_at_col(self, col: int, render_from_left=True) -> bool:
        """
        Render the DirectoryPad at the specified column. This function will handle cases where the pad's content cannot fit entirely on the screen.

        Returns true if the pad was fully rendered

        Parameters:

        - col : :class:`int` --> the column to start rendering the pad at
        - render_from_left : :class:`bool` --> if True, render the pad's content from left to right. Default value is True
        """
        if not render_from_left: # Render at left edge of screen
            self.set_offset(0)
            self.set_render_from_left(False) 
            self.set_max_cols(col)
        else:
            self.set_offset(col)
            if col + self.width < curses.COLS:
                self.set_max_cols(self.width)
            else:
                self.set_max_cols(curses.COLS - col)    # Number of columns that the pad will get to render before hitting an edge of the screen
            self.set_render_from_left(render_from_left)
        if not self.is_drawn():
            self.draw()
        else:
            self.noutrefresh()


    def select_at_index(self, curr_index: int):
        """
        Highlight the row of the file at curr_index
        """
        # NOTE: coords for window.move methods are relative to the window's position
        self.pad.move(curr_index, 0)  # Move cursor vertically
        self.pad.chgat(self.SELECTED_COLOR)
        self._update_start_index(curr_index)
        self.noutrefresh()  # Mark for refresh

    def get_num_entries(self) -> int:
        return len(self._get_file_entries())

    def get_width(self) -> int:
        return self._get_max_filename_len() + 1

    def set_offset(self, offset: int):
        self.offset = offset

    def set_max_cols(self, max_cols: int):
        self.max_cols = max_cols

    def set_render_from_left(self, from_left: bool):
        self.render_from_left = from_left

    def deselect_file(self, curr_file: FileEntry):
        # Remove the selection highlight from the currently selected file
        if type(curr_file) == Directory:
            self.pad.chgat(self.DIR_COLOR)
        else:
            self.pad.chgat(self.FILE_COLOR)

    def deep_select_curr_file(self):
        # Apply a selection highlight to show the current file was previously selected
        self.pad.chgat(self.DEEP_DIR_COLOR)

    def is_drawn(self):
        return hasattr(self, 'drawn')

    def clear(self):
        self.pad.move(0, 0)
        self.pad.clear()
        self.noutrefresh()

    def _get_max_filename_len(self) -> int:
        longest_name_file = max(self._get_file_entries(), key=lambda x: len(x.name), default=None)
        return len(longest_name_file.name) if longest_name_file is not None else 0

    def _create_pad(self):
        # Create a new pad with width (rows) based on number of file entries and width (columns) based on the longest file name in the file entry list
        num_file_entries = self.get_num_entries()
        num_rows = num_file_entries+1 if num_file_entries >= curses.LINES else curses.LINES
        return curses.newpad(num_rows, self.width)

    def _get_file_entries(self):
        return self.directory.children

    def _update_start_index(self, new_index: int):
        # Shift the file entry list up or down if it doesn't fit entirely within the screen
        if new_index - self.start_index >= curses.LINES:
            self.start_index = new_index - curses.LINES + 1
        elif new_index < self.start_index:
            self.start_index = new_index
    