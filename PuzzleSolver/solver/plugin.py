"""
Various base classes for plugins.

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

import abc
import os
import tkinter

class PuzzleType(metaclass=abc.ABCMeta):
    """Entire plugin."""

    def __init__(self):
        """Just here to avoid complains by PyDev in derived classes."""

    @abc.abstractmethod
    def name(self):
        """Get the name of the puzzle type."""

    @abc.abstractmethod
    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""

class PuzzleView(metaclass=abc.ABCMeta):
    """Functionality for a single mode."""

    def __init__(self):
        """Here to avoid complaints in subclasses."""

    @abc.abstractmethod
    def get_frame(self, master):
        """Get the GUI frame."""

    @abc.abstractmethod
    def can_solve(self):
        """Can we solve puzzles in this view."""

    @abc.abstractmethod
    def get_solver(self):
        """Get the solver for this view if one exists."""

    @abc.abstractmethod
    def get_extension(self):
        """Get either the file extension used to save the puzzles below, or None"""

    @abc.abstractmethod
    def get_puzzle(self):
        """Get either the puzzle object if it can be saved, or None."""

    @abc.abstractmethod
    def changed(self):
        """Was the puzzle changed since the last call to save."""

    @abc.abstractmethod
    def saved(self):
        """Reset changed."""

    @abc.abstractmethod
    def clean(self):
        """Clean the view, removing all user changes."""

    @abc.abstractmethod
    def load(self, puzzle):
        """Load the given puzzle if possible and return if successful."""

class Solver(metaclass=abc.ABCMeta):
    """Functionality for a puzzle solver, changed will be performed on the underlying view."""

    def __init__(self):
        """Avoids complaints from subclasses."""

    @abc.abstractmethod
    def start(self):
        """Start the solver."""

    @abc.abstractmethod
    def stop(self):
        """Stop the solver and return success (in stopping)."""


def _find_plugins(module):
    """Find all plugin names for the given package."""

    mod_names = set()
    for path in module.__path__:
        if os.path.isdir(path):
            mod_files = os.listdir(path)
            for file in mod_files:
                if file.endswith(".py") and file != "__init__.py":
                    mod_names.add(file[:-3])
    return mod_names

def load_plugins(module):
    """Load all the plugins inside module."""

    plugins = list(_find_plugins(module))
    if not plugins:
        return []
    else:
        m = __import__(module.__name__, globals(), locals(), fromlist=plugins)
        mods = (getattr(m, p, None) for p in plugins)
        return [getattr(m, "Puzzle") for m in mods if hasattr(m, "Puzzle")]

class DummyView(PuzzleView):
    """Functionality for a single mode."""

    def __init__(self):
        PuzzleView.__init__(self)
        self._puzzle = None

    def get_frame(self, master):
        return tkinter.Label(master, text="No puzzle type is currently selected.")

    def can_solve(self): return False
    def get_solver(self): return None
    def get_extension(self): return None
    def get_puzzle(self): return self._puzzle
    def changed(self): return False
    def saved(self): pass
    def clean(self): self._puzzle = None

    def load(self, puzzle):
        self._puzzle = puzzle
        return True
