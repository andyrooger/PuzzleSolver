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
        self._btn = tkinter.Button(self, text="Solve", command=self.toggle)
        self._btn.grid(sticky="nsew")

        self._pressed(solver.state.solving.value() != None)

        solver.state.view.on_change(self._view_changed)
        solver.state.solving.during_change(self._solving_changed)
        solver.state.solving.vito_change(self._vito_solving)
        solver.state.wiping.vito_change(self._vito_wipe)

    def toggle(self):
        """Press or unpress the button."""
        
        cur = solver.state.solving.value()
        solver.state.solving.change(solver.state.view.value().get_solver() if cur == None else None)

    def _pressed(self, selected):
        """Update the pressed status and look of the button."""
        
        if selected == self._selected:
            return
        self._selected = selected
        if selected:
            self._btn.config(relief=tkinter.SUNKEN)
        else:
            self._btn.config(relief=tkinter.RAISED)

    def _view_changed(self, view):
        state = tkinter.NORMAL if view != None and view.can_solve() else tkinter.DISABLED
        self._btn.config(state=state)

    def _solving_changed(self, solving):
        self._pressed(solving != None)
        if solving != None:
            solving.start()

    def _vito_solving(self, solving):
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

    def _vito_wipe(self, _):
        return not solver.state.solving.change(None)
