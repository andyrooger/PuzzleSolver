"""
Use AStar utility to path find.

"""

from solver.utility import astar

from . import directions

# For a path finder, the state is (state, move to get here)

def manhattan_distance(frm, to):
    return abs(frm[0]-to[0]) + abs(frm[1]-to[1])

def state_path_finder(state, to):
    """Generate a path finder from a puzzle state (or None if to is not accessible)."""
    
    if not state.finalised:
        raise ValueError("State has not been finalised so we cannot path-find.")
    if to not in state.accessible:
        return None
    
    def transitions(pos):
        dirs = directions.adjacent(pos)
        return [(dirs[k], k, 1) for k in dirs if dirs[k] in state.accessible]
    
    return astar.TransitionAStar(astar.AStar,
                                 state.player,
                                 (lambda pos: pos == to),
                                 (lambda pos: manhattan_distance(pos, to)),
                                 transitions).solve()

def find_path(state, to):
    """Find the path to the required location, returns a list of directions to the given point."""
    
    return state_path_finder(state, to)
