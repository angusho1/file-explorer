import os, subprocess, platform
from typing import List
from src.explorer.FileEntry import FileEntry, Directory
import pyperclip

class FileExplorer:
    """
    Central class for traversing the file system and maintaining state about currently selected
    files and folders

    Attributes:

    - start : :class:`str` --> the absolute file path for the directory upon initialization
    - curr_directory : :class:`Directory` --> the current directory the program is running in
    - selected_index : :class:`int` --> index of the currently selected file entry, inside the
    curr_directory
    """
    def __init__(self) -> None:
        self.start = os.getcwd()
        self.curr_directory = self._get_curr_directory()
        self.selected_index = 0

    def get_selected_entry(self) -> FileEntry:
        return self.curr_directory.get_child(self.selected_index)

    def select_by_index(self, index: int) -> FileEntry:
        """
        Set the file entry at the given index as the current file entry, and return the file entry. Returns None if the index is out of bounds.

        Parameters:

        - index: :class:`int` --> the index of the file entry to select
        """
        if (index < 0 or index >= len(self.curr_directory.children)):
            return None
        else:
            self.selected_index = index
            self.curr_directory.select_child(self.selected_index)
            return self.get_selected_entry()

    def traverse_up(self) -> int:
        """
        Move upwards one selection in the current directory. Returns the index of the currently
        selected file entry.
        """
        if self.selected_index == 0:
            self.selected_index = len(self.curr_directory.children) - 1
        else:
            self.selected_index -= 1
        self.curr_directory.select_child(self.selected_index)
        return self.selected_index

    def traverse_down(self) -> int:
        """
        Move downwards one selection in the current directory. Returns the index of the currently
        selected file entry.
        """
        if self.selected_index == len(self.curr_directory.children) - 1:
            self.selected_index = 0
        else:
            self.selected_index += 1
        self.curr_directory.select_child(self.selected_index)
        return self.selected_index

    def traverse_left(self):
        """
        Move backwards to the parent directory
        """
        if self.curr_directory.name == '':
            raise Exception('Cannot traverse left on root directory')

        current_dir = self.curr_directory
        current_dir.select_child(self.selected_index) # Maintain history of selected child
        os.chdir('../')
        if self.curr_directory.parent is None:
            parent_dir = Directory()
            parent_dir.traverse_contents(current_dir)
            self.curr_directory = parent_dir
        else:
            self.curr_directory = self.curr_directory.parent
        self.selected_index = self.curr_directory.children.index(current_dir) # TODO: Use a faster method than index()

    def traverse_right(self) -> int:
        """
        Move into the currently selected directory

        Returns the index of the currently selected file entry.

        Raises an exception if the current selection is not a directory
        """
        selection = self.get_selected_entry()
        parent = self.curr_directory

        if type(selection) != Directory:
            raise Exception('Cannot traverse a file')
        os.chdir(selection.name)
        if selection.parent is None:
            selection.set_parent(parent)
        self.curr_directory = selection
        if self.curr_directory.children == None:
            self.curr_directory.traverse_contents()
        self.selected_index = self.curr_directory.get_curr_selected_child_index()
        return self.selected_index

    def peek_right(self) -> bool:
        """
        If the currently selected file entry is a directory, parse it using the FileExplorer object.

        Returns true if a directory was parsed, false otherwise
        """
        if len(self.curr_directory.children) == 0:
            return False
        selection = self.get_selected_entry()
        parent = self.curr_directory

        if type(selection) != Directory:
            return False
        os.chdir(selection.name)
        if selection.parent is None:
            selection.set_parent(parent)
        selection.traverse_contents()
        os.chdir('../')
        return True

    def copy_path(self) -> Directory:
        """
        Copy the relative path of the currently selected directory
        """
        selection = self.get_selected_entry()
        if type(selection) == Directory:
            rel_path = os.path.relpath(selection.name, self.start)
            escaped_path = rel_path.replace(' ', '\ ')
            pyperclip.copy(f'cd {escaped_path}')
            return selection
        return None

    def open_file(self):
        """
        Open file using default OS application
        """
        # Ref: https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
        selection = self.get_selected_entry()
        if type(selection) != Directory:
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', selection.name))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(selection.name)
            else:                                   # linux variants
                subprocess.call(('xdg-open', selection.name))

    def _get_curr_directory(self) -> Directory:
        # Get the current Directory object, creating it if it doesn't exist
        if not hasattr(self, 'curr_directory') or self.curr_directory.path != os.getcwd():
            curr_dir = Directory()
            curr_dir.traverse_contents()
            return curr_dir
        else:
            return self.curr_directory

    def get_curr_file_entries(self) -> List[FileEntry]:
        """
        Returns the list of file entries in the current directory
        """
        return self.curr_directory.children

if __name__ == "__main__":
    fe = FileExplorer()
    fe.traverse_right()
    fe.traverse_left()
    fe.traverse_left()
    fe.traverse_left()
    pass