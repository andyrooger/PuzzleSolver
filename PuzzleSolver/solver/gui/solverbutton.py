"""
Contains the solver button code.

"""

import tkinter

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

        self.pressed(solver.state.solving.value())

        solver.state.view.onChange(self.viewChanged)
        solver.state.solving.onChange(self.solvingChanged)
        solver.state.quitting.vitoChange(self.vitoQuitting)
        solver.state.puzzle.vitoChange(self.vitoPuzzle)
        solver.state.mode.vitoChange(self.vitoMode)

    def toggle(self):
        solver.state.solving.change(not solver.state.solving.value())

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
        self.pressed(solving)

    def vitoQuitting(self, quitting):
        if quitting:
            return not solver.state.solving.change(False)
        return False

    def vitoPuzzle(self, puzzle):
        return not solver.state.solving.change(False)

    def vitoMode(self, mode):
        return not solver.state.solving.change(False)
