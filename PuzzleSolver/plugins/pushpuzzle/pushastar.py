"""
Uses AStar to asynchronously solve a push puzzle.

"""

class PushAStar:
    """Asynchronously solves a puzzle."""
    
    def __init__(self, puzzle):
        self._puzzle = puzzle

    def begin(self):
        """Start the solving process."""
        
    def cancel(self):
        """Try to stop the solving process and return whether successful."""
        
        return True
        
    def solving(self):
        """Check if the solver is currently running."""
        
        return False
        
    def status(self):
        """Returns a dictionary containing the latest information."""
        
        return {}
        
    def result(self):
        """If the solver has completed, return directions/None. Raises IncompleteError otherwise."""
        
        return None
        
class IncompleteError(Exception):
    """Thrown when a result is requested and the operation is not yet complete."""