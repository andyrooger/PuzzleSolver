"""
View for an unknown mode.

"""

import tkinter

import solver.plugin

class UnknownView(solver.plugin.PuzzleView):
    """Functionality for an unknown mode."""

    def __init__(self, mode):
        solver.plugin.PuzzleView.__init__(self)
        self._mode = mode

    def get_frame(self, master):
        txt = "Sorry, this mode is not supported: " + self._mode
        return tkinter.Label(master, text=txt)

    def can_solve(self): return False
    def get_solver(self): return None
    def get_extension(self): return None
    def get_puzzle(self): return None
    def changed(self): return False
    def saved(self): pass
    def clean(self): pass
    def load(self, puzzle): return False
