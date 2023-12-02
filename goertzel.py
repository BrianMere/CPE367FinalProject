
from bandpass import DifferenceEquation
import dft
from my_fifo import my_fifo

import math
import cmath
import matplotlib.pyplot as plt
import numpy as np

class BPGoertzel:
    """A list of passed frequencies that want to be detected are passed, given 
    some sampling frequency. This class gives information 
    
    This is pretty much a bandpass filter on the frequency in question, as 
    well as doing the actual goertzel calculation from that filter's 
    information. 
    """

    def __init__(self, f_m : float, f_s : float, resolution : float = 0.01):
        self.f_m = f_m
        self.f_s = f_s
        self.N = int(1/resolution)
        self.k = round((self.f_m / self.f_s) * self.N)
        self.sn = my_fifo(self.N)
        self.wo = 2*math.pi*self.k / self.N
        self.deq = DifferenceEquation([-2*math.cos(self.wo), 1], [], 1.0)
        self.fifo_y = my_fifo(self.N)

        self.flush()

    def flush(self):
        while not self.sn.is_empty():
            self.sn.dequeue()
        while not self.fifo_y.is_empty():
            self.fifo_y.dequeue()
        for _ in range(self.N):
            self.sn.enqueue(0)
            self.fifo_y.enqueue(0)
    
    def get_mag(self, x_in : float) -> float:
        """Get the magnitude of our class's f_m value. 
        
        Args:
            x_in : Single memory input data...
        """
        return abs(self.goertzel(x_in))

    # goertzel output based on a single new input value of x_in
    def goertzel(self, x_in : float) -> complex:
        """A Gortzel-Style Filter. 
        
        All this is is a filter that does two things in parallel:

        1) Apply an IIR filter to get s[n]
        2) While s[n] is being calculated, get y[n] from s[n]

        Args:
            x_in: Signal data dump of some length 1
            k: Get the k-th DFT constant from doing xn. Thus, the analyzed frequency is wo = 2pi*k/N
        """

        # Constants 
        j = complex(0.0, 1.0)

        
        s_n: float = x_in + 2*math.cos(self.wo)*self.sn.get(self.N-1) - self.sn.get(self.N-2)
        # i_n: float = self.deq.current_yn(x_in)
        # assert s_n == i_n
        self.sn.dequeue()
        self.sn.enqueue(s_n)
        
        self.fifo_y.dequeue()
        # difference equation for going from s[n] to y[n]
        y_n : complex = complex(complex(self.sn.get(self.N - 1)) - cmath.exp(-1 * j * self.wo)*self.sn.get(self.N - 2))
        self.fifo_y.enqueue(y_n)
        
        return y_n


if __name__ == "__main__":


    f_s = 4000
    xn = [math.cos(2*math.pi*i*0.03) + math.cos(2*math.pi*i * 0.1) for i in range(0, 500)]

    dft.plot_dft(xn, 32, f_s, "output")

    fig, ax = plt.subplots()

    bpg = BPGoertzel(100, f_s, 0.2)
    bpg2 = BPGoertzel(400, f_s, 0.2)
    bpg3 = BPGoertzel(600, f_s, 0.2)

    l1 = []
    l2 = []
    l3 = []
    ln = []

    for i, x in enumerate(xn):
        l1.append(bpg.get_mag(x))
        l2.append(bpg2.get_mag(x))
        l3.append(bpg3.get_mag(x))
        ln.append(i)

    ax.plot(np.array(ln), np.array(l1))
    # ax.plot(np.array(ln), np.array(l2))
    # ax.plot(np.array(ln), np.array(l3))
    ax.plot(np.array(ln), np.array(xn))
    ax.grid()

    plt.show()

    pass

    


