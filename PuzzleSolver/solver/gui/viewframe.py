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

        # Should always happen first so vito is a hack
        solver.state.view.vitoChange(self.onViewChange)
        solver.state.puzzle.change(None)

        solver.state.mode.vitoChange(self.vitoPuzzleOrModeChange)
        solver.state.puzzle.vitoChange(self.vitoPuzzleOrModeChange)
        solver.state.quitting.vitoChange(self.vitoQuitting)
        solver.state.wiping.vitoChange(self.vitoWiping)

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
