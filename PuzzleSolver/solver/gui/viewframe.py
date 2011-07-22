"""
Contains the content frame for the main window.

"""

import tkinter

import solver.state

from . puzzlesaver import PuzzleSaver

class ViewFrame(tkinter.Frame):
    """Frame to contain current view."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = None

        # Should always happen first so vito is a hack
        solver.state.view.vitoChange(self.onViewChange)
        solver.state.puzzle.change(None)

        solver.state.mode.vitoChange(self.vitoPuzzleOrModeChange)
        solver.state.puzzle.vitoChange(self.vitoPuzzleOrModeChange)
        solver.state.quitting.vitoChange(self.vitoQuitting)
        solver.state.wiping.vitoChange(self.vitoWiping)

    def setContent(self, frame):
        if self.content != None:
            self.content.grid_forget()
        self.content = frame
        self.content.grid(sticky="nsew")

    def vitoPuzzleOrModeChange(self, _):
        return not solver.state.wiping.attempt()

    def vitoQuitting(self, _):
        return not solver.state.wiping.attempt()

    def vitoWiping(self, _):
        return not PuzzleSaver().check(self)

    def onViewChange(self, view):
        frame = (
            tkinter.Label(self, text="No puzzle type is currently selected.")
            if view == None else view.getFrame(self))
        self.setContent(frame)
        return False # do not vito, EVER!
