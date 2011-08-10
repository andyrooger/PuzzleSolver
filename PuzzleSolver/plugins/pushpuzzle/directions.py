"""
Directions and relevant functions to avoid duplicating this functionality.

"""

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
