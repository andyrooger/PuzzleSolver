"""
Solver for the push puzzle.

"""

# PuzzleSolver
# Copyright (C) 2010  Andy Gurden
#
#     This file is part of PuzzleSolver.
#
#     PuzzleSolver is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PuzzleSolver is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PuzzleSolver.  If not, see <http://www.gnu.org/licenses/>.

import tkinter
from tkinter import tix
import multiprocessing
import queue
import time

import solver.plugin
import solver.state
from solver.utility import process_exec, buttonselector, astar

from . import pushastar
from . import navigation

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
        
        if self._solver != None:
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
        self.resizable(False, False)
        
        tkinter.Label(self, text="Solver Type").grid(sticky="nsew", row=0, column=0)
        self._solver = buttonselector.ButtonSelector(self, vertical=True, selected=self._change_setting)
        self._solver.add("Basic A*", astar.AStar)
        self._solver.add("Parallel Symmetric A*", astar.SymmetricAStar)
        self._solver.add("Parallel Served A*", astar.ServedAStar)
        self._solver.add("Parallel Pulled A*", astar.PulledAStar)
        self._solver.grid(sticky="nsew", row=1, column=0)
        
        tkinter.Label(self, text="Num Processes").grid(sticky="nsew", row=0, column=1)
        self._processes = buttonselector.ButtonSelector(self, vertical=True, selected=self._change_setting)
        cpus = self._cpus()
        if cpus != None:
            self._processes.add("One per Core (%s)" % cpus, cpus)
        for i in [1, 2, 5, 10, 20]:
            self._processes.add(str(i), i)
        self._processes.grid(sticky="nsew", row=1, column=1)
        
        tkinter.Label(self, text="Heuristic").grid(sticky="nsew", row=0, column=2)
        self._heuristic = buttonselector.ButtonSelector(self, vertical=True, selected=self._change_setting)
        self._heuristic.add("Blind Matching", pushastar.blind_match)
        self._heuristic.add("Far Matching", pushastar.far_match)
        self._heuristic.add("Close Matching", pushastar.close_match)
        self._heuristic.add("Hungarian Matching", pushastar.munkres_value)
        self._heuristic.add("Shift Sum", pushastar.shift_sum)
        self._heuristic.grid(sticky="nsew", row=1, column=2)
        
        tkinter.Label(self, text="Distances").grid(sticky="nsew", row=0, column=3)
        self._distance = buttonselector.ButtonSelector(self, vertical=True, selected=self._change_setting)
        self._distance.add("Manhattan", navigation.manhattan_distance)
        self._distance.add("Direct", navigation.direct_distance)
        self._distance.add("Basic Path", navigation.box_basic_distance)
        self._distance.add("Box Path", navigation.box_path_distance)
        self._distance.grid(sticky="nsew", row=1, column=3)
        
        self._btns = tkinter.Frame(self)
        self._btns.columnconfigure(2, weight=1)
        tkinter.Button(self._btns, text="Reset to Defaults", command=self._defaults).grid(sticky="nsew", row=0, column=0)
        tkinter.Button(self._btns, text="Cancel", command=self._cancelled).grid(sticky="nsew", row=0, column=1)
        tkinter.Button(self._btns, text="Solve", command=self._solve).grid(sticky="nsew", row=0, column=2)
        self._btns.grid(sticky="nsew", columnspan=4, row=2, column=0)
        
        self._defaults()
            
    def _cpus(self):
        """Get number of CPUs or None."""
        
        try:
            return multiprocessing.cpu_count()
        except NotImplementedError:
            return None
    
    def _change_setting(self, change):
        """One of the settings has been changed."""
        
        self._processes.set_enabled(self._solver.selection() is not astar.AStar)
        self._distance.set_enabled(self._heuristic.selection() is not pushastar.shift_sum)
        
    def _cancelled(self):
        if solver.state.solving.change(None):
            self.destroy()
            
    def _defaults(self, choice=None):
        if choice is None:
            self._defaults(self._solver)
            self._defaults(self._processes)
            self._defaults(self._heuristic)
            self._defaults(self._distance)
        elif choice is self._solver:
            choice.selection(astar.ServedAStar)
        elif choice is self._processes:
            choice.selection(self._cpus() or 1) # cpus never 0 (I hope!)
        elif choice is self._heuristic:
            choice.selection(pushastar.munkres_value)
        elif choice is self._distance:
            choice.selection(navigation.box_path_distance)
        
    def _solve(self):
        # Just choosing the default for now
        conf = {"solver": self._solver.selection()}
        if conf["solver"] is None:
            return
        if conf["solver"] is not astar.AStar:
            conf["groupsize"] = self._processes.selection()
            if conf["groupsize"] is None:
                return
            
        conf["heuristic"] = self._heuristic.selection()
        if conf["heuristic"] is None:
            return
        if conf["heuristic"] is not pushastar.shift_sum:
            dist = self._distance.selection()
            if dist is None:
                return
            conf["heuristic"] = pushastar.matched_separation(conf["heuristic"], dist)
        
        self.destroy()
        self._done(**conf)
        
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
