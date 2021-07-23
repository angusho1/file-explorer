import os

class FileEntry:
    def __init__(self, file: str) -> None:
        self.name = file

class Directory(FileEntry):
    def __init__(self, dir: str) -> None:
        super().__init__(dir)
        self.children = []
    

