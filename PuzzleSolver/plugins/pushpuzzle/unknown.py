"""
View for an unknown mode.

"""

import tkinter

import solver.plugin

class UnknownView(solver.plugin.PuzzleView):
    """Functionality for an unknown mode."""

    def __init__(self, mode):
        solver.plugin.PuzzleView.__init__(self)
        self.mode = mode

    def getFrame(self, master):
        txt = "Sorry, this mode is not supported: " + self.mode
        return tkinter.Label(master, text=txt)

    def canSolve(self): return False
    def getSolver(self): return None
    def getExtension(self): return None
    def getPuzzle(self): return None
    def changed(self): return False
    def saved(self): pass
    def clean(self): pass
    def load(self, puzzle): return False
