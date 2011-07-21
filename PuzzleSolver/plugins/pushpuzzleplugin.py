"""
Plugin for the Sun Push Puzzle demo given in the old J2ME SDK.

"""

import solver.plugin

from . pushpuzzle import play, create, unknown

class Puzzle(solver.plugin.PuzzleType):
    """Entire plugin."""

    def __init__(self):
        solver.plugin.PuzzleType.__init__(self)

    def name(self):
        """Get the name of the puzzle type."""
        return "Sun Push Puzzle"

    def get(self, mode):
        """Get the a new puzzle pane for the given mode."""
        if mode == "CREATE":
            return create.CreateView()
        elif mode == "PLAY":
            return play.PlayView()
        else:
            return unknown.UnknownView(mode)
