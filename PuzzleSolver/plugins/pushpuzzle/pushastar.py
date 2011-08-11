"""
Uses AStar to solve a push puzzle.

"""

from solver.utility.astar import AStar
from plugins.pushpuzzle import directions
    
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

def solve(initial, heuristic=(lambda s: 0), solver=AStar, **kwargs):
    """Try to solve the puzzle from the initial state."""
    
    goal = (lambda state: state.goal())

    return solver(
        initial,
        goal,
        heuristic,
        transitions,
        **kwargs).solve()