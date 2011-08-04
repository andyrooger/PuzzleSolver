"""
Contains the control panel for loading/saving puzzles etc.

"""

import tkinter

from . puzzlesaver import PuzzleSaver
import solver.state

class ControlPanel(tkinter.Frame):
    """Control panel widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._cleanBtn = tkinter.Button(self, text="Clean", command=self.clean)
        self._cleanBtn.grid(column=0, row=0, sticky="nsew")
        self._saveBtn = tkinter.Button(self, text="Save", command=self.save)
        self._saveBtn.grid(column=1, row=0, sticky="nsew")
        self._loadBtn = tkinter.Button(self, text="Load", command=self.load)
        self._loadBtn.grid(column=2, row=0, sticky="nsew")

        solver.state.puzzle.on_change(self._puzzle_chosen)
        solver.state.view.on_change(self._view_changed)

    def clean(self):
        if solver.state.wiping.attempt():
            solver.state.view.value().clean()

    def save(self):
        PuzzleSaver().save(self)

    def load(self):
        if solver.state.wiping.attempt():
            PuzzleSaver().load(self)

    def _puzzle_chosen(self, puzzle):
        state = tkinter.NORMAL if puzzle != None else tkinter.DISABLED
        self._cleanBtn.configure(state=state)
        self._saveBtn.configure(state=state)
        self._loadBtn.configure(state=state)

    def _view_changed(self, view):
        puzzle = solver.state.view.value().get_puzzle()
        if puzzle != None:
            view.load(puzzle)
