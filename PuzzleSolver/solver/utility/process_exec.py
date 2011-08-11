"""
Similar to future but doesn't keep shouting about obscure errors.

"""

from multiprocessing import Queue, Process

class ProcessExecutor:
    def __init__(self, func, *vargs, **kwargs):
        self._q = Queue()
        def worker(func, q, vargs, kwargs):
            q.put(func(*vargs, **kwargs))
        self._proc = Process(target=worker, args=[func, self._q, vargs, kwargs])
        
    def start(self):
        self._proc.start()
        
    def cancel(self):
        self._proc.terminate() # TODO do this cleanly!
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