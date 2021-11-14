from __future__ import annotations
import os

class FileEntry:
    def __init__(self, dir: str, name: str, parent: Directory = None) -> None:
        self.dir = dir
        self.name = name
        self.path = os.path.join(dir, name)
        self.parent = parent

    def set_parent(self, parent: Directory) -> None:
        self.parent = parent

class Directory(FileEntry):
    def __init__(self, dir: str = None, name: str = None, parent: Directory = None) -> None:
        if dir is None or name is None or parent is None:
            super().__init__(*os.path.split(os.getcwd()))
        else:
            super().__init__(dir, name, parent)

    def set_children(self, children: List[FileEntry]) -> None:
        self.children = children

    def get_child(self, index: int) -> FileEntry:
        return self.children[index]

    def traverse_contents(self, existing_child: FileEntry = None) -> None:
        traverser = os.walk(self.path)
        root, dirs, files = traverser.__next__()

        if existing_child is None:
            results = list(map(lambda dir: Directory(self.path, dir, self), dirs))
        else:
            results = list(map(lambda dir: create_dir_child(self.path, dir, self, existing_child), dirs))
        results.extend(list(map(lambda file: FileEntry(self.path, file, self), files)))
        self.set_children(results)

def create_dir_child(dir, name, parent: Directory, existing_child: FileEntry) -> Directory:
    if os.path.join(dir, name) == existing_child.path:
        existing_child.set_parent(parent)
        return existing_child
    else:
        return Directory(dir, name, parent)