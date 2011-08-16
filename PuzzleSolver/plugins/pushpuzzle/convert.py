"""
Performs conversion between the original Sun style input files,
and our own type.

"""

import os

from tkinter import filedialog
from . puzzle import Puzzle

def choose_oldfile(master, directory=None):
    """Allow the user to choose a puzzle file and start in the given dir."""
    
    if directory == None:
        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "resources", "examples")
    
    filename = filedialog.askopenfilename(
        filetypes = [("Original Push Puzzle file", "screen.*")],
        initialdir=directory,
        parent = master)
    
    return filename

def from_file(file):
    """Read an old file and pump out an intermediate representation."""

    return [list(line.rstrip()) for line in file]

def to_puzzle(intermediate):
    """Take the intermediate representation and create a puzzle."""
    
    height = len(intermediate)
    width = max(len(row) for row in intermediate)
    
    p = Puzzle(height, width)
    for y, row in enumerate(intermediate):
        for x, item in enumerate(row):
            if item == "#":
                p.base.walls.add((x, y))
            elif item == "$":
                p.initial().boxes.add((x, y))
            elif item == ".":
                p.base.targets.add((x, y))
            elif item == "@":
                p.initial().player= (x, y)
    
    return p