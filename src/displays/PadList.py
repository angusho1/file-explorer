from typing import List
from src.explorer.FileEntry import FileEntry, Directory
from src.explorer.FileExplorer import FileExplorer
from src.displays.DirectoryPad import DirectoryPad
import curses

class PadList:
    """
    Data structure for maintaining a horizontal row of directory pads.

    Attributes:

    - file_explorer : :class:`FileExplorer` --> the FileExplorer object used to read file entries
    - dir_pads : :class:`List[DirectoryPad]` --> the list of directory pads currently in use
    - current : :class:`int` --> the index of the currently selected DirectoryPad in dir_pads
    - leftmost_index : :class:`int` --> the index of the leftmost pad that is visible on the screen
    - rightmost_index : :class:`int` --> the index of the rightmost pad that is visible on the screen
    """
    def __init__(self, fe: FileExplorer) -> None:
        self.fe = fe
        self.dir_pads = []
        self.current = 0
        self.leftmost_index = 0
        self.rightmost_index = 0
        self.left_padding = 0
        self.right_padding = 0
        self.render_ltr = True
        self._init_dir_pads()
        self.refresh()

    def traverse_up(self):
        """
        Deselect the current file in the current directory, and select the previous one
        """
        prev_selected_file = self.fe.get_selected_entry()
        new_index = self.fe.traverse_up()
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deselect_file(prev_selected_file)
        curr_dir_pad.select_at_index(new_index)
        self._clear_peek_directory()
        self._init_child_dir()
        self.refresh(render_from_current=True)

    def traverse_down(self):
        """
        Deselect the current file in the current directory, and select the next one
        """
        prev_selected_file = self.fe.get_selected_entry()
        new_index = self.fe.traverse_down()
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deselect_file(prev_selected_file)
        curr_dir_pad.select_at_index(new_index)
        self._clear_peek_directory()
        self._init_child_dir()
        self.refresh(render_from_current=True)

    def traverse_left(self):
        """
        Move into the parent directory, creating one if it doesn't exist
        """
        try:
            self.fe.traverse_left()
        except:
            return
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deep_select_curr_file()
        curr_dir_pad.noutrefresh()
        if self.current == 0:
            new_dir = DirectoryPad(self.fe.curr_directory)
            self.dir_pads.insert(0, new_dir)
        else:
            self.current -= 1
        self.refresh()

    def traverse_right(self):
        """
        If a child directory in the current directory is selected, move into the child directory
        """
        curr_selection = self.fe.get_selected_entry()
        if type(curr_selection) != Directory:
            return
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deep_select_curr_file()
        self.fe.traverse_right()
        self.current += 1
        if self.current == len(self.dir_pads)-1:
            self._init_child_dir()
        self.refresh()

    def get_current_dir_pad(self) -> DirectoryPad:
        """
        Get the currently selected DirectoryPad
        """
        return self.dir_pads[self.current]

    def refresh(self, render_from_current=False):
        """
        Update the position of all DirectoryPads that can be visible on screen, and mark each one for refresh

        Parameters:

        - render_from_current : :class:`bool` --> if True, only re-render DirectoryPads to the right of the current one, unless the pads need to be shifted left. Default value is False
        """
        current_pad: DirectoryPad = self.get_current_dir_pad()
        curr_pad_contains_child = current_pad.directory.get_curr_selected_child().contains_child_dirs()

        # Index of the furthest-right DirectoryPad that must be shown on screen fully
        shown_dp_index = self.current + 1 if curr_pad_contains_child else self.current

        offset = current_pad.offset if render_from_current else self.left_padding
        offset = 0 if self.current < self.leftmost_index else offset
        i = self.current if render_from_current or self.current < self.leftmost_index else self.leftmost_index  # Set leftmost pad to start rendering from
        dp: DirectoryPad
        while i < shown_dp_index:
            dp = self.dir_pads[i]
            offset += dp.width
            i += 1
        
        shown_dp: DirectoryPad = self.dir_pads[shown_dp_index]
        if offset + shown_dp.width > curses.COLS:
            # Need to render pads from the right edge of the screen to the left
            start_at = self.current + 1 if curr_pad_contains_child else self.current
            self._refresh_rtl(start_at)
        else:
            self.leftmost_index = self.current if self.current < self.leftmost_index else self.leftmost_index   # Index of furthest left pad visible on the screen
            self._refresh_ltr(render_from_current)
    
    def _refresh_ltr(self, render_from_current=False):
        dp: DirectoryPad
        i = self.current if render_from_current else self.leftmost_index
        offset = self.get_current_dir_pad().offset if render_from_current else 0
        while i < len(self.dir_pads) and offset < curses.COLS:
            dp = self.dir_pads[i]
            dp.render_at_col(offset)    # Render pad at specified offset
            if i == self.current:   # Highlight currently selected file
                dp.select_at_index(self.fe.selected_index)
            offset += dp.width
            i += 1

        self.left_padding = self.left_padding if render_from_current else 0
        self.rightmost_index = i-1  # Index of the last pad to be rendered on screen
        self.right_padding = self.dir_pads[i-1].max_cols

    def _refresh_rtl(self, start: int):
        if start >= len(self.dir_pads):
            return
        dp: DirectoryPad = self.dir_pads[start]
        i = start
        offset = curses.COLS
        while i >= 0 and offset >= 0:
            dp = self.dir_pads[i]
            offset -= dp.width
            col = offset + dp.width if offset < 0 else offset
            dp.render_at_col(col, render_from_left=False if offset < 0 else True)
            if i == self.current:
                dp.select_at_index(self.fe.selected_index)
            i -= 1

        self.leftmost_index = i+1

    def _clear_peek_directory(self):
        while len(self.dir_pads) > self.current + 1:
            prev_child_dir_pad = self.dir_pads.pop()
            prev_child_dir_pad.clear()
            self.rightmost_index -= 1

    def _init_dir_pads(self):
        # Create the first directory pad and highlight the first entry
        # Then, create the first child directory pad
        first_dir_pad = DirectoryPad(self.fe.curr_directory)
        self.dir_pads.append(first_dir_pad)
        self._init_child_dir()

    def _init_child_dir(self):
        # If the currently selected file is a directory, show a preview of it to the right
        is_dir = self.fe.peek_right()
        if is_dir:
            selected_dir = self.fe.get_selected_entry()
            peek_dir_pad = DirectoryPad(selected_dir)
            self.dir_pads.append(peek_dir_pad)
