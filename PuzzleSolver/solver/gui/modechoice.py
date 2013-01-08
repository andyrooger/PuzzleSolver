"""
Contains the mode choice code.

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

from .. utility.buttonselector import ButtonSelector

class ModeChoice(tkinter.Frame):
    """Mode choice widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selector = ButtonSelector(self, selected=self.changeMode)
        for mode in solver.state.mode.allowable:
            self.selector.add(mode.title(), mode)
        self.selector.grid(sticky="nsew")

        solver.state.puzzle.onChange(self.puzzleChosen)
        solver.state.mode.onChange(self.modeChosen)

    def puzzleChosen(self, puzzle):
        self.selector.setEnabled(puzzle != None)

    def modeChosen(self, mode):
        self.selector.selection(mode)

    def changeMode(self, mode):
        if not solver.state.mode.change(mode):
            self.selector.selection(solver.state.mode.value())
