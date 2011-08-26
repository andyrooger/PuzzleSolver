"""
Contains functions related to navigation of puzzles.

"""

import math

from solver.utility import astar
from . import directions

############################
#
# Distance Functions
#
############################

def manhattan_distance(a, b):
    """Get distance from a to b, moving in a grid."""
    
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def direct_distance(a, b):
    """Get distance from a to b, moving in a direct line."""
    return math.sqrt(a*a + b*b)

def path_distance(a, b, state):
    """Get distance from a to b, moving through the given puzzle as a player."""
    
    route = find_path(a, b, state)
    return None if route == None else len(route)

def box_path_distance(a, b, state):
    """Get distance from a to b, moving through the given puzzle as a box."""
    
    route = find_box_path(a, b, state)
    return None if route == None else len(route)

###############################
#
# Path finding
#
###############################

def can_move_player(state, pos, direction):
    """Can we move a player at pos in the given direction."""
    return directions.adjacent(pos, direction) in state.accessible

def can_move_box(state, pos, direction, ignore=None, ignoreall=False):
    """
    Can we move a box in the given direction? ...Assuming the player can push from
    there and the box exists. Similar to function in puzzle state but without check
    for player accessibility.
    """
    frm = directions.adjacent(pos, directions.opposite(direction))
    to = directions.adjacent(pos, direction)
    if ignoreall:
        return (state.base.empty_square(frm) and state.base.empty_square(to))
    else:
        return ((frm == ignore or state.cleared_square(frm))
                and (to == ignore or state.cleared_square(to)))

def player_path(state, to):
    """Find the path that the player should take to find 'to'"""
    
    return find_path(state.player, to, state)

def find_path(a, b, state):
    """
    Find the directions needed to navigate from a to b within state.
    
    Takes This will return None if the journey is not possible.
    
    """
    
    if not state.finalised:
        raise ValueError("State has not been finalised so we cannot path-find.")
    if b not in state.accessible:
        return None
    
    ok = (lambda pos: pos in state.accessible)
    
    def transitions(pos):
        #ds = [d for d in directions.DIRECTIONS if can_move_player(state, pos, d)]
        #return [(directions.adjacent(pos, d), d, 1) for d in ds]
        dirs = directions.adjacent(pos)
        return [(dirs[k], k, 1) for k in dirs if ok(dirs[k])]
    
    return astar.TransitionAStar(astar.AStar,
                                 a,
                                 (lambda pos: pos == b),
                                 (lambda pos: manhattan_distance(pos, b)),
                                 transitions).solve()

def find_box_path(a, b, state, ignore_boxes=True):
    """
    Find the directions needed to navigate a box from a to b within state.
    
    Takes This will return None if the journey is not possible.
    
    """
    
    def transitions(pos):
        ds = [d for d in directions.DIRECTIONS if
              can_move_box(state, pos, d, ignore=a, ignoreall=ignore_boxes)]
        return [(directions.adjacent(pos, d), d, 1) for d in ds]
    
    return astar.TransitionAStar(astar.AStar,
                                 a,
                                 (lambda pos: pos == b),
                                 (lambda pos: manhattan_distance(pos, b)),
                                 transitions).solve()

