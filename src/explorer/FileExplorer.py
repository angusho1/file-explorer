import os
from typing import List
from FileEntry import FileEntry, Directory

class FileExplorer:
    """
    Central object for traversing the file system and maintaining state about currently selected files and folders
    """
    def __init__(self) -> None:
        self.curr_dir_entries = self.get_curr_file_entries()
        self.selected = None

    def get_curr_file_entries(self) -> List[FileEntry]:
        """
        Get all the files and directories in the current directory
        """
        traverser = os.walk('.')
        root, dirs, files = traverser.__next__()

        results = list(map(lambda dir: Directory(dir), dirs))
        results.extend(list(map(lambda file: FileEntry(file), files)))

        return results

    def traverse_up(self):
        pass

    def traverse_down(self):
        pass
        

if __name__ == "__main__":
    fe = FileExplorer()
    entries1 = fe.get_curr_file_entries()
    print(entries1)