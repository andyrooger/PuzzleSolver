"""
Editor frame for push puzzle.

"""

import tkinter

from . puzzle import Puzzle

class PuzzleEditor(tkinter.Frame):
    def __init__(self, master, puzzle):
        if not isinstance(puzzle, Puzzle):
            raise ValueError # Puzzle is broken
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="puzzleedit").grid(sticky="nsew")
        tkinter.Label(self, text="Height: "+str(puzzle.height)).grid(sticky="nsew")
        tkinter.Label(self, text="Width: "+str(puzzle.width)).grid(sticky="nsew")

    def getPuzzle(self): return None
    def saved(self): pass
    def changed(self): return False
