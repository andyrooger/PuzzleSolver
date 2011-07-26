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
            raise ValueError

        self.puzzle = puzzle
        self.changecb = changecb or (lambda: None)

        self.focus_set()
        self.bind("<Key>", self.keypress)

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
                content = ("WALL" if (x,y) in self.puzzle.walls else "EMPTY")
                if self.puzzle.initial().player == (x, y):
                    content = "PLAYER"
                if (x, y) in self.puzzle.initial().boxes:
                    content = "BOX"
                target = ((x,y) in self.puzzle.targets)
                tile.config(**style.tileStyle(content, target, separated=False))
            self.buttons.append(row)

    def createTile(self, pos):
        def click():
            self.clicked(pos)
        btn = tkinter.Button(self.window, relief=tkinter.FLAT, command=click)
        return btn

    def clicked(self, pos):
        """One of the tiles has been clicked."""

        print("Clicked " + str(pos))

    def keypress(self, evt):
        """A key has been pressed."""

        CODES = {111: "UP", 116: "DOWN", 113: "LEFT", 114: "RIGHT"}

        if evt.keycode in CODES:
            print("Pressed: " + CODES[evt.keycode])

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
