"""
Concrete implementation of a plugin as an example.

"""

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
        self.i = _i
        _i += 1

    def name(self):
        """Get the name of the puzzle type."""
        return "Concrete " + str(self.i)

    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""
        return ConcreteView(mode, self.i)

class ConcreteView(solver.plugin.PuzzleView):
    """Functionality for a single mode."""

    def __init__(self, mode, i):
        solver.plugin.PuzzleView.__init__(self)
        self.mode = mode
        self.i = i
        self.data = tkinter.StringVar()
        self.changeValue("", False)

    def changeValue(self, text, needssaving=True):
        self.data.set(text)
        if not needssaving:
            self.oldval = text

    def get_frame(self, master):
        """Get the GUI frame."""
        fr = tkinter.Frame(master)
        fr.grid_rowconfigure(0, weight=1)
        fr.grid_columnconfigure(0, weight=1)
        tkinter.Label(fr, text="Hello I am " + str(self.i) + " and my mode is " + self.mode).grid(row=0, column=0, sticky="nsew")
        tkinter.Entry(fr, textvariable=self.data).grid(row=1, column=0, sticky="sew")
        self.status = tkinter.Frame(fr, width=50, background="GREEN")
        self.status.grid(row=0, column=1, rowspan=2, sticky="nse")
        return fr

    def can_solve(self):
        """Can we solve puzzles in this view."""
        return self.i > 4 and self.mode == "PLAY"

    def get_solver(self):
        """Get the solver for this view if one exists."""
        return ConcreteSolver(self.data, self.status) if self.can_solve() else None

    def get_extension(self):
        """Get either the file extension used to save the puzzles below, or None."""
        return ".con"

    def get_puzzle(self):
        """Get either the puzzle object if it can be saved, or None."""
        return self.data.get()

    def changed(self):
        """Was the puzzle changed since the last call to save."""
        return self.data.get() != self.oldval

    def saved(self):
        """Reset changed."""
        self.oldval = self.data.get()

    def clean(self):
        """Clean the view, removing all user changes."""
        self.changeValue("")

    def load(self, puzzle):
        """Load the given puzzle if possible and return if successful."""
        self.changeValue(str(puzzle), False)
        return True

class ConcreteSolver(solver.plugin.Solver):
    """Functionality for a puzzle solver, changed will be performed on the underlying view."""

    def __init__(self, var, status):
        solver.plugin.Solver.__init__(self)
        self.var = var
        self.status = status
        self.queue = multiprocessing.Queue()
        self.proc = None

    def start(self):
        """Start the solver."""

        self.proc = multiprocessing.Process(target=self.solve)
        self.proc.start()
        self.poll()

    def stop(self):
        """Stop the solver and return success (in stopping)."""

        return self.proc == None or not self.proc.is_alive()

    def poll(self): # Ergh
        if self.proc == None:
            return
        lastitem = None
        while True:
            try:
                lastitem = self.queue.get(False)

                if lastitem == False: # Done
                    self.proc.join()
                    self.proc = None
                    solver.state.solving.change(None)
                    return

                self.status.config(bg=lastitem)
            except queue.Empty:
                break

        self.status.after(10, self.poll)

    def solve(self):
        for _ in range(10):
            self.queue.put("RED")
            time.sleep(0.5)
            self.queue.put("ORANGE")
            time.sleep(0.5)
        self.queue.put("GREEN")
        self.queue.put(False)
