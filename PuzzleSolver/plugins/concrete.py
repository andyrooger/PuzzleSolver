"""
Various base classes for plugins.

"""

import tkinter

import solver.plugin

_i = 0

class Puzzle(solver.plugin.PuzzleType):
    """Entire plugin."""

    def __init__(self):
        global _i
        solver.plugin.PuzzleType.__init__(self)
        self.i = _i
        _i += 1

    def name(self):
        """Get the name of the puzzle type."""
        return "Concrete " + str(self.i)

    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""
        return ConcreteView(mode, self.i)

class ConcreteView(solver.plugin.PuzzleView):
    """Functionality for a single mode."""

    def __init__(self, mode, i):
        solver.plugin.PuzzleView.__init__(self)
        self.mode = mode
        self.i = i

    def getFrame(self, master):
        """Get the GUI frame."""
        return tkinter.Label(master, text="Hello I am " + str(self.i) + " and my mode is " + self.mode)

    def canSolve(self):
        """Can we solve puzzles in this view."""
        return self.i == 3

    def getSolver(self):
        """Get the solver for this view if one exists."""
        return None

    def getExtension(self):
        """Get either the file extension used to save the puzzles below, or None."""
        return ".con"

    def getPuzzle(self):
        """Get either the puzzle object if it can be saved, or None."""
        return True

    def changed(self):
        """Was the puzzle changed since the last call to save."""
        return self.i == 4

    def saved(self):
        """Reset changed."""
