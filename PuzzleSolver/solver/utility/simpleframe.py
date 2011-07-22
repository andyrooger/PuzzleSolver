"""
Contains a frame that allows a single child to be displayed at a time.

"""

import tkinter

class SimpleFrame(tkinter.Frame):
    """Display a single child at any time."""

    def __init__(self, master, init=None):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = None
        self.setContent(init)

    def setContent(self, child=None):
        if self.content != None:
            self.content.grid_forget()
        self.content = child
        if self.content != None:
            self.content.grid(sticky="nsew", column=0, row=0)
