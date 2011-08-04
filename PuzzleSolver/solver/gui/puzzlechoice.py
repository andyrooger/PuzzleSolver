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

        self._selector = ButtonSelector(self, vertical=True, selected=self._change_puzzletype)
        for plugin in solver.state.puzzletype.allowable:
            if plugin != None:
                self._selector.add(plugin.name(), plugin)
        self._selector.grid(row=1, sticky="nsew")

        solver.state.puzzletype.during_change(self._selector.selection)

    def _change_puzzletype(self, puzzletype):
        if solver.state.puzzletype.change(None):
            solver.state.mode.change("CREATE")
            solver.state.puzzletype.change(puzzletype)
        else:
            self._selector.selection(solver.state.puzzletype.value())
