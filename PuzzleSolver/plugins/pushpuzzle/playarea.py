"""
Area for playing the Push Puzzle.

"""

import tkinter

from . puzzle import Puzzle

class PlayArea(tkinter.Frame):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle, changecb=None):
        tkinter.Frame.__init__(self, master)

        if not isinstance(puzzle, Puzzle) or not puzzle.valid():
            return ValueError

        self.puzzle = puzzle
        self.changecb = changecb or (lambda: None)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        tkinter.Label(self, text="Play Mode!!!").grid(sticky="nsew")

    def rewind(self):
        """Go to the beginning of the play area."""

        self.puzzle.cursor(0)

    def next(self):
        """Go to the next state. Return whether successful."""

        try:
            self.puzzle.cursor(self.puzzle.cursor()+1)
            return True
        except IndexError:
            return False

    def hasnext(self):
        """Do we have a next state?"""

        return self.puzzle.cursor()+1 < len(self.puzzle)

    def prev(self):
        """Go to previous state. Returns whether successful."""

        try:
            self.puzzle.cursor(self.puzzle.cursor()-1)
            return True
        except IndexError:
            return False

    def hasprev(self):
        """Do we have a previous state?"""

        return self.puzzle.cursor() > 0
