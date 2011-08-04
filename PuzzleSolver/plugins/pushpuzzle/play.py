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
        self.frame = None

    def get_frame(self, master):
        self.frame = PlaceholderPlayFrame(master)
        return self.frame

    def can_solve(self):
        return self.frame.can_solve()
    
    def get_solver(self):
        return self.frame.get_solver()

    def get_extension(self):
        return ".spp"

    def get_puzzle(self):
        return self.frame.get_puzzle()

    def changed(self):
        return self.frame.changed()

    def saved(self):
        self.frame.saved()

    def clean(self):
        self.frame.clean()

    def load(self, puzzle):
        return self.frame.load(puzzle)

class PlaceholderPlayFrame(SimpleFrame):
    """Like SimpleFrame but has a placeholder before a puzzle is loaded."""

    def __init__(self, master):
        SimpleFrame.__init__(self, master)

        self.set_content(tkinter.Label(self, text="No puzzle loaded yet."))

    def puzzleLoaded(self):
        return isinstance(self.content, PlayFrame)

    def can_solve(self):
        return self.puzzleLoaded()

    def get_solver(self):
        if self.puzzleLoaded():
            return self.content.get_solver()
        else:
            return None

    def changed(self):
        return self.content.changed() if self.puzzleLoaded() else False

    def saved(self):
        if self.puzzleLoaded():
            self.content.saved()

    def get_puzzle(self):
        return self.content.get_puzzle() if self.puzzleLoaded() else None

    def clean(self):
        if self.puzzleLoaded():
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
        self.playarea = PlayArea(self, puzzle, self.change) # Could throw valueerror
        self.playarea.grid(sticky="nsew", columnspan=2, row=1, column=0)

        def prev():
            self.playarea.prev()
            self.controlState()
        def next():
            self.playarea.next()
            self.controlState()
        self.prevarrow = tkinter.Button(self, image=style.loadIcon("larrow"), command=prev)
        self.prevarrow.grid(sticky="nsew", row=0, column=0)
        self.nextarrow = tkinter.Button(self, image=style.loadIcon("rarrow"), command=next)
        self.nextarrow.grid(sticky="nsew", row=0, column=1)

        self.status = tkinter.Label(self, text="")
        self.status.grid(sticky="nsew", row=2, column=0, columnspan=2)

        self.clean()

    def controlState(self):
        """Set state for all controls."""

        self.prevarrow.config(state=(
            tkinter.NORMAL if self.playarea.hasprev() else tkinter.DISABLED
        ))
        self.nextarrow.config(state=(
            tkinter.NORMAL if self.playarea.hasnext() else tkinter.DISABLED
        ))

        info = self.playarea.metrics()
        self.status["text"] = "Targets: %(filled)s/%(targets)s  -  Moves: %(move)s/%(total)s" % info

    def get_solver(self):
        return PushSolver(self.freeze)

    def changed(self):
        return self._changed

    def saved(self):
        self._changed = False

    def get_puzzle(self):
        return None # TODO - maybe

    def clean(self):
        self.playarea.rewind()
        self.controlState()

    def change(self):
        """Called whenever the puzzle is edited."""

        self._changed = True
        self.controlState()
        
    def freeze(self, frozen):
        if frozen:
            self.prevarrow.config(state=tkinter.DISABLED)
            self.nextarrow.config(state=tkinter.DISABLED)
        else:
            self.controlState()
        self.playarea.freeze(frozen)
