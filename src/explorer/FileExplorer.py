import os
from typing import List
from FileEntry import FileEntry, Directory

class FileExplorer:
    """
    Central object for traversing the file system and maintaining state about currently selected files and folders
    """
    def __init__(self) -> None:
        self.start = os.getcwd()
        self.curr_dir_entries = self.get_curr_file_entries()
        self.selected_index = 0
        self.num_entries = len(self.curr_dir_entries)

    def get_curr_file_entries(self) -> List[FileEntry]:
        """
        Get all the files and directories in the current directory
        """
        traverser = os.walk('.')
        root, dirs, files = traverser.__next__()

        results = list(map(lambda dir: Directory(dir), dirs))
        results.extend(list(map(lambda file: FileEntry(file), files)))

        return results

    def get_selected_entry(self) -> FileEntry:
        return self.curr_dir_entries[self.selected_index]

    def traverse_up(self):
        """
        Move upwards one selection in the current directory
        """
        if self.selected_index == 0:
            self.selected_index = self.num_entries - 1
        else:
            self.selected_index -= 1

    def traverse_down(self):
        """
        Move downwards one selection in the current directory
        """
        if self.selected_index == self.num_entries - 1:
            self.selected_index = 0
        else:
            self.selected_index += 1

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

    def _update_directory(self):
        self.curr_dir_entries = self.get_curr_file_entries()
        self.selected_index = 0
        self.num_entries = len(self.curr_dir_entries)

if __name__ == "__main__":
    fe = FileExplorer()
    test1 = fe.get_selected_entry()
    fe.traverse_up()
    test2 = fe.get_selected_entry()
    fe.traverse_up()
    test3 = fe.get_selected_entry()
    fe.traverse_right()
    test4 = fe.get_selected_entry()
    pass