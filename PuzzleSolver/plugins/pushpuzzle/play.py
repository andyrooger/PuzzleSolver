"""
View for Push Puzzle playing.

"""

import tkinter

import solver.plugin
from solver.utility.simpleframe import SimpleFrame

from . import style
from . playarea import PlayArea
from . pushsolver import PushSolver

class PlayView(solver.plugin.PuzzleView):
    """Functionality for Push Puzzle playing."""

    def __init__(self):
        solver.plugin.PuzzleView.__init__(self)
        self._frame = None

    def get_frame(self, master):
        self._frame = PlaceholderPlayFrame(master)
        return self._frame

    def can_solve(self):
        return True
    
    def get_solver(self):
        return self._frame.get_solver()

    def get_extension(self):
        return ".spp"

    def get_puzzle(self):
        return self._frame.get_puzzle()

    def changed(self):
        return self._frame.changed()

    def saved(self):
        self._frame.saved()

    def clean(self):
        self._frame.clean()

    def load(self, puzzle):
        return self._frame.load(puzzle)

class PlaceholderPlayFrame(SimpleFrame):
    """Like SimpleFrame but has a placeholder before a puzzle is loaded."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)

        self.set_content(tkinter.Label(self, text="No puzzle loaded yet."))

    def _puzzle_loaded(self):
        return isinstance(self.content, PlayFrame)

    def get_solver(self):
        if self._puzzle_loaded():
            return self.content.get_solver()
        else:
            return None

    def changed(self):
        return self.content.changed() if self._puzzle_loaded() else False

    def saved(self):
        if self._puzzle_loaded():
            self.content.saved()

    def get_puzzle(self):
        return self.content.get_puzzle() if self._puzzle_loaded() else None

    def clean(self):
        if self._puzzle_loaded():
            self.content.clean()

    def load(self, puzzle):
        try:
            p = PlayFrame(self, puzzle)
            self.set_content(p)
            return True
        except ValueError:
            return False

class PlayFrame(tkinter.Frame):
    """GUI for playing the game."""

    def __init__(self, master, puzzle):
        tkinter.Frame.__init__(self, master)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._changed = False
        self._playarea = PlayArea(self, puzzle, self._change) # Could throw valueerror
        self._playarea.grid(sticky="nsew", columnspan=2, row=1, column=0)

        def prev():
            self._playarea.prev()
            self._control_state()
        def next():
            self._playarea.next()
            self._control_state()
        self._prevarrow = tkinter.Button(self, image=style.load_icon("larrow"), command=prev)
        self._prevarrow.grid(sticky="nsew", row=0, column=0)
        self._nextarrow = tkinter.Button(self, image=style.load_icon("rarrow"), command=next)
        self._nextarrow.grid(sticky="nsew", row=0, column=1)

        self._status = tkinter.Label(self, text="")
        self._status.grid(sticky="nsew", row=2, column=0, columnspan=2)

        self.clean()

    def _control_state(self):
        """Set state for all controls."""

        self._prevarrow.config(state=(
            tkinter.NORMAL if self._playarea.hasprev() else tkinter.DISABLED
        ))
        self._nextarrow.config(state=(
            tkinter.NORMAL if self._playarea.hasnext() else tkinter.DISABLED
        ))

        info = self._playarea.metrics()
        self._status["text"] = "Targets: %(filled)s/%(targets)s  -  Moves: %(move)s/%(total)s" % info

    def get_solver(self):
        return PushSolver(self, self._playarea.automove)

    def changed(self):
        return self._changed

    def saved(self):
        self._changed = False

    def get_puzzle(self):
        return self._playarea.get_puzzle()

    def clean(self):
        self._playarea.rewind()
        self._control_state()

    def _change(self):
        """Called whenever the puzzle is edited."""

        self._changed = True
        self._control_state()
        
    def freeze(self, frozen):
        if frozen:
            self._prevarrow.config(state=tkinter.DISABLED)
            self._nextarrow.config(state=tkinter.DISABLED)
        else:
            self._control_state()
        self._playarea.freeze(frozen)
