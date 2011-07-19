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

        self.selector = ButtonSelector(self, vertical=True, selected=self.changePuzzle)
        for plugin in solver.state.puzzle.allowable:
            if plugin != None:
                self.selector.add(plugin.name(), plugin)
        self.selector.grid(row=1, sticky="nsew")

    def changePuzzle(self, puzzle):
        if solver.state.puzzle.change(None):
            solver.state.mode.change("CREATE")
            solver.state.puzzle.change(puzzle)

    def setEnabled(self, enabled):
        self.selector.setEnabled(enabled)
