"""
Contains the content frame for the main window.

"""

# PuzzleSolver
# Copyright (C) 2010  Andy Gurden
#
#     This file is part of PuzzleSolver.
#
#     PuzzleSolver is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PuzzleSolver is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PuzzleSolver.  If not, see <http://www.gnu.org/licenses/>.

import tkinter

import solver.state

from solver.utility.simpleframe import SimpleFrame
from . puzzlesaver import PuzzleSaver

class ViewFrame(SimpleFrame):
    """Frame to contain current view."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)

        solver.state.view.during_change(self._on_view_change)
        solver.state.puzzletype.change(None)

        solver.state.mode.vito_change(self._vito_puzzletype_or_mode_change)
        solver.state.puzzletype.vito_change(self._vito_puzzletype_or_mode_change)
        solver.state.quitting.vito_change(self._vito_quitting)
        solver.state.wiping.vito_change(self._vito_wiping)

    def _vito_puzzletype_or_mode_change(self, _):
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
