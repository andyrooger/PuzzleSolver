"""
View for Push Puzzle creation.

"""

import tkinter

import solver.plugin
from solver.utility.simpleframe import SimpleFrame

from . puzzleeditor import PuzzleEditor
from . puzzle import Puzzle


class CreateView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle creation."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)
        self.frame = None

    def get_frame(self, master):
        self.frame = CreateFrame(master)
        return self.frame

    def can_solve(self): return False
    def get_solver(self): return None
    def get_extension(self): return ".spp"

    def get_puzzle(self): return self.frame.get_puzzle()
    def changed(self): return self.frame.changed()
    def saved(self): return self.frame.saved()
    def clean(self): return self.frame.clean()
    def load(self, puzzle): return self.frame.load(puzzle)

class CreateFrame(SimpleFrame):
    """GUI for the creation view."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)
        self.clean()

    def showingEditor(self):
        return isinstance(self.content, PuzzleEditor)

    def clean(self):
        def puzzle_create(r, c):
            p = Puzzle(r, c)
            p.initial().finalise()
            self.set_content(PuzzleEditor(self, p))
        self.set_content(DimensionChooser(self, puzzle_create))

    def load(self, puzzle):
        try:
            puz = PuzzleEditor(self, puzzle)
        except ValueError:
            return False
        else:
            self.set_content(puz)
            return True

    def get_puzzle(self):
        if self.showingEditor():
            return self.content.get_puzzle()
        else:
            return None

    def saved(self):
        if self.showingEditor():
            self.content.saved()

    def changed(self):
        if self.showingEditor():
            return self.content.changed()
        else:
            return False

class DimensionChooser(tkinter.Frame):
    def __init__(self, master, callback=(lambda r, c: None)):
        tkinter.Frame.__init__(self, master)
        self.callback = callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        centred = tkinter.Frame(self)
        centred.grid_columnconfigure(0, weight=1)

        tkinter.Label(centred, text="Please choose the dimensions for your new puzzle.").grid(
            sticky="nsew", row=0, column=0, columnspan=2)

        self.rows = tkinter.IntVar()
        self.rows.set(10)
        self.columns = tkinter.IntVar()
        self.columns.set(10)
        scale_info = {"from_": 1, "to": 50, "orient": tkinter.HORIZONTAL}

        tkinter.Scale(centred, label="Rows", variable=self.rows, **scale_info).grid(
            sticky="nsew", row=1, column=0)
        tkinter.Entry(centred, textvariable=self.rows, width=2).grid(
            sticky="sew", row=1, column=1)

        tkinter.Scale(centred, label="Columns", variable=self.columns, **scale_info).grid(
            sticky="nsew", row=2, column=0)
        tkinter.Entry(centred, textvariable=self.columns, width=2).grid(
            sticky="sew", row=2, column=1)

        tkinter.Button(centred, text="Create", command=self.click).grid(
            row=3, column=0, columnspan=2)

        centred.grid()

    def click(self):
        self.callback(self.rows.get(), self.columns.get())
