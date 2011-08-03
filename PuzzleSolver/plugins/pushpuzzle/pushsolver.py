"""
Solver for the push puzzle.

"""

class PushSolver:
    """Solver for the PushPuzzle."""
    
    def __init__(self, pause):
        self._pause = pause
    
    def start(self):
        """Start the push puzzle solver."""
        
        self._pause(True)
    
    def stop(self):
        """Stop the push puzzle solver."""
        
        self._pause(False)
        return True