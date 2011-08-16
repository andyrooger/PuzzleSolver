"""
Contains functions related to navigation of puzzles.

"""

import math

from solver.utility import astar
from . import directions

def manhattan_distance(a, b):
    """Get distance from a to b, moving in a grid."""
    
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def direct_distance(a, b):
    """Get distance from a to b, moving in a direct line."""
    return math.sqrt(a*a + b*b)

def path_distance(a, b, state, boxes=False):
    """Get distance from a to b, moving through the given puzzle."""
    
    route = find_path(a, b, state, boxes)
    return None if route == None else len(route)

def player_path(state, to):
    """Find the path that the player should take to find 'to'"""
    
    return find_path(state.player, to, state, True)

def find_path(a, b, state, boxes=True):
    """
    Find the directions needed to navigate from a to b within state.
    
    boxes indicates whether the boxes should be taken into account when
    generating the path. This will return None if the journey is not
    possible.
    
    """
    
    if not state.finalised:
        raise ValueError("State has not been finalised so we cannot path-find.")
    if boxes and b not in state.accessible:
        return None
    
    if boxes:
        ok = (lambda pos: pos in state.accessible)
    else:
        ok = (lambda pos: pos not in state.base.walls and state.base.in_area(pos))
    
    def transitions(pos):
        dirs = directions.adjacent(pos)
        return [(dirs[k], k, 1) for k in dirs if ok(dirs[k])]
    
    return astar.TransitionAStar(astar.AStar,
                                 a,
                                 (lambda pos: pos == b),
                                 (lambda pos: manhattan_distance(pos, b)),
                                 transitions).solve()
