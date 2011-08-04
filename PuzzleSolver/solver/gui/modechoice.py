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

        self._selector = ButtonSelector(self, selected=self._change_mode)
        for mode in solver.state.mode.allowable:
            self._selector.add(mode.title(), mode)
        self._selector.grid(sticky="nsew")

        solver.state.puzzle.on_change(self._puzzle_chosen)
        solver.state.mode.on_change(self._mode_chosen)

    def _puzzle_chosen(self, puzzle):
        self._selector.setEnabled(puzzle != None)

    def _mode_chosen(self, mode):
        self._selector.selection(mode)

    def _change_mode(self, mode):
        if not solver.state.mode.change(mode):
            self._selector.selection(solver.state.mode.value())
