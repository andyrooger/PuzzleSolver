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
        self.data = tkinter.StringVar()
        self.changeValue("", False)

    def changeValue(self, text, needssaving=True):
        self.data.set(text)
        if not needssaving:
            self.oldval = text

    def getFrame(self, master):
        """Get the GUI frame."""
        fr = tkinter.Frame(master)
        fr.grid_rowconfigure(0, weight=1)
        fr.grid_columnconfigure(0, weight=1)
        tkinter.Label(fr, text="Hello I am " + str(self.i) + " and my mode is " + self.mode).grid(row=0, column=0, sticky="nsew")
        tkinter.Entry(fr, textvariable=self.data).grid(row=1, column=0, sticky="sew")
        return fr

    def canSolve(self):
        """Can we solve puzzles in this view."""
        return self.i == 3

    def getSolver(self):
        """Get the solver for this view if one exists."""
        return ConcreteSolver() if self.i == 3 else None

    def getExtension(self):
        """Get either the file extension used to save the puzzles below, or None."""
        return ".con"

    def getPuzzle(self):
        """Get either the puzzle object if it can be saved, or None."""
        return self.data.get()

    def changed(self):
        """Was the puzzle changed since the last call to save."""
        return self.data.get() != self.oldval

    def saved(self):
        """Reset changed."""
        self.oldval = self.data.get()

    def clean(self):
        """Clean the view, removing all user changes."""
        self.changeValue("")

    def load(self, puzzle):
        """Load the given puzzle if possible and return if successful."""
        self.changeValue(str(puzzle), False)

class ConcreteSolver(solver.plugin.Solver):
    """Functionality for a puzzle solver, changed will be performed on the underlying view."""

    def start(self):
        """Start the solver."""

        print("Solving...")

    def stop(self):
        """Stop the solver and return success (in stopping)."""

        print("Done.")
        return True
