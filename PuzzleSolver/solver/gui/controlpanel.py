"""
Contains the control panel for loading/saving puzzles etc.

"""

import tkinter

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

    def clean(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def setEnabled(self, enabled):
        state = tkinter.ENABLED if enabled else tkinter.DISABLED
        self.cleanBtn.configure(state=state)
        self.saveBtn.configure(state=state)
        self.loadBtn.configure(state=state)
