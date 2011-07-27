"""
Helpful search algorithms for use by plugins.

"""

import multiprocessing

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

class DictSortedUniqueSet(DictSortedSet):
    """Like DictSortedSet but with an additional closed set."""

    def __init__(self):
        DictSortedSet.__init__(self)
        self.closed = set()

    def add(self, item):
        if item[0] in self.closed:
            return
        super().add(item)
        self.closed.add(item)

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

class ServedAStar(AStar):
    """Like AStar but the procesing set becomes a server that serves a new item to processes each time one completes."""

    def __init__(self, state, goal, heuristic, expander, groupsize=1, ProcessingSet=DictSortedSet):
        AStar.__init__(self, state, goal, heuristic, expander, ProcessingSet)
        self.groupsize = groupsize

    def step_worker(self, pipe, rlock, wlock):
        while True:
            with rlock:
                msg = pipe.recv()
            if msg == None:
                return
            next = self.next_states(msg)
            with wlock:
                pipe.send(next)

    def distribute_work(self, pipe, available):
        """Distribute as much work as possible and return number of processes left."""

        while available > 0:
            try:
                state = self.processing.take()
                pipe.send(state)
                available -= 1
            except KeyError:
                break
        return available

    def receive_results(self, pipe, available):
        """Receive all results and return either goal or None"""

        goal = None
        while pipe.poll():
            msg = pipe.recv()
            available += 1
            if isinstance(msg, list):
                for state in msg:
                    self.processing.add(state)
            else:
                goal = msg
        return (available, goal)

    def stop_processes(self, pipe, available):
        """Stop running processes."""

        for _ in range(self.groupsize-available):
            pipe.recv()

        for _ in range(self.groupsize):
            pipe.send(None)

    def solve(self):
        try:
            rlock = multiprocessing.Lock()
            wlock = multiprocessing.Lock()
            server_pipe, worker_pipe = multiprocessing.Pipe()
            waiting = self.groupsize
            processes = [multiprocessing.Process(target=self.step_worker, args=(worker_pipe, rlock, wlock)) for _ in range(self.groupsize)]
            for proc in processes:
                proc.start()
            while True:
                waiting = self.distribute_work(server_pipe, waiting)
                if waiting == self.groupsize:
                    self.stop_processes(server_pipe, waiting)
                    return None
                waiting, goal = self.receive_results(server_pipe, waiting)
                if goal != None:
                    self.stop_processes(server_pipe, waiting)
                    return goal
        finally:
            while any(p.is_alive() for p in processes):
                if server_pipe.poll():
                    server_pipe.recv()
            server_pipe.close()
            worker_pipe.close()
