"""
Dialog allowing analysis of a puzzle.

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
from solver.utility.scrollable_window import ScrollableWindow

from . import style

class AnalysisDialog(tkinter.Toplevel):
    """Allows analysis of the given puzzle file."""
    
    def __init__(self, master, puzzle):
        tkinter.Toplevel.__init__(self, master)
        
        self.title("Puzzle Analysis")
        self.grab_set()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", (lambda: False))
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        AnalysisPane(self, puzzle).grid(sticky="nsew", row=0, column=0)
        
        tkinter.Button(self, text="OK", command=self._done).grid(sticky="nsew", row=1, column=0)
        
    def _done(self):
        self.destroy()
        
class AnalysisPane(ScrollableWindow):
    """Shows the results of the analysis on the current puzzle."""

    def __init__(self, master, puzzle):
        ScrollableWindow.__init__(self, master)
        
        self._buttons = []
        for y in range(puzzle.base.height):
            row = []
            for x in range(puzzle.base.width):
                pos = (x, y)
                p = AnalysisTile(self.window)
                row.append(p)
                p.grid(sticky="nsew", row=y, column=x)
            self._buttons.append(row)
        self._update_tiles(puzzle)

    def _update_tiles(self, puzzle):
        """Tell each tile what their content should be."""
        
        for x,y in puzzle.base.walls:
            self._buttons[y][x].content("WALL")

class AnalysisTile(tkinter.Button):
    """Single tile in the puzzle."""

    def __init__(self, master):
        tkinter.Button.__init__(self, master, relief="flat")
        self.content("EMPTY", noupdate=True)
        self._appearance()

    def content(self, c = None, noupdate=False):
        if c != None:
            self._content = c
            noupdate or self._appearance()
        return self._content

    def _appearance(self):
        """Set up appearance."""

        self.config(**style.tile_style(self.content(), False, separated=False))
