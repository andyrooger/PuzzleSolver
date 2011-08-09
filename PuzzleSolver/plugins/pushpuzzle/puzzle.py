"""
Contains the structures to store our puzzles in.

"""

class Puzzle:
    """Main class for storing our puzzles."""

    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.walls = set()
        self.targets = set()
        self._states = [PuzzleState(self)]
        self._curstate = 0

    def in_area(self, x, y):
        """Are the given coordinates within our range?"""

        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def adjacent(self, pos, direction):
        """Return the position adjacent to our position in the corresponding direction."""

        if direction == "UP":
            return (pos[0], pos[1]-1) if pos[1] > 0 else None
        elif direction == "DOWN":
            return (pos[0], pos[1]+1) if pos[1] < self.height-1 else None
        elif direction == "LEFT":
            return (pos[0]-1, pos[1]) if pos[0] > 0 else None
        elif direction == "RIGHT":
            return (pos[0]+1, pos[1]) if pos[0] < self.width-1 else None
        else:
            return None

    def valid(self, children=True):
        """Is this a valid setup?"""

        if not all(self.in_area(x, y) for x, y in self.walls.union(self.targets)):
            return False

        if children and not all(s.valid() for s in self._states):
            return False

        if self.walls.intersection(self.targets):
            return False

        if children and not all(len(self._states[0].boxes) == len(s.boxes) for s in self._states):
            return False

        return True

    def initial(self):
        """Get the initial puzzle state."""

        return self._states[0]

    def state(self):
        """Get the current puzzle state."""

        return self._states[self._curstate]

    def cursor(self, cur=None):
        if cur != None:
            if cur < 0 or cur >= len(self):
                raise IndexError
            self._curstate = cur
        return self._curstate

    def add_state(self, player=None):
        """
        Add a new state identical to the current after our current state and remove any following.
        
        If not done already, the current state is finalised. If player is given then the new state
        will be finalised and the only change will be the player. Otherwise it will be left
        unfinalised.
        
        """

        self.state().finalise()

        self._states[self._curstate+1:] = [self.state().copy(player)]
        self._curstate = len(self)-1

    def __len__(self):
        return len(self._states)

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self, parent):
        self.parent = parent
        self.player = None
        self.boxes = set()
        self.finalised = False

    # Allow finalisation
    def __setattr__(self, *vargs):
        if not hasattr(self, "finalised") or not self.finalised:
            super().__setattr__(*vargs)
        else:
            raise ValueError("Cannot edit a finalised puzzle state.")

    def finalise(self, freeze=True):
        if self.finalised:
            return
        self._record_accessibility()
        if freeze:
            self.boxes = frozenset(self.boxes)
        self.finalised = True

    def valid(self):
        if self.player == None or not self.parent.in_area(*self.player):
            return False

        if len(self.boxes) != len(self.parent.targets):
            return False

        if not all(self.parent.in_area(x, y) for (x, y) in self.boxes):
            return False

        if self.player in self.parent.walls.union(self.boxes):
            return False

        if self.boxes.intersection(self.parent.walls):
            return False

        return True
    
    def separation(self):
        """Return the total separation of the boxes from targets."""
        totalSeparation = 0
        targets = set(self.parent.targets)
        
        for box in self.boxes:
            nearestTarget = self.findNearest(targets,box)
            assert nearestTarget, "More boxes than targets"
            targets.discard(nearestTarget)
            totalSeparation += self.getDistance(nearestTarget,box)
            
        return totalSeparation
    
    def getDistance(self, object1, object2):
        xDist = object1[0]-object2[0]
        yDist = object1[1]-object2[1]
        return abs(xDist) + abs(yDist)
    
    def findNearest(self, rabbits, dog):
        if not rabbits:
            return None
        nearestRabbitDistance = min(self.getDistance(rabbit,dog) for rabbit in rabbits) 
        for rabbit in rabbits:
            if self.getDistance(rabbit,dog) == nearestRabbitDistance:
                return rabbit
            
        
    def _record_accessibility(self):
        """Create and record a set describing accessible coordinates from this state."""
        
        if self.player == None:
            self.accessible = frozenset()
            return

        accessible = set()
        # In an attempt to avoid hitting recursion limit
        tocheck = [self.player]
        while tocheck:
            pos = tocheck.pop()
            if not self.parent.in_area(*pos):
                continue
            if pos in accessible:
                continue
            if pos in self.parent.walls:
                continue
            if pos in self.boxes:
                continue
            accessible.add(pos)
            x, y = pos
            tocheck += [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        self.accessible = frozenset(accessible)

    def goal(self):
        """Have we achieved our goal?"""

        return self.parent.targets == self.boxes

    def copy(self, player=None):
        """
        Return an identical copy of this state.
        
        If we have not finalised this state first we will copy everything and
        possibly replace player. This could take up more memory than necessary.
        Otherwise:
        
        With no arguments this will return an identical but unfinalised
        version (so no 'accessible' attribute). This is best before big alterations
        of the state.
        
        If only the player should be changed then provide this as an argument and
        the new state will be efficiently finalised.
        
        """

        p = PuzzleState(self.parent)
        if not self.finalised:
            p.player = player or self.player
            p.boxes = set(self.boxes)
        elif player == None: # Don't finalise
            p.player = self.player
            p.boxes = set(self.boxes)
        else: # finalise
            p.player = player
            p.boxes = self.boxes # still frozen
            if player in self.accessible:
                p.accessible = self.accessible
                p.finalised = True
            else:
                p.finalise(freeze=False) # Don't need to freeze boxes
        return p
