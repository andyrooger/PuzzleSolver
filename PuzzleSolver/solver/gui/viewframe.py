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

        solver.state.view.during_change(self._on_view_change)
        solver.state.puzzle.change(None)

        solver.state.mode.vito_change(self._vito_puzzle_or_mode_change)
        solver.state.puzzle.vito_change(self._vito_puzzle_or_mode_change)
        solver.state.quitting.vito_change(self._vito_quitting)
        solver.state.wiping.vito_change(self._vito_wiping)

    def _vito_puzzle_or_mode_change(self, _):
        return not solver.state.wiping.attempt()

    def _vito_quitting(self, _):
        return not solver.state.wiping.attempt()

    def _vito_wiping(self, _):
        return not PuzzleSaver().check(self)

    def _on_view_change(self, view):
        frame = (
            tkinter.Label(self, text="No puzzle type is currently selected.")
            if view == None else view.get_frame(self))
        self.set_content(frame)
