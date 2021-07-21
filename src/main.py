#!/usr/bin/env python3

import os
from typing import List

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def get_files(dir):
    items = os.listdir(dir)
    res = []
    for f in items:
        if os.path.isfile(f):
            res.append({ 'type': 'file', 'name': f })
        else:
            res.append({ 'type': 'folder', 'name': f })
    return res


def print_files(files: List[dict]):
    for f in files:
        color = bcolors.OKGREEN if f.get('type') == 'file' else bcolors.OKBLUE
        print(f"{color}{f.get('name')}{bcolors.ENDC}")


if __name__ == '__main__':
    files = get_files('./')
    print_files(files)