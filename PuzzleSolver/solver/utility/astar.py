"""
Helpful search algorithms for use by plugins.

"""

import multiprocessing
import queue

from . import sync

###############################################################
#
# Storage for A* implementations
#
###############################################################

class UsefulStorage:
    """Saves implementing certain functions in storage classes."""

    def record(self, state, parent):
        self.add_state(state)
        self.add_parent(state, parent)

    def record_all(self, states, parent):
        for s in states:
            self.record(s, parent)

class LayeredAStarStorage(UsefulStorage):
    """Orders states using various levels of dicts."""

    def __init__(self):
        self.open = {}
        self.parents = {}

    def add_parent(self, state, parent):
        s, cost, _2 = state
        # only record one parent for each state, can cause recursive lookup if we choose the wrong one, so always choose shortest
        try:
            if cost >= self.parents[s][1]:
                return # old value was better
        except KeyError:
            pass # not in yet
        self.parents[s] = (parent, cost)

    def add_state(self, item):
        _, cost, expected = item # split parts

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

    def parent(self, state):
        return self.parents[state]

class UniqueLayeredAStarStorage(LayeredAStarStorage):
    """Like DictSortedSet using parents as a closed set."""

    def __init__(self):
        LayeredAStarStorage.__init__(self)

    def add_state(self, item):
        if item[0] in self.parents:
            return
        super().add_state(item)


class BasicAStarStorage(UsefulStorage):
    """Uses set for the most basic implementation of our set."""

    def __init__(self):
        self.collection = set()
        self.parents = {}

    def add_parent(self, state, parent):
        s, cost, _2 = state
        self.parents[s] = (parent, cost)

    def add_state(self, item):
        self.collection.add(item)

    def take(self): # raises key error if none exists
        return self.collection.pop()

    def parent(self, state):
        return self.parents[state]

def StorageManager(Storage):
    """Create a class that spawns a new process to control the class and acts as a proxy anywhere else."""

    class StorageManager:
        def __init__(self):
            #multiprocessing.current_process.name() # The one to delete with
            # create server process, add and take become clients
            self.server_pipe, self.client_pipe = multiprocessing.Pipe()
            self.lock = multiprocessing.Lock() # Every client locks, then send and wait for receive if necessary, then unlock
            self.storage = None
            self.manager = multiprocessing.Process(target=self.server)
            self.manager.start() # Runs independently and closes on finish()

        def server(self):
            """Serves items back and forth for client."""

            storage = Storage()
            while True:
                msg = self.server_pipe.recv()
                if msg == None:
                    self.server_pipe.send(storage)
                    return
                elif len(msg) == 2:
                    storage.record_all(msg[0], msg[1])
                elif len(msg) == 1:
                    p = storage.parent(msg[0])
                    self.server_pipe.send(p)
                else: # len(msg) == 0
                    try:
                        item = storage.take()
                    except KeyError:
                        item = None
                    self.server_pipe.send(item)

        def finish(self):
            """Tells the manager to stop and make this act as a normal processing set."""

            with self.lock:
                self.client_pipe.send(None)
                self.storage = self.client_pipe.recv()
                self.manager.join()

        def record(self, state, parent):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send(([state], parent))
            else:
                self.storage.record(state, parent)

        def record_all(self, states, parent):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send((states, parent))
            else:
                self.storage.record_all(states, parent)

        def take(self):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send(())
                    msg = self.client_pipe.recv()
                    if msg == None:
                        raise KeyError
                    else:
                        return msg
            else:
                return self.storage.take()

        def parent(self, state):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send((state,))
                    return self.client_pipe.recv()
            else:
                return self.storage.parent(state)

    return StorageManager

def PreparedStorageManager(Storage):
    """Like StorageManager but prepares for the next take early."""

    class PreparedStorageManager(StorageManager(Storage)):
        def __init__(self):
            super().__init__()
            self.waiting_item = None

        def server(self):
            """Serves items back and forth for client."""

            storage = Storage()
            while True:
                msg = self.server_pipe.recv()
                if msg == None:
                    self.server_pipe.send(storage)
                    return
                elif len(msg) == 3:
                    storage.record_all(msg[0], msg[1])
                    if msg[2]:
                        self.send_take(storage)
                elif len(msg) == 1:
                    p = storage.parent(msg[0])
                    self.server_pipe.send(p)
                else: # len(msg) == 0
                    self.send_take(storage)

        def send_take(self, storage):
            try:
                item = storage.take()
            except KeyError:
                item = None
            self.server_pipe.send(item)

        def record(self, state, parent):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send(([state], parent, False))
            else:
                self.storage.record(state, parent)

        def record_all(self, states, parent):
            if self.storage == None:
                with self.lock:
                    self.client_pipe.send((states, parent, True))
                    new_state = self.client_pipe.recv()
# Sending back won't work, we shouldn't ever need to though
#                    if self.waiting_item != None: # if we got one already, send it back
#                        self.client_pipe.send((new_state], parent))
                    self.waiting_item = new_state
            else:
                self.storage.record_all(states, parent)

        def take(self):
            if self.storage == None:
                with self.lock:
                    if self.waiting_item != None:
                        item = self.waiting_item
                        self.waiting_item = None
                        return item
                    self.client_pipe.send(())
                    msg = self.client_pipe.recv()
                    if msg == None:
                        raise KeyError
                    else:
                        return msg
            else:
                return self.storage.take()

    return PreparedStorageManager

BestStorage=UniqueLayeredAStarStorage

###############################################################
#
# Actual A* implementations
#
###############################################################

class AStar:
    """Provides an implementation for the A* algorithm."""

    def __init__(self, state, goal, heuristic, expander, Storage=BestStorage):
        self.goal = goal
        self.heuristic = heuristic
        self.expander = expander
        self.storage = Storage() # Collects and returns full_state
        self.storage.record((state, 0, self.heuristic(state)), None)

    def generate_path(self, state):
        """Generate the states leading to our goal given a minimal state."""

        states = []
        while state != None:
            states.append(state)
            state, _ = self.storage.parent(state)
        states.reverse()
        return states

    def next_states(self, parent):
        """Generate the next full states from the current full state."""

        (s, cost, _1) = parent
        if self.goal(s):
            return s # Got answer
        else:
            return [(state, cost+c, cost+c+self.heuristic(state)) for state, c in self.expander(s)]

    def single_step(self):
        """Take a single state from the set if possible and expand or return the answer."""

        try:
            best_full = self.storage.take()
        except KeyError:
            return None # Empty processing set
        states = self.next_states(best_full)
        if isinstance(states, list):
            self.storage.record_all(states, best_full[0])
            return bool(states) # did we add new states
        else:
            return states # goal

    def solve(self):
        """Solve the given problem."""

        while True:
            result = self.single_step()
            if result == None:
                return None
            elif not isinstance(result, bool):
                return self.generate_path(result)

class SymmetricAStar(AStar):
    """Like other parallel AStar implementations, but all parallel operations have to finish before the next group begin."""

    def __init__(self, state, goal, heuristic, expander, groupsize=2, Storage=BestStorage):
        AStar.__init__(self, state, goal, heuristic, expander, Storage)
        self.groupsize = groupsize

    def step_worker(self, pipe, rlock, wlock):
        while True:
            with rlock:
                msg = pipe.recv()
            if msg == None:
                return
            next = self.next_states(msg)
            with wlock:
                pipe.send((next, msg[0])) # return states and minimal parent state

    def distribute_work(self, pipe):
        """Distribute as much work as possible and return number distributed."""

        distributed = 0
        for _ in range(self.groupsize):
            try:
                state = self.storage.take()
                pipe.send(state)
                distributed += 1
            except KeyError:
                break
        return distributed

    def receive_results(self, pipe, toreceive):
        """Receive all results and return either goal or None"""

        goal = None
        for _ in range(toreceive):
            msg, parent = pipe.recv()
            if isinstance(msg, list):
                self.storage.record_all(msg, parent)
            else:
                goal = msg
        return goal

    def stop_processes(self, pipe):
        """Stop running processes."""

        for _ in range(self.groupsize):
            pipe.send(None)

    def solve(self):
        rlock = multiprocessing.Lock()
        wlock = multiprocessing.Lock()
        server_pipe, worker_pipe = multiprocessing.Pipe()
        processes = [multiprocessing.Process(target=self.step_worker, args=(worker_pipe, rlock, wlock)) for _ in range(self.groupsize)]
        for proc in processes:
            proc.start()
        while True:
            working = self.distribute_work(server_pipe)
            if working == 0:
                self.stop_processes(server_pipe)
                return None
            goal = self.receive_results(server_pipe, working)
            if goal != None:
                self.stop_processes(server_pipe)
                return self.generate_path(goal)


class ServedAStar(AStar):
    """Like AStar but the procesing set becomes a server that serves a new item to processes each time one completes."""

    def __init__(self, state, goal, heuristic, expander, groupsize=2, Storage=BestStorage):
        AStar.__init__(self, state, goal, heuristic, expander, Storage)
        self.groupsize = groupsize

    def step_worker(self, pipe, rlock, wlock):
        while True:
            with rlock:
                msg = pipe.recv()
            if msg == None:
                return
            next = self.next_states(msg)
            with wlock:
                pipe.send((next, msg[0])) # return states and minimal parent state

    def distribute_work(self, pipe, available):
        """Distribute as much work as possible and return number of processes left."""

        while available > 0:
            try:
                state = self.storage.take()
                pipe.send(state)
                available -= 1
            except KeyError:
                break
        return available

    def receive_results(self, pipe, available):
        """Receive all results and return either goal or None"""

        goal = None
        while pipe.poll():
            msg, parent = pipe.recv()
            available += 1
            if isinstance(msg, list):
                self.storage.record_all(msg, parent)
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
                    return self.generate_path(goal)
        finally:
            while any(p.is_alive() for p in processes):
                if server_pipe.poll():
                    server_pipe.recv()
            server_pipe.close()
            worker_pipe.close()


class PulledAStar(AStar):
    """Like ServedAStar but processes pull when available rather than being served."""

    def __init__(self, state, goal, heuristic, expander, groupsize=2, Storage=BestStorage):
        AStar.__init__(self, state, goal, heuristic, expander, PreparedStorageManager(Storage))
        self.groupsize = groupsize

    def step_worker(self, q, idle):
        """
        Keep performing single step until processing set is empty. Should use our remote manager set.

        """

        while True:
            if not idle.intact():
                return
            result = self.single_step()
            if isinstance(result, bool): # expanded a state
                if result: # Added a state
                    idle.reset()
            elif result == None: # empty state set
                if not idle.wait():
                    return # all waiting or goal
                # otherwise continue as before, more items were added
            else:
                q.put(result)
                idle.destroy()

    def solve(self):
        idle = sync.IdleLock(self.groupsize)
        q = multiprocessing.Queue()

        processes = [multiprocessing.Process(target=self.step_worker, args=(q, idle)) for _ in range(self.groupsize)]
        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()

        answer = None
        try:
            answer = q.get(False)
        except queue.Empty:
            pass

        self.storage.finish() # kill manager process

        return None if answer == None else self.generate_path(answer)
