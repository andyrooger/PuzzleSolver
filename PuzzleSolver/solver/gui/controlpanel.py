"""
Contains the control panel for loading/saving puzzles etc.

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

from . puzzlesaver import PuzzleSaver
import solver.state

class ControlPanel(tkinter.Frame):
    """Control panel widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.cleanBtn = tkinter.Button(self, text="Clean", command=self.clean)
        self.cleanBtn.grid(column=0, row=0, sticky="nsew")
        self.saveBtn = tkinter.Button(self, text="Save", command=self.save)
        self.saveBtn.grid(column=1, row=0, sticky="nsew")
        self.loadBtn = tkinter.Button(self, text="Load", command=self.load)
        self.loadBtn.grid(column=2, row=0, sticky="nsew")

        solver.state.puzzle.onChange(self.puzzleChosen)
        solver.state.view.onChange(self.viewChanged)

    def clean(self):
        if solver.state.wiping.attempt():
            solver.state.view.value().clean()

    def save(self):
        PuzzleSaver().save(self)

    def load(self):
        if solver.state.wiping.attempt():
            PuzzleSaver().load(self)

    def puzzleChosen(self, puzzle):
        state = tkinter.NORMAL if puzzle != None else tkinter.DISABLED
        self.cleanBtn.configure(state=state)
        self.saveBtn.configure(state=state)
        self.loadBtn.configure(state=state)

    def viewChanged(self, view):
        puzzle = solver.state.view.value().getPuzzle()
        if puzzle != None:
            view.load(puzzle)
