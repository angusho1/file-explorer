import os
from typing import List
from explorer.FileEntry import FileEntry, Directory

class FileExplorer:
    """
    Central object for traversing the file system and maintaining state about currently selected files and folders
    """
    def __init__(self) -> None:
        self.start = os.getcwd()
        self.curr_dir_entries = self._get_curr_file_entries()
        self.selected_index = 0

    def get_selected_entry(self) -> FileEntry:
        return self.curr_dir_entries[self.selected_index]

    def select_by_index(self, index: int) -> FileEntry:
        """
        Set the file entry at the given index as the current file entry, and return the file entry. Returns None if the index is out of bounds.
        """
        if (index < 0 or index >= len(self.curr_dir_entries)):
            return None
        else:
            self.select_by_index = index
            return self.get_selected_entry()

    def traverse_up(self) -> int:
        """
        Move upwards one selection in the current directory. Returns the index of the currently selected file entry.
        """
        if self.selected_index == 0:
            self.selected_index = len(self.curr_dir_entries) - 1
        else:
            self.selected_index -= 1
        return self.selected_index

    def traverse_down(self) -> int:
        """
        Move downwards one selection in the current directory. Returns the index of the currently selected file entry.
        """
        if self.selected_index == len(self.curr_dir_entries) - 1:
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

    def _get_curr_file_entries(self) -> List[FileEntry]:
        """
        Get all the files and directories in the current directory
        """
        traverser = os.walk('.')
        root, dirs, files = traverser.__next__()

        results = list(map(lambda dir: Directory(dir), dirs))
        results.extend(list(map(lambda file: FileEntry(file), files)))

        return results

    def _update_directory(self):
        self.curr_dir_entries = self._get_curr_file_entries()
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