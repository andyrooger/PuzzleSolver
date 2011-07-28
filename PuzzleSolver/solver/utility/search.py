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
        self.closed.add(item[0])

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

    def __init__(self, state, goal, heuristic, expander, ProcessingSet=DictSortedUniqueSet):
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
            return bool(states) # did we add new states
        else:
            return states # could be goal or None

    def solve(self):
        """Solve the given problem."""

        while True:
            result = self.single_step()
            if result == None:
                return None
            elif not isinstance(result, bool):
                return self.generate_path(result)

class ServedAStar(AStar):
    """Like AStar but the procesing set becomes a server that serves a new item to processes each time one completes."""

    def __init__(self, state, goal, heuristic, expander, groupsize=2, ProcessingSet=DictSortedUniqueSet):
        AStar.__init__(self, state, goal, heuristic, expander, ProcessingSet)
        self.groupsize = groupsize
        self.statestore = {}

    def sending_state(self, state):
        """Convert the state for sending to workers."""

        s, cost, expected, parent = state
        if isinstance(parent, int):
            return state
        h = hash(parent)
        self.statestore[h] = parent
        return (s, cost, expected, h)

    def receiving_state(self, state):
        """Convert the state for receiving from workers."""

        s, cost, expected, h = state
        if isinstance(h, int):
            p = self.statestore[h]
            return self.receiving_state((s, cost, expected, p))
        elif h == None:
            return state
        else:
            return (s, cost, expected, self.receiving_state(h))

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
                state = self.sending_state(state)
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
                    return self.generate_path(self.receiving_state(goal))
        finally:
            while any(p.is_alive() for p in processes):
                if server_pipe.poll():
                    server_pipe.recv()
            server_pipe.close()
            worker_pipe.close()

def ProcessingSetManager(ProcessingSet):
    """Create a class that spawns a new process to control the class and acts as a proxy anywhere else."""

    class ProcessingSetManager:
        def __init__(self):
            #multiprocessing.current_process.name() # The one to delete with
            # create server process, add and take become clients
            self.server_pipe, self.client_pipe = multiprocessing.Pipe()
            self.lock = multiprocessing.Lock() # Every client locks, then send and wait for receive if necessary, then unlock
            self.processing = None
            self.manager = multiprocessing.Process(target=self.server)
            self.manager.start() # Runs independently and closes on finish()

        def server(self):
            """Serves items back and forth for client."""

            processing = ProcessingSet()
            while True:
                msg = self.server_pipe.recv()
                if msg == None:
                    self.server_pipe.send(processing)
                    return
                elif isinstance(msg, int):
                    for _ in range(msg):
                        try:
                            item = processing.take()
                        except KeyError:
                            item = None
                        self.server_pipe.send(item)
                else:
                    processing.add(msg)

        def finish(self):
            """Tells the manager to stop and make this act as a normal processing set."""

            with self.lock:
                self.client_pipe.send(None)
                self.processing = self.client_pipe.recv()
                self.manager.join()

        def add(self, item):
            if self.processing == None:
                with self.lock:
                    self.client_pipe.send(item)
            else:
                self.processing.add(item)

        def take(self):
            if self.processing == None:
                with self.lock:
                    self.client_pipe.send(1)
                    state = self.client_pipe.recv()
                    if state == None:
                        raise KeyError
                    else:
                        return state
            else:
                return self.processing.take()

    return ProcessingSetManager

class PulledAStar(AStar):
    """Like ServedAStar but processes pull when available rather than being served."""

    def __init__(self, state, goal, heuristic, expander, groupsize=2, ProcessingSet=DictSortedUniqueSet):
        AStar.__init__(self, state, goal, heuristic, expander, ProcessingSetManager(ProcessingSet))
        self.groupsize = groupsize
        self.statestore = {}

    def step_worker(self, itemsleft, wait_protector, finished, item_protector):
        """
        Keep performing single step until processing set is empty. Should use our remote manager set.

        itemsleft is an event that is set whenever states are added to our set and cleared whenever they cannot be retreived.
        wait_protector is a semaphore with initial value of groupsize-1 to allow all but one process to be waiting at once.
        finished says if we should quit
        item_protector is a lock so that we can ensure we only clear itemsleft if finished is untrue

        NOT COMPLETELY SAFE, IN RARE CASES WE COULD DO THINGS WE DO NOT MEAN TO!

        """

        while True:
            result = self.single_step()
            if isinstance(result, bool): # expanded a state
                if result: # Added a state
                    itemsleft.set()
            elif result == None: # empty state set
                if wait_protector.acquire(False): # Not all waiting
                    item_protector.acquire()
                    if not finished.is_set():
                        itemsleft.clear()
                    item_protector.release()
                    itemsleft.wait()
                    wait_protector.release()
                else: # All waiting
                    finished.set()
                    itemsleft.set() # to release the waiting processes
            else:
                # Goal, TODO: publish this somehow! 
                finished.set()
                itemsleft.set() # to release waiting processes

            if finished.is_set():
                return

    def solve(self):
        itemsleft = multiprocessing.Event()
        itemsleft.set()
        finished = multiprocessing.Event()
        wait_protector = multiprocessing.Semaphore(self.groupsize-1)
        item_protector = multiprocessing.Lock()

        processes = [multiprocessing.Process(target=self.step_worker, args=(itemsleft, wait_protector, finished, item_protector)) for _ in range(self.groupsize)]
        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()

        self.processing.finish() # kill manager process
        # TODO - receive results somehow
        return
