"""
Helpful search algorithms for use by plugins.

"""

import multiprocessing
import queue
import abc

from . import sync

###############################################################
#
# Storage for A* implementations
#
###############################################################

class AbstractStorage(metaclass=abc.ABCMeta):
    """ABC for storage so we know what we have to implement!"""
    
    @abc.abstractmethod
    def record(self, state, parent): raise NotImplementedError
    @abc.abstractmethod
    def record_all(self, states, parent): raise NotImplementedError
    @abc.abstractmethod
    def take(self): raise NotImplementedError
    @abc.abstractmethod
    def parent(self, state): raise NotImplementedError

class UsefulStorage(AbstractStorage):
    """Saves implementing certain functions in storage classes."""

    def record(self, state, parent):
        self._add_state(state)
        self._add_parent(state, parent)

    def record_all(self, states, parent):
        for s in states:
            self.record(s, parent)

    @abc.abstractmethod
    def _add_parent(self, state, parent): raise NotImplementedError
    @abc.abstractmethod
    def _add_state(self, item): raise NotImplementedError

class LayeredAStarStorage(UsefulStorage):
    """Orders states using various levels of dicts."""

    def __init__(self):
        self._open = {}
        self._parents = {}

    def _add_parent(self, state, parent):
        s, cost, _2 = state
        # only record one parent for each state, can cause recursive lookup if we choose the wrong one, so always choose shortest
        try:
            if cost >= self._parents[s][1]:
                return # old value was better
        except KeyError:
            pass # not in yet
        self._parents[s] = (parent, cost)

    def _add_state(self, item):
        _, cost, expected = item # split parts
        
        if expected == None:
            return # Don't add terminal states to processing set

        if expected not in self._open: # expected cost level
            self._open[expected] = {}
        e_dict = self._open[expected]
        if cost not in e_dict: # current cost level
            e_dict[cost] = set()
        e_dict[cost].add(item)

    def take(self):
        if not self._open: # no states left
            raise KeyError
        min_exp = min(self._open) # smallest expected
        e_dict = self._open[min_exp]
        max_cost = max(e_dict) # largest current
        item = e_dict[max_cost].pop()
        if not e_dict[max_cost]: # remove current level
            del e_dict[max_cost]
        if not e_dict: # remove empty expected level
            del self._open[min_exp]
        return item

    def parent(self, state):
        return self._parents[state]

class UniqueLayeredAStarStorage(LayeredAStarStorage):
    """Like DictSortedSet using parents as a closed set."""

    def __init__(self):
        LayeredAStarStorage.__init__(self)

    def _add_state(self, item):
        if item[0] in self._parents:
            return
        super()._add_state(item)


class BasicAStarStorage(UsefulStorage):
    """Uses set for the most basic implementation of our set."""

    def __init__(self):
        self._collection = set()
        self._parents = {}

    def _add_parent(self, state, parent):
        s, cost, _2 = state
        self._parents[s] = (parent, cost)

    def _add_state(self, item):
        self._collection.add(item)

    def take(self): # raises key error if none exists
        return self._collection.pop()

    def parent(self, state):
        return self._parents[state]

def StorageManager(Storage):
    """Create a class that spawns a new process to control the class and acts as a proxy anywhere else."""

    class StorageManager(AbstractStorage):
        def __init__(self):
            #multiprocessing.current_process.name() # The one to delete with
            # create server process, add and take become clients
            self._server_pipe, self._client_pipe = multiprocessing.Pipe()
            self._lock = multiprocessing.Lock() # Every client locks, then send and wait for receive if necessary, then unlock
            self._storage = None
            self._manager = multiprocessing.Process(target=self._server)
            self._manager.daemon = True
            self._manager.start() # Runs independently and closes on finish()

        def _server(self):
            """Serves items back and forth for client."""

            storage = Storage()
            while True:
                msg = self._server_pipe.recv()
                if msg == None:
                    self._server_pipe.send(storage)
                    return
                elif len(msg) == 2:
                    storage.record_all(msg[0], msg[1])
                elif len(msg) == 1:
                    p = storage.parent(msg[0])
                    self._server_pipe.send(p)
                else: # len(msg) == 0
                    try:
                        item = storage.take()
                    except KeyError:
                        item = None
                    self._server_pipe.send(item)

        def finish(self):
            """Tells the manager to stop and make this act as a normal processing set."""

            with self._lock:
                self._client_pipe.send(None)
                self._storage = self._client_pipe.recv()
                self._manager.join()

        def record(self, state, parent):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send(([state], parent))
            else:
                self._storage.record(state, parent)

        def record_all(self, states, parent):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send((states, parent))
            else:
                self._storage.record_all(states, parent)

        def take(self):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send(())
                    msg = self._client_pipe.recv()
                    if msg == None:
                        raise KeyError
                    else:
                        return msg
            else:
                return self._storage.take()

        def parent(self, state):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send((state,))
                    return self._client_pipe.recv()
            else:
                return self._storage.parent(state)

    return StorageManager

def PreparedStorageManager(Storage):
    """Like StorageManager but prepares for the next take early."""

    class PreparedStorageManager(StorageManager(Storage)):
        def __init__(self):
            super().__init__()
            self._waiting_item = None

        def _server(self):
            """Serves items back and forth for client."""

            storage = Storage()
            while True:
                msg = self._server_pipe.recv()
                if msg == None:
                    self._server_pipe.send(storage)
                    return
                elif len(msg) == 3:
                    storage.record_all(msg[0], msg[1])
                    if msg[2]:
                        self._send_take(storage)
                elif len(msg) == 1:
                    p = storage.parent(msg[0])
                    self._server_pipe.send(p)
                else: # len(msg) == 0
                    self._send_take(storage)

        def _send_take(self, storage):
            try:
                item = storage.take()
            except KeyError:
                item = None
            self._server_pipe.send(item)

        def record(self, state, parent):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send(([state], parent, False))
            else:
                self._storage.record(state, parent)

        def record_all(self, states, parent):
            if self._storage == None:
                with self._lock:
                    self._client_pipe.send((states, parent, True))
                    new_state = self._client_pipe.recv()
# Sending back won't work, we shouldn't ever need to though
#                    if self.waiting_item != None: # if we got one already, send it back
#                        self.client_pipe.send((new_state], parent))
                    self._waiting_item = new_state
            else:
                self._storage.record_all(states, parent)

        def take(self):
            if self._storage == None:
                with self._lock:
                    if self._waiting_item != None:
                        item = self._waiting_item
                        self._waiting_item = None
                        return item
                    self._client_pipe.send(())
                    msg = self._client_pipe.recv()
                    if msg == None:
                        raise KeyError
                    else:
                        return msg
            else:
                return self._storage.take()

    return PreparedStorageManager

def ReportingStorageManager(StorageManager, q):
    """Transforms a normal storage manager to report information about the current situation."""
    
    class ReportingStorageManager(StorageManager):
        def take(self):
            state = super().take() # Exceptions propagated
            q.put((state[1], state[2])) # cost, expected
            return state
    
    return ReportingStorageManager

BestStorage=UniqueLayeredAStarStorage

###############################################################
#
# Actual A* implementations
#
###############################################################

class AStar:
    """Provides an implementation for the A* algorithm."""

    def __init__(self, state, goal, heuristic, expander, Storage=BestStorage, reporting=None):
        self._goal = goal
        self._heuristic = heuristic
        self._expander = expander
        # Collects and returns full_state
        self._storage = (Storage if reporting == None
                         else ReportingStorageManager(Storage, reporting))()
        self._storage.record((state, 0, heuristic(state)), None)

    def generate_path(self, state):
        """Generate the states leading to our goal given a minimal state."""

        states = []
        while state != None:
            states.append(state)
            state, _ = self._storage.parent(state)
        states.reverse()
        return states

    def next_states(self, parent):
        """Generate the next full states from the current full state."""

        (s, cost, _1) = parent
        if self._goal(s):
            return s # Got answer
        else:
            full_states = ((state, cost+c, self._heuristic(state)) for state, c in self._expander(s))
            return [ns if ns[2] == None else (ns[0], ns[1], ns[1]+ns[2]) for ns in full_states]

    def single_step(self):
        """Take a single state from the set if possible and expand or return the answer."""

        try:
            best_full = self._storage.take()
        except KeyError:
            return None # Empty processing set
        states = self.next_states(best_full)
        if isinstance(states, list):
            self._storage.record_all(states, best_full[0])
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

    def __init__(self, *vargs, groupsize=2, **kwargs):
        AStar.__init__(self, *vargs, **kwargs)
        self._groupsize = groupsize

    def _step_worker(self, pipe, rlock, wlock):
        while True:
            with rlock:
                msg = pipe.recv()
            if msg == None:
                return
            next = self.next_states(msg)
            with wlock:
                pipe.send((next, msg[0])) # return states and minimal parent state

    def _distribute_work(self, pipe):
        """Distribute as much work as possible and return number distributed."""

        distributed = 0
        for _ in range(self._groupsize):
            try:
                state = self._storage.take()
                pipe.send(state)
                distributed += 1
            except KeyError:
                break
        return distributed

    def _receive_results(self, pipe, toreceive):
        """Receive all results and return either goal or None"""

        goal = None
        for _ in range(toreceive):
            msg, parent = pipe.recv()
            if isinstance(msg, list):
                self._storage.record_all(msg, parent)
            else:
                goal = msg
        return goal

    def _stop_processes(self, pipe):
        """Stop running processes."""

        for _ in range(self._groupsize):
            pipe.send(None)

    def solve(self):
        rlock = multiprocessing.Lock()
        wlock = multiprocessing.Lock()
        server_pipe, worker_pipe = multiprocessing.Pipe()
        processes = [
            multiprocessing.Process(target=self._step_worker, args=(worker_pipe, rlock, wlock))
            for _ in range(self._groupsize)
        ]
        for proc in processes:
            proc.daemon = True
            proc.start()
        while True:
            working = self._distribute_work(server_pipe)
            if working == 0:
                self._stop_processes(server_pipe)
                return None
            goal = self._receive_results(server_pipe, working)
            if goal != None:
                self._stop_processes(server_pipe)
                return self.generate_path(goal)


class ServedAStar(AStar):
    """Like AStar but the procesing set becomes a server that serves a new item to processes each time one completes."""

    def __init__(self, *vargs, groupsize=2, **kwargs):
        AStar.__init__(self, *vargs, **kwargs)
        self._groupsize = groupsize

    def _step_worker(self, pipe, rlock, wlock):
        while True:
            with rlock:
                msg = pipe.recv()
            if msg == None:
                return
            next = self.next_states(msg)
            with wlock:
                pipe.send((next, msg[0])) # return states and minimal parent state

    def _distribute_work(self, pipe, available):
        """Distribute as much work as possible and return number of processes left."""

        while available > 0:
            try:
                state = self._storage.take()
                pipe.send(state)
                available -= 1
            except KeyError:
                break
        return available

    def _receive_results(self, pipe, available):
        """Receive all results and return either goal or None"""

        goal = None
        while pipe.poll():
            msg, parent = pipe.recv()
            available += 1
            if isinstance(msg, list):
                self._storage.record_all(msg, parent)
            else:
                goal = msg
        return (available, goal)

    def _stop_processes(self, pipe, available):
        """Stop running processes."""

        for _ in range(self._groupsize-available):
            pipe.recv()

        for _ in range(self._groupsize):
            pipe.send(None)

    def solve(self):
        rlock = multiprocessing.Lock()
        wlock = multiprocessing.Lock()
        server_pipe, worker_pipe = multiprocessing.Pipe()
        waiting = self._groupsize
        processes = [
            multiprocessing.Process(target=self._step_worker, args=(worker_pipe, rlock, wlock))
            for _ in range(self._groupsize)
        ]
        for proc in processes:
            proc.daemon = True
            proc.start()
        while True:
            waiting = self._distribute_work(server_pipe, waiting)
            if waiting == self._groupsize:
                self._stop_processes(server_pipe, waiting)
                return None
            waiting, goal = self._receive_results(server_pipe, waiting)
            if goal != None:
                self._stop_processes(server_pipe, waiting)
                return self.generate_path(goal)


class PulledAStar(AStar):
    """Like ServedAStar but processes pull when available rather than being served."""

    def __init__(self, *vargs, groupsize=2, **kwargs):
        kwargs["Storage"] = kwargs.get("Storage", BestStorage)
        kwargs["Storage"] = PreparedStorageManager(kwargs["Storage"])
        AStar.__init__(self, *vargs, **kwargs)
        self._groupsize = groupsize

    def _step_worker(self, q, idle):
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
        idle = sync.IdleLock(self._groupsize)
        q = multiprocessing.Queue()

        processes = [
            multiprocessing.Process(target=self._step_worker, args=(q, idle))
            for _ in range(self._groupsize)
        ]
        for proc in processes:
            proc.daemon = True
            proc.start()

        for proc in processes:
            proc.join()

        answer = None
        try:
            answer = q.get(False)
        except queue.Empty:
            pass

        self._storage.finish() # kill manager process

        return None if answer == None else self.generate_path(answer)

###############################################################
#
# Transition extensions
#
###############################################################

class TransitionAStar:
    """Use the AStar class Solver to solve a problem, recording transitions."""
    
    def __init__(self, Solver, state, goal, heuristic, expander, **kwargs):
        """Solver is AStar or similar, expander is as before but centre item is transition."""
        
        new_state = (state, None)
        new_goal = (lambda state: goal(state[0]))
        new_heuristic = (lambda state: heuristic(state[0]))
        new_expander = (lambda state: [(s[:2], s[2]) for s in expander(state[0])])
        self._solve = Solver(new_state, new_goal, new_heuristic, new_expander, **kwargs)
    
    def solve(self):
        states = self._solve.solve()
        if states == None:
            return None
        return [s[1] for s in states if s[1] != None]
