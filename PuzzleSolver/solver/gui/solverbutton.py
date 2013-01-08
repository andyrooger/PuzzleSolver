"""
Contains the solver button code.

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
from tkinter import messagebox

import solver.state

class SolverButton(tkinter.Frame):
    """Solver button widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected = False
        self.btn = tkinter.Button(self, text="Solve", command=self.toggle)
        self.btn.grid(sticky="nsew")

        self.pressed(solver.state.solving.value() != None)

        solver.state.view.onChange(self.viewChanged)
        solver.state.solving.onChange(self.solvingChanged)
        solver.state.solving.vitoChange(self.vitoSolving)
        solver.state.wiping.vitoChange(self.vitoWipe)

    def toggle(self):
        cur = solver.state.solving.value()
        solver.state.solving.change(solver.state.view.value().getSolver() if cur == None else None)

    def pressed(self, selected):
        if selected == self.selected:
            return
        self.selected = selected
        if selected:
            self.btn.config(relief=tkinter.SUNKEN)
        else:
            self.btn.config(relief=tkinter.RAISED)

    def viewChanged(self, view):
        state = tkinter.NORMAL if view != None and view.canSolve() else tkinter.DISABLED
        self.btn.config(state=state)

    def solvingChanged(self, solving):
        self.pressed(solving != None)
        if solving != None:
            solving.start()

    def vitoSolving(self, solving):
        old = solver.state.solving.value()
        if solving == old:
            return False
        if solving == None and old != None:
            # Cancelling a solve
            worked = old.stop()
            if not worked:
                messagebox.showinfo("Whoops", "Sorry, the solving process could not be interrupted.")
            return not worked
        else:
            return False

    def vitoWipe(self, _):
        return not solver.state.solving.change(None)
