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

        self._selector = ButtonSelector(self, vertical=True, selected=self._change_puzzletype)
        for plugin in solver.state.puzzletype.allowable:
            if plugin != None:
                self._selector.add(plugin.name(), plugin)
        self._selector.grid(row=1, sticky="nsew")

        solver.state.puzzletype.during_change(self._selector.selection)

    def _change_puzzletype(self, puzzletype):
        if solver.state.puzzletype.change(None):
            solver.state.mode.change("CREATE")
            solver.state.puzzletype.change(puzzletype)
        else:
            self._selector.selection(solver.state.puzzletype.value())
