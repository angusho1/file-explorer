from __future__ import annotations
import os

class FileEntry:
    def __init__(self, dir: str, name: str) -> None:
        self.dir = dir
        self.name = name
        self.path = os.path.join(dir, name)
        self.parent = None

    def set_parent(self, file_entry: FileEntry) -> None:
        self.parent = file_entry

class Directory(FileEntry):
    def __init__(self, dir: str, name: str) -> None:
        super().__init__(dir, name)
        self.children = []

    def set_children(self, children: List[FileEntry]) -> None:
        self.children = children

    def get_child(self, index: int) -> FileEntry:
        return self.children[index]

