import curses
from typing import List
from src.explorer.FileEntry import FileEntry, Directory
from src.explorer.FileExplorer import FileExplorer
from src.displays.DirectoryPad import DirectoryPad

class PadList:
    """
    Data structure for maintaining a horizontal row of directory pads.

    Attributes:

    - file_explorer : :class:`FileExplorer` --> the FileExplorer object used to read file entries
    - dir_pads : :class:`List[DirectoryPad]` --> the list of directory pads currently in use
    - current : :class:`int` --> the index of the currently selected DirectoryPad in dir_pads
    """
    def __init__(self, fe: FileExplorer) -> None:
        self.fe = fe
        self.dir_pads = []
        self.current = 0
        self._init_dir_pads()

    def traverse_up(self):
        """
        Deselect the current file in the current directory, and select the previous one
        """
        prev_selected_file = self.fe.get_selected_entry()
        new_index = self.fe.traverse_up()
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deselect_file(prev_selected_file)
        curr_dir_pad.select_at_index(new_index)

    def traverse_down(self):
        """
        Deselect the current file in the current directory, and select the next one
        """
        prev_selected_file = self.fe.get_selected_entry()
        new_index = self.fe.traverse_down()
        curr_dir_pad = self.get_current_dir_pad()
        curr_dir_pad.deselect_file(prev_selected_file)
        curr_dir_pad.select_at_index(new_index)

    def traverse_left(self):
        """
        Move into the parent directory, creating one if it doesn't exist
        """
        # TODO Implement
        return

    def traverse_right(self):
        """
        If a child directory in the current directory is selected, move into the child directory
        """
        # TODO Implement
        return

    def get_current_dir_pad(self) -> DirectoryPad:
        """
        Get the currently selected DirectoryPad
        """
        return self.dir_pads[self.current]

    def _init_dir_pads(self):
        first_dir_pad = DirectoryPad(self.fe.curr_directory)
        self.dir_pads.append(first_dir_pad)
        first_dir_pad.draw()
        first_dir_pad.select_at_index(self.fe.selected_index)
