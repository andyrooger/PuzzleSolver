"""
Various base classes for plugins.

"""

import abc
import os

class PuzzleType(metaclass=abc.ABCMeta):
    """Entire plugin."""

    @abc.abstractmethod
    def name(self):
        """Get the name of the puzzle type."""

    @abc.abstractmethod
    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""

class PuzzleView(metaclass=abc.ABCMeta):
    """Functionality for a single mode."""

    @abc.abstractmethod
    def getFrame(self, master):
        """Get the GUI frame."""

    @abc.abstractmethod
    def canSolve(self):
        """Can we solve puzzles in this view."""

    @abc.abstractmethod
    def getSolver(self):
        """Get the solver for this view if one exists."""

    @abc.abstractmethod
    def getExtension(self):
        """Get either the file extension used to save the puzzles below, or None"""

    @abc.abstractmethod
    def getPuzzle(self):
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

def find_plugins(module):
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

    plugins = list(find_plugins(module))
    if not plugins:
        return []
    else:
        m = __import__(module.__name__, globals(), locals(), fromlist=plugins)
        mods = (getattr(m, p, None) for p in plugins)
        return [getattr(m, "Puzzle") for m in mods if hasattr(m, "Puzzle")]
