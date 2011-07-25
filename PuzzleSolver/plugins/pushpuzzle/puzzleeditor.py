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

        creationicons = {"PLAYER": self.icons["PLAYER"],
                         "BOX": self.icons["BOX"],
                         "BLANK": self.blank}
        self.creation = CreationArea(self, puzzle, icons=creationicons, getmode=self.modeselect.selection)
        self.creation.grid(sticky="nsew", row=0, column=0)

    def loadIcons(self):
        """Load and store all necessary icons."""

        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "resources", "images")

        self.icons = {
            mode: tkinter.PhotoImage(file=os.path.join(directory, mode.lower()+".gif"))
            for mode in EDIT_MODES
        }
        self.blank = tkinter.PhotoImage(file=os.path.join(directory, "blank.gif"))

    def getPuzzle(self): return None
    def saved(self): pass
    def changed(self): return False

class CreationArea(tkinter.tix.ScrolledWindow):
    """Creation area, containing scrolled grid of tiles."""

    def __init__(self, master, puzzle, icons=None, getmode=None):
        tkinter.tix.ScrolledWindow.__init__(self, master, scrollbar="auto")

        if not isinstance(puzzle, Puzzle):
            raise ValueError("Type is not a puzzle: " + puzzle.__class__.__name__) # Puzzle is broken

        self.getmode = getmode
        self.buttons = []
        for x in range(puzzle.width):
            row = []
            for y in range(puzzle.height):
                pos = (x, y)
                p = PuzzleTile(self.window, icons, clicked=self.click)
                row.append(p)
                p.grid(sticky="nsew", row=y, column=x)
            self.buttons.append(row)
        self.setContent(puzzle)

    def setContent(self, puzzle):
        """Tell each tile what their content should be."""

        for x,y in puzzle.walls:
            self.buttons[y][x].content("WALL")
        for x,y in puzzle.targets:
            self.buttons[y][x].target(True)
        for x,y in puzzle.initial().boxes:
            self.buttons[y][x].content("BOX")
        try:
            x,y = puzzle.initial().player
            self.buttons[y][x].content("PLAYER")
        except TypeError:
            pass # No player

    def click(self, tile):
        """On click callback for clicks on PuzzleTiles."""

        pass

class PuzzleTile(tkinter.Button):
    """Single tile in the puzzle."""

    def __init__(self, master, icons, clicked=None):
        tkinter.Button.__init__(self, master, relief="flat", command=self.click)
        self.icons = icons
        self.clicked = clicked
        # could raise and propagate valueerror
        self.content("EMPTY", noupdate=True)
        self.target(False, noupdate=True)
        self.appearance()

    def target(self, t = None, noupdate=False):
        if t != None:
            self._target = t
            noupdate or self.appearance()
        return self._target

    def content(self, c = None, noupdate=False):
        if c != None:
            self._content = c
            noupdate or self.appearance()
        return self._content

    def appearance(self):
        """Set up appearance."""

        bg = "blue" if self.content() == "WALL" else "white"
        icon = self.icons.get(self.content(), self.icons["BLANK"])
        hbg = "red" if self.target() else "black"
        self.config(bg=bg, image=icon, highlightbackground=hbg, highlightthickness=1)

    def click(self):
        self.clicked(self)
