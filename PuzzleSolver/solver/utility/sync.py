"""
Contains any useful synchronisation classes.

"""

import multiprocessing

class IdleLock:
    """One-use lock that releases when enough processes are idle."""

    def __init__(self, limit):
        self._limit = limit
        self._waiting = multiprocessing.Value('i', 0)
        self._broken = multiprocessing.Value('i', 0) # 0 good, 1 broken
        self._release = multiprocessing.Event()
        self._lock = multiprocessing.RLock()

    def intact(self):
        """Is this lock intact (True), broken (None) or overflowed (False)?"""

        with self._lock:
            if self._broken.value == 1:
                return None
            else:
                return self._waiting.value < self._limit

    def reset(self):
        """Release waiting processes and reset the lock."""

        with self._lock:
            # only works if we haven't already broken or overflowed
            if self.intact():
                self._waiting.value = 0
                self._release.set()
                return True
            else:
                return False

    def destroy(self):
        """Break the lock so that any waits return immediately."""

        with self._lock:
            if self.intact():
                self._broken.value = 1
                self._release.set()
                return True
            else:
                return False

    def wait(self):
        """Wait on this lock."""

        with self._lock:
            status = self.intact()
            if not status:
                return status

            self._waiting.value += 1
            if self._waiting.value == self._limit: # exactly limit so release all threads
                self._release.set()
                return False # do not reset number, so next wait returns as hit limit
            if self._waiting.value > self._limit: # more than so immediately release
                return False

            # less than so wait
            self._release.clear()

        self._release.wait()

        return self.intact()
