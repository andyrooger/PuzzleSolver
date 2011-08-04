"""
Contains the solver button code.

"""

import tkinter
from tkinter import messagebox

import solver.state

class SolverButton(tkinter.Frame):
    """Solver button widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._selected = False
        self.btn = tkinter.Button(self, text="Solve", command=self.toggle)
        self.btn.grid(sticky="nsew")

        self._pressed(solver.state.solving.value() != None)

        solver.state.view.onChange(self._viewChanged)
        solver.state.solving.onChange(self._solvingChanged)
        solver.state.solving.vitoChange(self._vitoSolving)
        solver.state.wiping.vitoChange(self._vitoWipe)

    def toggle(self):
        """Press or unpress the button."""
        
        cur = solver.state.solving.value()
        solver.state.solving.change(solver.state.view.value().getSolver() if cur == None else None)

    def _pressed(self, selected):
        """Update the pressed status and look of the button."""
        
        if selected == self._selected:
            return
        self._selected = selected
        if selected:
            self.btn.config(relief=tkinter.SUNKEN)
        else:
            self.btn.config(relief=tkinter.RAISED)

    def _viewChanged(self, view):
        state = tkinter.NORMAL if view != None and view.canSolve() else tkinter.DISABLED
        self.btn.config(state=state)

    def _solvingChanged(self, solving):
        self._pressed(solving != None)
        if solving != None:
            solving.start()

    def _vitoSolving(self, solving):
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

    def _vitoWipe(self, _):
        return not solver.state.solving.change(None)
