"""
View for Push Puzzle playing.

"""

import tkinter
import os.path

import solver.plugin
from solver.utility.simpleframe import SimpleFrame

from . import style
from . playarea import PlayArea

class PlayView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle playing."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)
        self.frame = None

    def getFrame(self, master):
        self.frame = PlaceholderPlayFrame(master)
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

class PlaceholderPlayFrame(SimpleFrame):
    """Like SimpleFrame but has a placeholder before a puzzle is loaded."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)

        self.setContent(tkinter.Label(self, text="No puzzle loaded yet."))

    def puzzleLoaded(self):
        return isinstance(self.content, PlayFrame)

    def changed(self):
        return self.content.changed() if self.puzzleLoaded() else False

    def saved(self):
        if self.puzzleLoaded():
            self.content.saved()

    def getPuzzle(self):
        return self.content.getPuzzle() if self.puzzleLoaded() else None

    def clean(self):
        if self.puzzleLoaded():
            self.content.clean()

    def load(self, puzzle):
        try:
            p = PlayFrame(self, puzzle)
            self.setContent(p)
            return True
        except ValueError:
            return False

class PlayFrame(tkinter.Frame):
    """GUI for playing the game."""

    def __init__(self, master, puzzle):
        tkinter.Frame.__init__(self, master)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._changed = False
        self.playarea = PlayArea(self, puzzle, self.change) # Could throw valueerror
        self.playarea.grid(sticky="nsew", columnspan=2, row=1, column=0)

        def prev():
            self.playarea.prev()
            self.buttonState()
        def next():
            self.playarea.next()
            self.buttonState()
        self.prevarrow = tkinter.Button(self, image=style.loadIcon("larrow"), command=prev)
        self.prevarrow.grid(sticky="nsew", row=0, column=0)
        self.nextarrow = tkinter.Button(self, image=style.loadIcon("rarrow"), command=next)
        self.nextarrow.grid(sticky="nsew", row=0, column=1)
        self.buttonState()

        self.clean()

    def buttonState(self):
        """Set disabled state for buttons."""

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
        return None # TODO - maybe

    def clean(self):
        self.playarea.rewind()
        self.buttonState()

    def change(self):
        """Called whenever the puzzle is edited."""

        self._changed = True
        self.buttonState()

