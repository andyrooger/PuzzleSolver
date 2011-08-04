"""
Contains puzzle type selection controls.

"""

import tkinter

import solver.state

from .. utility.buttonselector import ButtonSelector

class PuzzleChoice(tkinter.Frame):
    """Puzzle type selection widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        tkinter.Label(self, text="Choose a puzzle type:").grid(row=0, sticky="new")

        self._selector = ButtonSelector(self, vertical=True, selected=self._change_puzzle)
        for plugin in solver.state.puzzle.allowable:
            if plugin != None:
                self._selector.add(plugin.name(), plugin)
        self._selector.grid(row=1, sticky="nsew")

        solver.state.puzzle.during_change(self._selector.selection)

    def _change_puzzle(self, puzzle):
        if solver.state.puzzle.change(None):
            solver.state.mode.change("CREATE")
            solver.state.puzzle.change(puzzle)
        else:
            self._selector.selection(solver.state.puzzle.value())
