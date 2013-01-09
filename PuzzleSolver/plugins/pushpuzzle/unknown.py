"""
View for an unknown mode.

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

import solver.plugin

class UnknownView(solver.plugin.PuzzleView):
    """Functionality for an unknown mode."""

    def __init__(self, mode):
        solver.plugin.PuzzleView.__init__(self)
        self._mode = mode

    def get_frame(self, master):
        txt = "Sorry, this mode is not supported: " + self._mode
        return tkinter.Label(master, text=txt)

    def can_solve(self): return False
    def get_solver(self): return None
    def get_extension(self): return None
    def get_directory(self): return None
    def get_puzzle(self): return None
    def changed(self): return False
    def saved(self): pass
    def clean(self): pass
    def load(self, puzzle): return False
