"""
Editor frame for push puzzle.

"""

import os.path
import tkinter

from . puzzle import Puzzle
from solver.utility.buttonselector import ButtonSelector

EDIT_MODES = ["EMPTY", "WALL", "TARGET", "BOX", "PLAYER"]

class PuzzleEditor(tkinter.Frame):
    def __init__(self, master, puzzle):
        if not isinstance(puzzle, Puzzle):
            raise ValueError # Puzzle is broken

        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Height: "+str(puzzle.height)).grid(sticky="nsew")
        tkinter.Label(self, text="Width: "+str(puzzle.width)).grid(sticky="nsew")

        self.loadIcons()
        ctrl_panel = ButtonSelector(self)
        for mode in EDIT_MODES:
            ctrl_panel.add("Edit " + mode.title(), mode, self.icons[mode])
        ctrl_panel.grid(sticky="nsew")

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
