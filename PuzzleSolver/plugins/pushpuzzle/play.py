"""
View for Push Puzzle playing.

"""

import tkinter
import os.path

import solver.plugin
from solver.utility.simpleframe import SimpleFrame
from . playarea import PlayArea

class PlayView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle playing."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)
        self.frame = None

    def getFrame(self, master):
        self.frame = PlayFrame(master)
        return self.frame

    def canSolve(self): return False
    def getSolver(self): return None

    def getExtension(self):
        return ".spp"

    def getPuzzle(self):
        return self.frame.getPuzzle()

    def changed(self):
        return self.frame.changed()

    def saved(self):
        self.frame.saved()

    def clean(self):
        self.frame.clean()

    def load(self, puzzle):
        return self.frame.load(puzzle)

class PlayFrame(tkinter.Frame):
    """GUI for playing the game."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)

        self._changed = False

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.playframe = SimpleFrame(self)
        self.playframe.grid(sticky="nsew", columnspan=2, row=1, column=0)
        self.playarea = tkinter.Label(self.playframe, text="No puzzle loaded yet.")
        self.playframe.setContent(self.playarea)

        self.loadIcons()
        def prev():
            self.playarea.prev()
            self.buttonState()
        def next():
            self.playarea.next()
            self.buttonState()
        self.prevarrow = tkinter.Button(self, image=self.larrow, command=prev)
        self.prevarrow.grid(sticky="nsew", row=0, column=0)
        self.nextarrow = tkinter.Button(self, image=self.rarrow, command=next)
        self.nextarrow.grid(sticky="nsew", row=0, column=1)
        self.buttonState()

    def loadIcons(self):
        """Ensure that the necessary icons are loaded for the interface."""

        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "resources", "images")
        self.larrow = tkinter.PhotoImage(file=os.path.join(directory, "larrow.gif"))
        self.rarrow = tkinter.PhotoImage(file=os.path.join(directory, "rarrow.gif"))

    def puzzleLoaded(self):
        return isinstance(self.playarea, PlayArea)

    def buttonState(self):
        """Set disabled state for buttons."""

        if not self.puzzleLoaded():
            self.prevarrow.config(state=tkinter.DISABLED)
            self.nextarrow.config(state=tkinter.DISABLED)
            return

        self.prevarrow.config(state=(
            tkinter.NORMAL if self.playarea.hasprev() else tkinter.DISABLED
        ))
        self.nextarrow.config(state=(
            tkinter.NORMAL if self.playarea.hasnext() else tkinter.DISABLED
        ))

    def changed(self):
        return self._changed

    def saved(self):
        self._changed = False

    def getPuzzle(self):
        return None

    def clean(self):
        if self.puzzleLoaded():
            self.playarea.rewind()
            self.buttonState()

    def change(self):
        """Called whenever the puzzle is edited."""

        self._changed = True
        self.buttonState()

    def load(self, puzzle):
        self.playarea = PlayArea(self.playframe, puzzle, self.change)
        self.playframe.setContent(self.playarea)
        self.clean()
