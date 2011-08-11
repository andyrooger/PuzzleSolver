"""
Uses AStar to asynchronously solve a push puzzle.

"""

from solver.utility.astar import AStar
from astartest import goal, transitions
from solver.utility import process_exec
from plugins.pushpuzzle import directions

class PushAStar:
    """Asynchronously solves a puzzle."""
    
    def __init__(self, puzzle, solver_class=AStar, **extra_args):
        self._puzzle = puzzle
        self._solver_class = solver_class
        self._solver_args = extra_args
        self._solver_process = None

    def begin(self):
        """Start the solving process."""
        
        assert self._solver_process == None, "Solver already running."
        
        self._solver_process = process_exec.ProcessExecutor(
            self._solve_worker, self._puzzle.state()
        )
        self._solver_process.start()
        
    def _solve_worker(self, initial):
        def goal(state):
            return state.goal()
        
        def heuristic(state):
            return 0
        
        def transitions(state):
            for box in state.boxes:
                for dir in directions.DIRECTIONS:
                    if state.can_move_box(box, dir):
                        new_state = state.copy()
                        new_state.boxes.remove(box)
                        new_state.boxes.add(directions.adjacent(box, dir))
                        new_state.player = box
                        new_state.finalise()
                        yield (new_state, 1) # TODO maybe work out real distance?
        
        return self._solver_class(initial, goal, heuristic, transitions, **self._solver_args).solve()
        
    def cancel(self):
        """Try to stop the solving process and return whether successful."""
        
        if self._solver_process != None:
            # TODO: Terminate properly, do not orphan children!
            self._solver_process.cancel()
            self._solver_process = None
        
        return True
        
    def solving(self):
        """Check if the solver is currently running."""
        
        if self._solver_process != None:
            return self._solver_process.working()
        return False
        
    def status(self):
        """Returns a dictionary containing the latest information."""
        
        return {}
        
    def result(self):
        """If the solver has completed, return directions/None. Raises IncompleteError otherwise."""
        
        if self._solver_process != None:
            try:
                return self._solver_process.result()
            except process_exec.IncompleteError:
                pass
        
        raise IncompleteError
        
class IncompleteError(Exception):
    """Thrown when a result is requested and the operation is not yet complete."""