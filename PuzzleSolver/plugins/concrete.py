"""
Concrete implementation of a plugin as an example.

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
import multiprocessing
import queue
import time

import solver.plugin
import solver.state

_i = 0

class Puzzle(solver.plugin.PuzzleType):
    """Entire plugin."""

    def __init__(self):
        global _i
        solver.plugin.PuzzleType.__init__(self)
        self._i = _i
        _i += 1

    def name(self):
        """Get the name of the puzzle type."""
        return "Concrete " + str(self._i)

    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""
        return ConcreteView(mode, self._i)

class ConcreteView(solver.plugin.PuzzleView):
    """Functionality for a single mode."""

    def __init__(self, mode, i):
        solver.plugin.PuzzleView.__init__(self)
        self._mode = mode
        self._i = i
        self._data = tkinter.StringVar()
        self._change_value("", False)

    def _change_value(self, text, needssaving=True):
        self._data.set(text)
        if not needssaving:
            self._oldval = text

    def get_frame(self, master):
        """Get the GUI frame."""
        fr = tkinter.Frame(master)
        fr.grid_rowconfigure(0, weight=1)
        fr.grid_columnconfigure(0, weight=1)
        tkinter.Label(fr, text="Hello I am " + str(self._i) + " and my mode is " + self._mode).grid(row=0, column=0, sticky="nsew")
        tkinter.Entry(fr, textvariable=self._data).grid(row=1, column=0, sticky="sew")
        self._status = tkinter.Frame(fr, width=50, background="GREEN")
        self._status.grid(row=0, column=1, rowspan=2, sticky="nse")
        return fr

    def can_solve(self):
        """Can we solve puzzles in this view."""
        return self._i > 4 and self._mode == "PLAY"

    def get_solver(self):
        """Get the solver for this view if one exists."""
        return ConcreteSolver(self._data, self._status) if self.can_solve() else None

    def get_extension(self):
        """Get either the file extension used to save the puzzles below, or None."""
        return ".con"

    def get_puzzle(self):
        """Get either the puzzle object if it can be saved, or None."""
        return self._data.get()

    def changed(self):
        """Was the puzzle changed since the last call to save."""
        return self._data.get() != self._oldval

    def saved(self):
        """Reset changed."""
        self._oldval = self._data.get()

    def clean(self):
        """Clean the view, removing all user changes."""
        self._change_value("")

    def load(self, puzzle):
        """Load the given puzzle if possible and return if successful."""
        self._change_value(str(puzzle), False)
        return True

class ConcreteSolver(solver.plugin.Solver):
    """Functionality for a puzzle solver, changed will be performed on the underlying view."""

    def __init__(self, var, status):
        solver.plugin.Solver.__init__(self)
        self._var = var
        self._status = status
        self._queue = multiprocessing.Queue()
        self._proc = None

    def start(self):
        """Start the solver."""

        self._proc = multiprocessing.Process(target=self._solve)
        self._proc.start()
        self._poll()

    def stop(self):
        """Stop the solver and return success (in stopping)."""

        return self._proc == None or not self._proc.is_alive()

    def _poll(self): # Ergh
        if self._proc == None:
            return
        lastitem = None
        while True:
            try:
                lastitem = self._queue.get(False)

                if lastitem == False: # Done
                    self._proc.join()
                    self._proc = None
                    solver.state.solving.change(None)
                    return

                self._status.config(bg=lastitem)
            except queue.Empty:
                break

        self._status.after(10, self._poll)

    def _solve(self):
        for _ in range(10):
            self._queue.put("RED")
            time.sleep(0.5)
            self._queue.put("ORANGE")
            time.sleep(0.5)
        self._queue.put("GREEN")
        self._queue.put(False)
