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

        self._selector = ButtonSelector(self, selected=self._change_mode)
        for mode in solver.state.mode.allowable:
            self._selector.add(mode.title(), mode)
        self._selector.grid(sticky="nsew")

        solver.state.puzzletype.on_change(self._puzzletype_chosen)
        solver.state.mode.during_change(self._mode_chosen)

    def _puzzletype_chosen(self, puzzletype):
        self._selector.set_enabled(puzzletype != None)

    def _mode_chosen(self, mode):
        self._selector.selection(mode)

    def _change_mode(self, mode):
        if not solver.state.mode.change(mode):
            self._selector.selection(solver.state.mode.value())
