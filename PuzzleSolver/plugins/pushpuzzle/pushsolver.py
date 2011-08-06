"""
Solver for the push puzzle.

"""

import tkinter

import solver.plugin
import solver.state

from . import pushastar

class PushSolver(solver.plugin.Solver):
    """Solver for the PushPuzzle."""
    
    def __init__(self, frame, finished):
        self._playframe = frame
        self._puzzle = None
        self._finished = finished
        self._solver = None
    
    def start(self):
        """Start the push puzzle solver."""
        
        self._playframe.freeze(True)
        self._solver = pushastar.PushAStar(self._playframe.get_puzzle())
        self._solver.begin()
        SolverStatusDialog(self._playframe, self._solver, self._finished)
    
    def stop(self):
        """
        Stop the push puzzle solver.
        
        This should only ever be called by a cancellation from the dialog. The cancellation
        should not be possible from the main window.
        """
        
        if not self._solver.cancel():
            return False # it's still running
        self._playframe.freeze(False)
        # Now let the dialog decide what to do with it
        return True

class SolverStatusDialog(tkinter.Toplevel):
    """Record and periodically update information about the status of the solver."""
    
    def __init__(self, master, solver, finished):
        tkinter.Toplevel.__init__(self, master)
        self._solver = solver
        self._finished = finished
        
        self.title("Solving...")
        self.grab_set()
        self.transient(master)
        
        tkinter.Label(self, text="Progress").grid()
        tkinter.Button(self, text="Cancel", command=self.cancel).grid()
        self.wait_window(self)
        
        
    def cancel(self):
        if solver.state.solving.change(None):
            self.destroy()
