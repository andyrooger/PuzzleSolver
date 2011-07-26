"""
Area for playing the Push Puzzle.

"""

import tkinter
import tkinter.tix

from . import style
from . puzzle import Puzzle

class PlayArea(tkinter.tix.ScrolledWindow):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle, changecb=None):
        tkinter.tix.ScrolledWindow.__init__(self, master, scrollbar="auto")

        if not isinstance(puzzle, Puzzle) or not puzzle.valid():
            return ValueError

        self.puzzle = puzzle
        self.changecb = changecb or (lambda: None)

        self.initialSetup()

    def initialSetup(self):
        """Set up the parts of the view that are constant."""

        self.buttons = []
        for y in range(self.puzzle.height):
            row = []
            for x in range(self.puzzle.width):
                tile = self.createTile((x,y))
                row.append(tile)
                tile.grid(sticky="nsew", row=y, column=x)
                wall = ((x,y) in self.puzzle.walls)
                target = ((x,y) in self.puzzle.targets)
                tile.config(**style.tileStyle("WALL" if wall else "EMPTY", target, separated=False))
            self.buttons.append(row)


    def createTile(self, pos):
        def click():
            self.clicked(pos)
        btn = tkinter.Button(self.window, relief=tkinter.FLAT, command=click)
        btn.config(**style.tileStyle("EMPTY", False, separated=False))
        return btn

    def clicked(self, pos):
        """One of the tiles has been clicked."""

        print("Clicked " + str(pos))

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
