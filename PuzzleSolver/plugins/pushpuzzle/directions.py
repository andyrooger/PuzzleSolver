"""
Directions and relevant functions to avoid duplicating this functionality.

"""

# PuzzleSolver
# Copyright (C) 2010  Andy Gurden
#
#     This file is part of PuzzleSolver.
#
#     PuzzleSolver is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PuzzleSolver is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PuzzleSolver.  If not, see <http://www.gnu.org/licenses/>.

DIRECTIONS = {"UP", "DOWN", "LEFT", "RIGHT"}

def opposite(direction):
    """What's the opposite direction the current?"""
    
    return {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT"
    }[direction]
    
def adjacent(pos, direction=None):
    """What are the coordinates to the given direction from pos?"""
    
    if direction == None:
        return {dir: adjacent(pos, dir) for dir in DIRECTIONS}
    
    if direction == "UP":
        return (pos[0], pos[1]-1)
    elif direction == "DOWN":
        return (pos[0], pos[1]+1)
    elif direction == "LEFT":
        return (pos[0]-1, pos[1])
    elif direction == "RIGHT":
        return (pos[0]+1, pos[1])
    else:
        raise ValueError("Not a direction: " + str(direction))

def movement(a, b):
    """Which direction was the movement in, if multiple then this could return any valid."""
    
    if b[1] < a[1]:
        return "UP"
    elif b[1] > a[1]:
        return "DOWN"
    elif b[0] < a[0]:
        return "LEFT"
    elif b[0] > a[0]:
        return "RIGHT"
    else:
        return None
