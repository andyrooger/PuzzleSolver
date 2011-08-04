"""
Solver for the push puzzle.

"""

import solver.plugin

class PushSolver(solver.plugin.Solver):
    """Solver for the PushPuzzle."""
    
    def __init__(self, pause, getpuzzle, finished):
        self._pause = pause
        self._getpuzzle = getpuzzle
        self._puzzle = None
        self._finished = finished
    
    def start(self):
        """Start the push puzzle solver."""
        
        self._pause(True)
        self.puzzle = self._getpuzzle()
    
    def stop(self):
        """Stop the push puzzle solver."""
        
        self._pause(False)
        self._finished([]) # return answer
        return True