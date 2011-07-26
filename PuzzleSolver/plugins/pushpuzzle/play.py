"""
View for Push Puzzle playing.

"""

import tkinter
import os.path

import solver.plugin

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
        return None

    def changed(self):
        return False

    def saved(self):
        pass

    def clean(self):
        pass

    def load(self, puzzle):
        return False

class PlayFrame(tkinter.Frame):
    """GUI for playing the game."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "resources", "images")
        self.larrow = tkinter.PhotoImage(file=os.path.join(directory, "larrow.gif"))
        self.rarrow = tkinter.PhotoImage(file=os.path.join(directory, "rarrow.gif"))
        tkinter.Button(self, image=self.larrow).grid(sticky="nsew", row=0, column=0)
        tkinter.Button(self, image=self.rarrow).grid(sticky="nsew", row=0, column=1)

        tkinter.Label(self, text="Play Mode!!!").grid(sticky="nsew", columnspan=2, row=1, column=0)
