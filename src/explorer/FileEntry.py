from __future__ import annotations
from typing import List
import os

class FileEntry:
    """
    A file or directory in the file system.

    Attributes:

    - dir : :class:`str` --> the path of the directory that contains the file
    - name : :class:`str` --> the name of the file
    - parent : :class:`Directory` --> the Directory object representing the file's parent directory
    """
    def __init__(self, dir: str, name: str, parent: Directory = None) -> None:
        self.dir = dir
        self.name = name
        self.parent = parent

    def set_parent(self, parent: Directory) -> None:
        """
        Sets the parent directory for this file entry.

        Parameters:

        - parent : :class:`Directory` --> the Directory object representing the file's parent directory
        """
        self.parent = parent

    def get_path(self) -> str:
        """
        Returns the full path of the file entry.
        """
        return os.path.join(self.dir, self.name)

class Directory(FileEntry):
    """
    A directory in the file system.

    - Attributes:

    - children : :class:`List[FileEntry]` --> a list of files contained in this directory
    - selected_child_index :class:`int` --> index of the currently selected child
    """
    def __init__(self, dir: str = None, name: str = None, parent: Directory = None) -> None:
        if dir is None or name is None or parent is None:
            super().__init__(*os.path.split(os.getcwd()))
        else:
            super().__init__(dir, name, parent)
        self.children = None
        self.selected_child_index = 0

    def _set_children(self, children: List[FileEntry]) -> None:
        self.children = children

    def get_child(self, index: int) -> FileEntry:
        return self.children[index]
    
    def select_child(self, index: int):
        self.selected_child_index = index

    def get_curr_selected_child_index(self):
        return self.selected_child_index

    def get_curr_selected_child(self):
        return self.children[self.selected_child_index]

    def traverse_contents(self, existing_child: FileEntry = None) -> None:
        """
        Create FileEntry or Directory objects for each file entry in the directory, and save them
        as children of the directory. If existing_child is passed in and it matches a file entry
        in this directory, it will be used directly in place of a new FileEntry object.

        Parameters:

        - existing_child : :class:`FileEntry` --> an existing FileEntry object that represents a
        file entry inside this directory
        """
        full_path = self.get_path()
        traverser = os.walk(full_path)
        root, dirs, files = traverser.__next__()

        if existing_child is None:
            results = list(map(lambda dir: Directory(full_path, dir, self), dirs))
        else:
            results = list(map(lambda dir: create_dir_child(full_path, dir, self, existing_child), dirs))
        results.extend(list(map(lambda file: FileEntry(full_path, file, self), files)))
        self._set_children(results)

def create_dir_child(dir, name, parent: Directory, existing_child: FileEntry) -> Directory:
    if os.path.join(dir, name) == existing_child.get_path():
        existing_child.set_parent(parent)
        return existing_child
    else:
        return Directory(dir, name, parent)