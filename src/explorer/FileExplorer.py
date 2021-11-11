import os
from typing import List
from src.explorer.FileEntry import FileEntry, Directory
import pyperclip

class FileExplorer:
    """
    Central object for traversing the file system and maintaining state about currently selected files and folders
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
        """
        if (index < 0 or index >= len(self.curr_directory.children)):
            return None
        else:
            self.select_by_index = index
            return self.get_selected_entry()

    def traverse_up(self) -> int:
        """
        Move upwards one selection in the current directory. Returns the index of the currently selected file entry.
        """
        if self.selected_index == 0:
            self.selected_index = len(self.curr_directory.children) - 1
        else:
            self.selected_index -= 1
        return self.selected_index

    def traverse_down(self) -> int:
        """
        Move downwards one selection in the current directory. Returns the index of the currently selected file entry.
        """
        if self.selected_index == len(self.curr_directory.children) - 1:
            self.selected_index = 0
        else:
            self.selected_index += 1
        return self.selected_index

    def traverse_left(self):
        """
        Move backwards to the parent directory
        """
        os.chdir('../')
        self._update_directory()

    def traverse_right(self):
        """
        Move into the currently selected directory
        """
        selection = self.get_selected_entry()
        if type(selection) != Directory:
            raise Exception('Cannot traverse a file')
        os.chdir(selection.name)
        self._update_directory()

    def copy_path(self) -> Directory:
        """
        Copy the relative path of the currently selected directory
        """
        selection = self.get_selected_entry()
        if type(selection) == Directory:
            rel_path = os.path.relpath(selection.name, self.start)
            pyperclip.copy(f'cd {rel_path}')
            return selection
        return None

    def _get_curr_directory(self) -> Directory:
        """
        Get the current Directory object, creating it if it doesn't exist
        """
        curr_dir = Directory(*os.path.split(os.getcwd()))
        traverser = os.walk('.')
        root, dirs, files = traverser.__next__()

        results = list(map(lambda dir: Directory(curr_dir.path, dir), dirs))
        results.extend(list(map(lambda file: FileEntry(curr_dir.path, file), files)))
        curr_dir.set_children(results)
        return curr_dir

    def get_curr_file_entries(self) -> List[FileEntry]:
        return self.curr_directory.children

    def _update_directory(self):
        self.curr_directory = self._get_curr_directory()
        self.selected_index = 0

if __name__ == "__main__":
    fe = FileExplorer()
    test1 = fe.get_selected_entry()
    fe.traverse_up()
    test2 = fe.get_selected_entry()
    fe.traverse_up()
    test3 = fe.get_selected_entry()
    # fe.traverse_right()
    # test4 = fe.get_selected_entry()
    pass