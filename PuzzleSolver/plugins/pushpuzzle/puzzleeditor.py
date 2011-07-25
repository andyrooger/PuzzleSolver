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
        if not isinstance(puzzle, Puzzle):
            raise ValueError # Puzzle is broken

        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loadIcons()
        self.modeselect = ButtonSelector(self)
        for mode in EDIT_MODES:
            self.modeselect.add("Edit " + mode.title(), mode, self.icons[mode])
        self.modeselect.grid(sticky="nsew", row=1, column=0)

        self.creation = CreationArea(self, puzzle.height, puzzle.width, getmode=self.modeselect.selection())
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
    def __init__(self, master, height, width, getmode=None):
        tkinter.tix.ScrolledWindow.__init__(self, master, scrollbar="auto")

        self.getmode = getmode
        for x in range(width):
            for y in range(height):
                tkinter.tix.Button(self.window, text="x").grid(
                    sticky="nsew", row=y, column=x)
