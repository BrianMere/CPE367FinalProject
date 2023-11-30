from multiprocessing import Process, Queue
import types 

class Multiprocessor:
    """A generic class to handle many processing elements at one time"""

    def __init__(self):
        self.processes : list[Process] = []
        self.q = Queue()

    @staticmethod 
    def _wrapper(func : types.FunctionType, queue : Queue, args, kwargs):
        """DO NOT CALL THIS METHOD EXTERNALLY"""
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, f : types.FunctionType, *args, **kwargs) -> None:
        """Add and start a new process f(args, kwargs)"""
        args2 = [f, self.q, args, kwargs]
        p = Process(target = self._wrapper, args = args2)
        self.processes.append(p)
        p.start()
        
    def wait_all(self) -> list:
        """Wait for all processes and return a list of returned values"""
        ret = []
        for p in self.processes:
            ret.append(self.q.get())
        for p in self.processes:
            p.join()
        return ret
