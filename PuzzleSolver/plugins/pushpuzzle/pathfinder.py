"""
Use AStar utility to path find.

"""

from solver.utility import astar

# For a path finder, the state is (state, move to get here)

def manhattan_distance(frm, to):
    return abs(frm[0]-to[0]) + abs(frm[1]-to[1])

def state_path_finder(state, to):
    """Generate a path finder from a puzzle state (or None if to is not accessible)."""
    
    base = state.base
    if not state.finalised:
        raise ValueError("State has not been finalised so we cannot path-find.")
    if to not in state.accessible:
        return None
    
    initial = (state.player, None)
    goal = lambda pos: pos[0] == to
    heuristic = lambda pos: manhattan_distance(pos[0], to)
    def transitions(pos):
        pos_dir = [(base.adjacent(pos[0], dir), dir) for dir in ["UP", "DOWN", "LEFT", "RIGHT"]]
        return [(p, 1) for p in pos_dir if p[0] != None and p[0] in state.accessible]
    
    return astar.AStar(initial, goal, heuristic, transitions)

def find_path(state, to):
    """Find the path to the required location, returns a list of directions to the given point."""
    
    finder = state_path_finder(state, to)
    if finder == None:
        return None
    return [e[1] for e in finder.solve() if e[1] != None]