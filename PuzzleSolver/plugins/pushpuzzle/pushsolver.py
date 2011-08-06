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
        
        self._status = tkinter.Label(self, text="Progress")
        self._status.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self._demo = tkinter.Button(self, text="Demonstrate", command=self.demo, state=tkinter.DISABLED)
        self._demo.grid(row=1, column=0)
        tkinter.Button(self, text="Cancel", command=self.cancel).grid(row=1, column=1)
        self._periodic_update()
        
    def demo(self):
        """Demonstrate the solution."""
        
        solver.state.solving.change(None) # should always work
        try:
            solution = self._solver.result()
        except pushastar.IncompleteError:
            pass
        else:
            if solution != None:
                self._finished(solution)
        self.destroy()
        
    def cancel(self):
        """Cancel the solver whether or not it is running."""
        
        if solver.state.solving.change(None):
            self.destroy()

    def _periodic_update(self):
        """Update the dialog."""
        
        # Should be already solving or finished
        if not self._solver.solving():
            self._status.config(text="Finished")
            if self._solver.result() != None:
                self._demo.config(state=tkinter.NORMAL)
        else:
            self._status.config(text="Still solving")
            self.after(1000, self._periodic_update)
