"""
Dialog allowing analysis of a puzzle.

"""

import tkinter

class AnalysisDialog(tkinter.Toplevel):
    """Allows analysis of the given puzzle file."""
    
    def __init__(self, master, puzzle):
        tkinter.Toplevel.__init__(self, master)
        
        self._puzzle = puzzle
        
        self.title("Puzzle Analysis")
        self.grab_set()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", (lambda: False))
        self.resizable(False, False)
        
        tkinter.Button(self, text="OK", command=self._done).grid(sticky="nsew", row=1, column=0)
        
    def _done(self):
        self.destroy()