"""
Contains the structures to store our puzzles in.

"""

from . import directions

class Puzzle:
    """Main class for storing our puzzles."""
    
    def __init__(self, h, w):
        self.base = PuzzleDescription(h, w)
        self._states = [PuzzleState(self.base)]
        self._curstate = 0
        
    def valid(self, children=True):
        """Is this a valid setup?"""

        if not self.base.valid():
            return False

        if children:
            if not all(s.valid() for s in self._states):
                return False

            # All checked against targets in their individual valid functions
            #num_boxes = len(self.initial().boxes)
            #if not all(num_boxes == len(s.boxes) for s in self._states):
            #    return False

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

class PuzzleDescription:
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.walls = set()
        self.targets = set()

    def in_area(self, pos):
        """Are the given coordinates within our range?"""

        x, y = pos
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def valid(self, children=True):
        """Is this a valid setup?"""

        if not all(self.in_area(pos) for pos in self.walls.union(self.targets)):
            return False

        if self.walls.intersection(self.targets):
            return False

        return True

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self, base):
        self.base = base
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
        self._hash_obj = (min(self.accessible) if self.accessible else None, self.boxes)
        self.finalised = True

    def valid(self):
        if self.player == None or not self.base.in_area(self.player):
            return False

        if len(self.boxes) != len(self.base.targets):
            return False

        if not all(self.base.in_area(pos) for pos in self.boxes):
            return False

        if self.player in self.base.walls.union(self.boxes):
            return False

        if self.boxes.intersection(self.base.walls):
            return False

        return True

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
            if not self.base.in_area(pos):
                continue
            if pos in accessible:
                continue
            if pos in self.base.walls:
                continue
            if pos in self.boxes:
                continue
            accessible.add(pos)
            x, y = pos
            tocheck += [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        self.accessible = frozenset(accessible)

    def cleared_square(self, pos):
        """Is this a valid square with nothing on it."""
        
        return (self.base.in_area(pos) and
                pos not in self.boxes and
                pos not in self.base.walls)

    def can_move_box(self, box, direction):
        """Assuming box is a box, can we move it in the given direction?"""
        
        pushfrom = directions.adjacent(box, directions.opposite(direction))
        if pushfrom not in self.accessible:
            return False
        boxto = directions.adjacent(box, direction)
        if not self.cleared_square(boxto):
            return False
        
        return True

    def goal(self):
        """Have we achieved our goal?"""

        return self.base.targets == self.boxes

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

        p = PuzzleState(self.base)
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
                p._hash_obj = self._hash_obj
                p.finalised = True
            else:
                p.finalise(freeze=False) # Don't need to freeze boxes
        return p

    def __eq__(self, state):
        if isinstance(state, PuzzleState):
            assert self.finalised and state.finalised, "State was not finalised before comparison"
            return self._hash_obj.__eq__(state._hash_obj)
        else:
            return super().__eq__(state)
        
    def __ne__(self, state):
        if isinstance(state, PuzzleState):
            assert self.finalised, "State was not finalised before comparison."
            return self._hash_obj.__ne__(state._hash_obj)
        else:
            return super().__ne__(state)

    def __hash__(self):
        assert self.finalised, "State was not finalised before hashing"
        return self._hash_obj.__hash__()
