"""
Contains puzzle type selection controls.

"""

import tkinter

from .. utility.cancellableselector import CancellableSelector

class PuzzleChoice(tkinter.Frame):
    """Puzzle type selection widget."""

    def __init__(self, master, plugins):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        tkinter.Label(self, text="Choose a puzzle type:").grid(row=0, sticky="new")

        self.selector = CancellableSelector(self, vertical=True, selected=(lambda x: False))
        for plugin in plugins:
            self.selector.add(plugin.name(), plugin)
        self.selector.grid(row=1, sticky="nsew")

    def setEnabled(self, enabled):
        self.selector.setEnabled(enabled)
