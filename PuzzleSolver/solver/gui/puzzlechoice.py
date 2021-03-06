"""
Contains puzzle type selection controls.

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

class PuzzleChoice(tkinter.Frame):
    """Puzzle type selection widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        tkinter.Label(self, text="Choose a puzzle type:").grid(row=0, sticky="new")

        self.selector = ButtonSelector(self, vertical=True, selected=self.changePuzzle)
        for plugin in solver.state.puzzle.allowable:
            if plugin != None:
                self.selector.add(plugin.name(), plugin)
        self.selector.grid(row=1, sticky="nsew")

        solver.state.puzzle.onChange(self.setSelected)

    def changePuzzle(self, puzzle):
        if solver.state.puzzle.change(None):
            solver.state.mode.change("CREATE")
            solver.state.puzzle.change(puzzle)
        else:
            self.selector.selection(solver.state.puzzle.value())

    def setSelected(self, puzzle):
        self.selector.selection(puzzle)
