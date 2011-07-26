"""
Area for playing the Push Puzzle.

"""

import tkinter

class PlayArea(tkinter.Frame):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        tkinter.Label(self, text="Play Mode!!!").grid(sticky="nsew")

    def rewind(self):
        """Go to the beginning of the play area."""

    def next(self):
        """Go to the next state. Return whether successful."""

    def hasnext(self):
        """Do we have a next state?"""

        return False

    def prev(self):
        """Go to previous state. Returns whether successful."""

    def hasprev(self):
        """Do we have a previous state?"""

        return False
