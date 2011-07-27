"""
Helpful search algorithms for use by plugins.

"""

# TODO - make sure states aren't added twice and identical STATEs only keep the best expected, higher cost comes before lower (if the expected is the same)
class DictSortedSet:
    """Orders states using various levels of dicts."""

    def __init__(self):
        self.open = {}

    def add(self, item):
        state, cost, expected, _ = item # split parts

        if expected not in self.open: # expected cost level
            self.open[expected] = {}
        e_dict = self.open[expected]
        if cost not in e_dict: # current cost level
            e_dict[cost] = set()
        e_dict[cost].add(item)

    def take(self):
        if not self.open: # no states left
            raise KeyError
        min_exp = min(k for k in self.open) # smallest expected
        e_dict = self.open[min_exp]
        max_cost = max(k for k in e_dict) # largest current
        item = e_dict[max_cost].pop()
        if not e_dict[max_cost]: # remove current level
            del e_dict[max_cost]
        if not e_dict: # remove empty expected level
            del self.open[min_exp]
        return item

class BasicSet:
    """Uses set for the most basic implementation of our set."""

    def __init__(self):
        self.collection = set()

    def add(self, item):
        self.collection.add(item)

    def take(self): # raises key error if none exists
        return self.collection.pop()

class AStar:
    """Provides an implementation for the A* algorithm."""

    def __init__(self, state, goal, heuristic, expander, ProcessingSet=DictSortedSet):
        self.goal = goal
        self.heuristic = heuristic
        self.expander = expander
        self.processing = ProcessingSet()
        self.processing.add((state, 0, self.heuristic(state), None))

    def generate_path(self, state):
        states = []
        while state != None:
            s, _1, _2, p = state
            states.append(s)
            state = p
        states.reverse()
        return states

    def next_states(self, state=None):
        """Generate the next states from the current."""

        if state == None:
            try:
                best_full = self.processing.take()
            except KeyError:
                return None # Empty processing set
        else:
            best_full = state
        (best, cost, _1, _2) = best_full
        if self.goal(best):
            return best_full # Got answer
        else:
            return [(state, cost+c, cost+c+self.heuristic(state), best_full) for state, c in self.expander(best)]

    def single_step(self):
        """Take a single item if possible and expand or return the answer."""

        states = self.next_states()
        if isinstance(states, list):
            for n in states:
                self.processing.add(n)
            return True
        elif states == None:
            return None
        else:
            return self.generate_path(states) # Go answer

    def solve(self):
        """Solve the given problem."""

        while True:
            result = self.single_step()
            if result == None:
                return None
            elif result != True:
                return result
