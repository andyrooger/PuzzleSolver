"""
Solver for the push puzzle.

"""

import tkinter

import solver.plugin
import solver.state
from solver.utility import process_exec, simpleframe, buttonselector

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
        
        def make_solver(*vargs, **kwargs):
            self._solver = process_exec.ProcessExecutor(
                pushastar.solve,
                self._playframe.get_puzzle().state(),
                *vargs, **kwargs)
            self._solver.start()
            SolverStatusDialog(self._playframe, self._solver, self._finished)
            
        SolverConfig(self._playframe, make_solver)
    
    def stop(self):
        """
        Stop the push puzzle solver.
        
        This should only ever be called by a cancellation from the dialog. The cancellation
        should not be possible from the main window.
        """
        
        self._solver.cancel()
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
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
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
        except process_exec.IncompleteError:
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
        if not self._solver.working():
            self._status.config(text="Finished")
            try:
                if self._solver.result() != None:
                    self._demo.config(state=tkinter.NORMAL)
            except process_exec.IncompleteError:
                self._status.config(text="Something went horribly wrong!")
        else:
            self._status.config(text="Still solving")
            self.after(1000, self._periodic_update)

class SolverConfig(tkinter.Toplevel):
    """Deals with configuration for the solver, choosing solver classes and heuristics."""
    
    def __init__(self, master, done):
        tkinter.Toplevel.__init__(self, master)
        
        self._done = done
        
        self.title("Solver configuration")
        self.grab_set()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", (lambda: False))
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        
        self._question = tkinter.Label(self)
        self._question.grid(sticky="new")
        self._content = simpleframe.SimpleFrame(self)
        self._content.grid(sticky="nsew")
        
        self._ask_initial()
        
    def ask(self, question, answers, callback=None):
        """Ask a question."""
        
        self._question.config(text=question)
        print(callback)
        selector = buttonselector.ButtonSelector(self._content, vertical=True, selected=callback)
        for a in answers:
            selector.add(a, answers[a])
        self._content.set_content(selector)
        
    def finish(self, *vargs, **kwargs):
        """Spit out the given solver arguments."""
        
        self.destroy()
        self._done(*vargs, **kwargs)
        
    def _ask_initial(self):
        self.ask("Would you like to use solver defaults or manage this by your self?",
                 {
                  "Use Defaults": True,
                  "Configure on my Own.": False
                 },
                 callback=self._configure_defaults)
        
    def _configure_defaults(self, usedefaults):
        if usedefaults:
            h = (lambda s: pushastar.matched_separation(
                pushastar.far_match, pushastar.manhattan_dist, s))
            self.finish(h, pushastar.AStar)
        else:
            self.finish() # We want to ask more questions
