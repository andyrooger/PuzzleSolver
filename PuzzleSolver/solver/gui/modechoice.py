"""
Contains the mode choice code.

"""

import tkinter

import solver.state

from .. utility.buttonselector import ButtonSelector

class ModeChoice(tkinter.Frame):
    """Mode choice widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selector = ButtonSelector(self, selected=self.changeMode)
        for mode in solver.state.mode.allowable:
            self.selector.add(mode.title(), mode)
        self.selector.grid(sticky="nsew")

        solver.state.puzzle.onChange(self.puzzleChosen)
        solver.state.mode.onChange(self.modeChosen)

    def puzzleChosen(self, puzzle):
        self.selector.setEnabled(puzzle != None)

    def modeChosen(self, mode):
        self.selector.selection(mode)

    def changeMode(self, mode):
        if not solver.state.mode.change(mode):
            self.selector.selection(solver.state.mode.value())
