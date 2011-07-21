#!/usr/bin/env python3

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

import plugins

import solver.gui.main
import solver.state
import solver.plugin

if __name__ == "__main__":
    solver.state.puzzle.allowable = solver.plugin.load_plugins(plugins)
    solver.state.puzzle.allowable = [P() for P in solver.state.puzzle.allowable]
    solver.state.puzzle.allowable += [None]
    solver.gui.main.start_gui()
