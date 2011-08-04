"""
Contains the content frame for the main window.

"""

import tkinter

import solver.state

from solver.utility.simpleframe import SimpleFrame
from . puzzlesaver import PuzzleSaver

class ViewFrame(SimpleFrame):
    """Frame to contain current view."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)

        # Should always happen first so vito is a hack
        solver.state.view.vitoChange(self._onViewChange)
        solver.state.puzzle.change(None)

        solver.state.mode.vitoChange(self._vitoPuzzleOrModeChange)
        solver.state.puzzle.vitoChange(self._vitoPuzzleOrModeChange)
        solver.state.quitting.vitoChange(self._vitoQuitting)
        solver.state.wiping.vitoChange(self._vitoWiping)

    def _vitoPuzzleOrModeChange(self, _):
        return not solver.state.wiping.attempt()

    def _vitoQuitting(self, _):
        return not solver.state.wiping.attempt()

    def _vitoWiping(self, _):
        return not PuzzleSaver().check(self)

    def _onViewChange(self, view):
        frame = (
            tkinter.Label(self, text="No puzzle type is currently selected.")
            if view == None else view.getFrame(self))
        self.setContent(frame)
        return False # do not vito, EVER!
