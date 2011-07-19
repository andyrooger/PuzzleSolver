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

        self.selector = ButtonSelector(self)
        for mode in solver.state.mode.allowable:
            self.selector.add(mode.title(), mode)
        self.selector.grid(sticky="nsew")

    def setEnabled(self, enabled):
        self.selector.setEnabled(enabled)
