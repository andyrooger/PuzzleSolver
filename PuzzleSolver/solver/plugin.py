"""
Various base classes for plugins.

"""

import abc

class PuzzleType(metaclass=abc.ABCMeta):
    """Entire plugin."""

    @abc.abstractmethod
    def name(self):
        """Get the name of the puzzle type."""

    @abc.abstractmethod
    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""

class PuzzlePane(metaclass=abc.ABCMeta):
    """Functionality for a single mode."""

    @abc.abstractmethod
    def getFrame(self, master):
        """Get the GUI frame."""

    @abc.abstractmethod
    def start(self):
        """Get the GUI frame."""
