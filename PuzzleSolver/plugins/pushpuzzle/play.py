"""
View for Push Puzzle playing.

"""

import tkinter

import solver.plugin

class PlayView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle playing."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)

    def getFrame(self, master):
        return tkinter.Label(master, text="Play Mode!!!")

    def canSolve(self): return False
    def getSolver(self): return None

    def getExtension(self):
        return ".spp"

    def getPuzzle(self):
        return None

    def changed(self):
        return False

    def saved(self):
        pass

    def clean(self):
        pass

    def load(self, puzzle):
        return False
