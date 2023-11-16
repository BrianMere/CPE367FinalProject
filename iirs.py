from my_fifo import my_fifo
import numpy as np

class CombFilter:
    """Our Comb Filter"""
    
    def __init__(self, tau : int, gain : float):
        self.tau = np.abs(tau) #: Our comb delay in samples. Assumed to be positive. Will set to |t|.
        self.gain = gain #: Our recursive gain.

        self.fifo = my_fifo(tau) # Needs to be as long as tau'
        
        for i in range(0, self.tau):
            self.fifo.enqueue(0)

    def get_y(self, x : float):
        """Given some x[n] input, get some output. Stores intermediary values 
        interally.
        """
        tdelay = self.fifo.dequeue()
        self.fifo.enqueue(x + tdelay*self.gain)
        return tdelay
        




if __name__ == "__main__":

    cf = CombFilter(1, 0.7)

    print(cf.get_y(1))
    for i in range(1, 10):
        print(cf.get_y(0))
    
