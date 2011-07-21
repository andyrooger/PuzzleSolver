"""
View for Push Puzzle creation.

"""

import tkinter

import solver.plugin

class CreateView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle creation."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)

    def getFrame(self, master):
        return tkinter.Label(master, text="Create Mode!!!")

    def canSolve(self): return False
    def getSolver(self): return None

    def getExtension(self):
        return ".spp"

    def getPuzzle(self):
        return "The puzzle"

    def changed(self):
        return False

    def saved(self):
        pass

    def clean(self):
        pass

    def load(self, puzzle):
        return False
