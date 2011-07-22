"""
View for Push Puzzle creation.

"""

import tkinter

import solver.plugin

class CreateView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle creation."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)
        self.frame = None

    def getFrame(self, master):
        self.frame = CreateFrame(master)
        return self.frame

    def canSolve(self): return False
    def getSolver(self): return None
    def getExtension(self): return ".spp"

    def getPuzzle(self): return self.frame.getPuzzle()
    def changed(self): return self.frame.changed()
    def saved(self): return self.frame.saved()
    def clean(self): return self.frame.clean()
    def load(self, puzzle): return self.frame.load(puzzle)

class CreateFrame(tkinter.Frame):
    """GUI for the creation view."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.content = None

    def setContent(self, content):
        if self.content != None:
            self.content.grid_forget()
        self.content = content
        self.content.grid(sticky="nsew", row=0, column=0)

    def clean(self): pass
    def load(self, puzzle): return True
    def getPuzzle(self): return None
    def saved(self): pass
    def changed(self): return False
