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

from . puzzlesaver import PuzzleSaver

class ViewFrame(tkinter.Frame):
    """Frame to contain current view."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = None

        solver.state.view.onChange(self.onViewChange)
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

