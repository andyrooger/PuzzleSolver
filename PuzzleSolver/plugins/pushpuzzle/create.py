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
        self._frame = None

    def get_frame(self, master):
        self._frame = CreateFrame(master)
        return self._frame

    def can_solve(self): return False
    def get_solver(self): return None
    def get_extension(self): return ".spp"

    def get_puzzle(self): return self._frame.get_puzzle()
    def changed(self): return self._frame.changed()
    def saved(self): return self._frame.saved()
    def clean(self): return self._frame.clean()
    def load(self, puzzle): return self._frame.load(puzzle)

class CreateFrame(SimpleFrame):
    """GUI for the creation view."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)
        self.clean()

    def _showing_editor(self):
        return isinstance(self.content, PuzzleEditor)

    def clean(self):
        def show_editor(p):
            self.set_content(PuzzleEditor(self, p))
        self.set_content(PuzzleSetup(self, show_editor))

    def load(self, puzzle):
        try:
            puz = PuzzleEditor(self, puzzle)
        except ValueError:
            return False
        else:
            self.set_content(puz)
            return True

    def get_puzzle(self):
        if self._showing_editor():
            return self.content.get_puzzle()
        else:
            return None

    def saved(self):
        if self._showing_editor():
            self.content.saved()

    def changed(self):
        if self._showing_editor():
            return self.content.changed()
        else:
            return False

class PuzzleSetup(tkinter.Frame):
    def __init__(self, master, callback=(lambda r, c: None)):
        tkinter.Frame.__init__(self, master)
        self._callback = callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        centred = tkinter.Frame(self)
        centred.grid_columnconfigure(0, weight=1)

        tkinter.Label(centred, text="Please choose the dimensions for your new puzzle.").grid(
            sticky="nsew", row=0, column=0, columnspan=2)

        self._rows = tkinter.IntVar()
        self._rows.set(10)
        self._columns = tkinter.IntVar()
        self._columns.set(10)
        scale_info = {"from_": 1, "to": 50, "orient": tkinter.HORIZONTAL}

        tkinter.Scale(centred, label="Rows", variable=self._rows, **scale_info).grid(
            sticky="nsew", row=1, column=0)
        tkinter.Entry(centred, textvariable=self._rows, width=2).grid(
            sticky="sew", row=1, column=1)

        tkinter.Scale(centred, label="Columns", variable=self._columns, **scale_info).grid(
            sticky="nsew", row=2, column=0)
        tkinter.Entry(centred, textvariable=self._columns, width=2).grid(
            sticky="sew", row=2, column=1)

        tkinter.Button(centred, text="Create", command=self._create).grid(
            row=3, column=0, columnspan=2)

        # Separator
        tkinter.Frame(centred, height=2, bd=1, relief=tkinter.SUNKEN).grid(
            row=4, column=0, columnspan=2, padx=5, pady=15, sticky="ew")

        tkinter.Button(centred, text="Convert a Plain Puzzle File", command=self._convert).grid(
            row=5, column=0, columnspan=2, pady=5)

        centred.grid()

    def _create(self):
        """Create a puzzle based on dimensions."""
        
        p = Puzzle(self._rows.get(), self._columns.get())
        p.initial().finalise()
        self._callback(p)

    def _convert(self):
        """Load old-style puzzle file."""
