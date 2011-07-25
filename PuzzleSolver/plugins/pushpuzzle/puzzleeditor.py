"""
Editor frame for push puzzle.

"""

import os.path
import tkinter
import tkinter.tix

from . puzzle import Puzzle
from solver.utility.buttonselector import ButtonSelector

EDIT_MODES = ["EMPTY", "WALL", "TARGET", "BOX", "PLAYER"]

class PuzzleEditor(tkinter.Frame):
    def __init__(self, master, puzzle):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loadIcons()
        self.modeselect = ButtonSelector(self)
        for mode in EDIT_MODES:
            self.modeselect.add("Edit " + mode.title(), mode, self.icons[mode])
        self.modeselect.grid(sticky="nsew", row=1, column=0)

        self.creation = CreationArea(self, puzzle, getmode=self.modeselect.selection)
        self.creation.grid(sticky="nsew", row=0, column=0)


    def loadIcons(self):
        """Load and store all necessary icons."""

        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "resources", "images")

        self.icons = {
            mode: tkinter.PhotoImage(file=os.path.join(directory, mode.lower()+".gif"))
            for mode in EDIT_MODES
        }

    def getPuzzle(self): return None
    def saved(self): pass
    def changed(self): return False

class CreationArea(tkinter.tix.ScrolledWindow):
    """Creation area, containing scrolled grid of tiles."""

    def __init__(self, master, puzzle, getmode=None):
        tkinter.tix.ScrolledWindow.__init__(self, master, scrollbar="auto")

        if not isinstance(puzzle, Puzzle):
            raise ValueError("Type is not a puzzle: " + puzzle.__class__.__name__) # Puzzle is broken

        self.getmode = getmode
        self.buttons = []
        for x in range(puzzle.width):
            row = []
            for y in range(puzzle.height):
                pos = (x, y)
                p = PuzzleTile(self.window,
                               wall = (pos in puzzle.walls),
                               target = (pos in puzzle.targets),
                               box = (pos in puzzle.initial().boxes),
                               player = (pos == puzzle.initial().player),
                               clicked=self.click)
                row.append(p)
                p.grid(sticky="nsew", row=y, column=x)
            self.buttons.append(row)

    def click(self, tile):
        """On click callback for clicks on PuzzleTiles."""

        pass

class PuzzleTile(tkinter.Button):
    """Single tile in the puzzle."""

    def __init__(self, master, wall=False, target=False, box=False, player=False, clicked=None):
        tkinter.Button.__init__(self, master, text="x", command=self.click)
        self.clicked = clicked
        # could raise and propagate valueerror
        self._content = self.chooseContent(wall, target, box, player)

    def chooseContent(self, wall, target, box, player):
        """Decide which of the content we should display."""

        if sum(1 for x in [wall, target, box, player] if x) > 1:
            raise ValueError("Cannot display this puzzle.")

        if wall:
            return "WALL"
        elif target:
            return "TARGET"
        elif box:
            return "BOX"
        elif player:
            return "PLAYER"
        else:
            return "EMPTY"

    def content(self):
        return self._content

    def click(self):
        self.clicked(self)
