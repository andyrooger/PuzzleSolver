"""
Plugin for the Sun Push Puzzle demo given in the old J2ME SDK.

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

import solver.plugin

from . pushpuzzle import play, create, unknown

class Puzzle(solver.plugin.PuzzleType):
    """Entire plugin."""

    def __init__(self):
        solver.plugin.PuzzleType.__init__(self)

    def name(self):
        """Get the name of the puzzle type."""
        return "Sun Push Puzzle"

    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""
        if mode == "CREATE":
            return create.CreateView()
        elif mode == "PLAY":
            return play.PlayView()
        else:
            return unknown.UnknownView(mode)
