"""
Similar to future but doesn't keep shouting about obscure errors.

"""

from multiprocessing import Queue, Process
import signal

class ProcessExecutor:
    def __init__(self, func, *vargs, hideerror=False, **kwargs):
        self._q = Queue()
        self._proc = Process(target=self._worker, args=[func, self._q, hideerror, vargs, kwargs])

    @staticmethod
    def _worker(func, q, hideerror, vargs, kwargs):
        def killer(*vargs):
            raise KillProcess
        signal.signal(signal.SIGTERM, killer)
        try:
            q.put(func(*vargs, **kwargs))
        except KillProcess:
            pass # Been killed, do silently
            # Daemon processes will be killed loudly by this!
        except:
            if not hideerror:
                raise
    
    def start(self):
        self._proc.start()
        
    def cancel(self):
        self._proc.terminate() # Raises KillProcess
        self._proc.join()
        
    def working(self):
        return self._proc.is_alive()
    
    def result(self):
        if self.working():
            raise IncompleteError
        if not hasattr(self, "_result"):
            if self._q.empty():
                raise IncompleteError
            else:
                self._result = self._q.get(False)
        return self._result
    
class IncompleteError(Exception):
    """Thrown when a result is requested and the operation is not yet complete."""
    
class KillProcess(Exception):
    """Thrown when the process should terminate rather than just wiping it out."""
