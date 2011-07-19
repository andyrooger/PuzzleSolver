"""
Contains the solver button code.

"""

import tkinter

class SolverButton(tkinter.Frame):
    """Solver button widget."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected = False
        self.btn = tkinter.Button(self, text="Solve", command=self.toggle)
        self.btn.grid(sticky="nsew")

    def toggle(self):
        self.pressed(not self.selected) 

    def pressed(self, selected):
        if selected == self.selected:
            return
        self.selected = selected
        if selected:
            self.btn.config(relief=tkinter.SUNKEN)
        else:
            self.btn.config(relief=tkinter.RAISED)

    def setEnabled(self, enabled):
        state = tkinter.ENABLED if enabled else tkinter.DISABLED
        self.btn.config(state=state)
