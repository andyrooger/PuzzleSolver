"""
Solver for the push puzzle.

"""

import tkinter
from tkinter import tix
import multiprocessing
import queue
import time

import solver.plugin
import solver.state
from solver.utility import process_exec, simpleframe, buttonselector, astar

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
            self._solver = PushProcess(
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
        
        self._status = tkinter.Label(self, text="Solving...")
        self._status.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self._progress = tix.Meter(self, text="Not started")
        self._progress.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self._time = tkinter.Label(self, text="Not started")
        self._time.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        self._demo = tkinter.Button(self, text="Demonstrate", command=self.demo, state=tkinter.DISABLED)
        self._demo.grid(row=3, column=0)
        tkinter.Button(self, text="Cancel", command=self.cancel).grid(row=3, column=1)
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
            self._progress.config(text="Done", value=1)
            try:
                if self._solver.result() == None:
                    self._status.config(text="No solution found")
                else:
                    self._demo.config(state=tkinter.NORMAL)
            except process_exec.IncompleteError:
                self._status.config(text="Something went horribly wrong!")
        else:
            self._update_pipe_stats()
            self.after(500, self._periodic_update)
        self._update_time()
            
    def _update_pipe_stats(self):
        cnt, cur, total = self._solver.status()
        self._status.config(text=("Processed %i states." % cnt))
        prop = 0 if total == 0 else cur/total
        self._progress.config(text="At %i of %i Expected..." % (cur, total), value=prop)
    
    def _update_time(self):
        t = self._solver.runtime()
        if self._solver.working():
            self._time.config(text="Time elapsed: %.3fs" % t)
        else:
            self._time.config(text="Completed in %.3fs" % t)

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
        selector = buttonselector.ButtonSelector(self._content, vertical=True, selected=callback)
        for a, obj in answers:
            selector.add(a, obj)
        self._content.set_content(selector)
        
    def finish(self, *vargs, **kwargs):
        """Spit out the given solver arguments."""
        
        self.destroy()
        self._done(*vargs, **kwargs)
        
    def _ask_initial(self):
        def cb(usedefaults):
            if usedefaults:
                h = (lambda s: pushastar.matched_separation(
                    pushastar.far_match, pushastar.manhattan_dist, s))
                self.finish(heuristic=h, solver=astar.ServedAStar)
            else:
                self._ask_solver()
        self.ask("Would you like to use solver defaults or manage this by your self?",
                 [
                  ("Use Defaults", True),
                  ("Configure on my Own.", False)
                 ], callback=cb)
        
    def _ask_solver(self):
        def cb(solver):
            kwargs = {"solver": solver}
            if solver is astar.AStar:
                self._ask_heuristic(kwargs)
            else:
                self._ask_processes(kwargs)
            
        self.ask("What type of solver do you want to use?",
                 [
                  ("Basic A*", astar.AStar),
                  ("Parallel Symmetric A*", astar.SymmetricAStar),
                  ("Parallel Served A*", astar.ServedAStar),
                  ("Parallel Pulled A*", astar.PulledAStar)
                 ], callback=cb)
        
    def _ask_processes(self, kwargs):
        def cb(num):
            kwargs["groupsize"] =  num
            self._ask_heuristic(kwargs)
        
        proc_ans = [(str(x), x) for x in [1, 2, 5, 10, 20]]
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            pass
        else:
            proc_ans.insert(0, ("One per Core (%s)" % cpus, cpus))
        self.ask("How many processes do you want to run?",
                 proc_ans, callback=cb)
    
    def _ask_heuristic(self, kwargs):
        def cb(heuristic):
            if heuristic is pushastar.shift_sum:
                kwargs["heuristic"] = heuristic
                self.finish(**kwargs)
            else:
                self._ask_dist(kwargs, heuristic)
        self.ask("Which heuristic would you like to use?",
                 [
                  ("Blind Matching", pushastar.blind_match),
                  ("Far Matching", pushastar.far_match),
                  ("Close Matching", pushastar.close_match),
                  ("Hungarian Matching", pushastar.munkres_value),
                  ("Shift Sum", pushastar.shift_sum)
                 ], callback=cb)
        
    def _ask_dist(self, kwargs, heuristic):
        def cb(dist):
            self._ask_setpriority(kwargs, heuristic, dist)
        self.ask("Which distance function would you like to use?",
                 [
                  ("Manhattan", pushastar.manhattan_dist),
                  ("Direct", pushastar.direct_dist),
                  ("Actual Path", pushastar.path_dist)
                 ], callback=cb)
        
    def _ask_setpriority(self, kwargs, heuristic, dist):
        def cb(priority):
            kwargs["heuristic"] = (lambda s:
                pushastar.matched_separation(heuristic, dist, s, priority))
            self.finish(**kwargs)
        self.ask("Which set should be the primary set?",
                 [
                  ("Boxes", True),
                  ("Targets", False)
                 ], callback=cb)
        
class PushProcess(process_exec.ProcessExecutor):
    """Process executor for solving a push puzzle."""
    
    def __init__(self, initial, *vargs, **kwargs):
        self._reports = multiprocessing.Queue() # For status updates
        self._timer = None
        self._worker = self._timed(self._worker)
        process_exec.ProcessExecutor.__init__(self,
            pushastar.solve,
            initial,
            *vargs, reporting=self._reports, **kwargs)
        self._store_count = 0
        self._current_cost = 0
        self._current_total = 0

    def status(self):
        msg = None
        try:
            while True:
                msg = self._reports.get(False)
                self._store_count += 1 # If failed we already left
        except queue.Empty:
            pass
        
        if msg != None:
            self._current_cost = msg[0]
            self._current_total = msg[1]
        
        return (self._store_count, self._current_cost, self._current_total)
    
    def runtime(self):
        if self._timer == None:
            return 0
        else:
            t = self._timer.value
            if t >= 0:
                return time.time() - t
            else:
                return -t
    
    def _timed(self, f):
        self._timer = multiprocessing.Value('d', 0)
        timer = self._timer
        def new_f(*vargs, **kwargs):
            timer.value = time.time()
            f(*vargs, **kwargs)
            timer.value -= time.time() # negative to say done
        return new_f
