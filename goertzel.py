
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

    def __init__(self, f_m : float, f_s : float):

        self.f_m = f_m 
        self.f_s = f_s
       
        self.s_n = 0
        self.s_n1 = 0
        self.s_n2 = 0
       
        self.flush()

    def get_k(self, N : int) -> int:
        return int(0.5 + (N * self.f_m / self.f_s))
    
    def get_w(self, N : int) -> float:
        return 2*math.pi*self.get_k(N)/N

    def flush(self):
        self.s_n = 0
        self.s_n1 = 0
        self.s_n2 = 0
        """
        while not self.sn.is_empty():
            self.sn.dequeue()
        while not self.fifo_y.is_empty():
            self.fifo_y.dequeue()
        for _ in range(self.N):
            self.sn.enqueue(0)
            self.fifo_y.enqueue(0)
        """
    

    # goertzel output based on a single new input value of x_in
    def goertzel(self, xn : list[float]) -> float:
        """A Gortzel-Style Filter. 
        
        All this is is a filter that does two things in parallel:

        1) Apply an IIR filter to get s[n]
        2) While s[n] is being calculated, get y[n] from s[n]

        Args:
            x_in: Signal data dump of some length 1
            surr: An integer that represents how many surrounding k-values around w0 you want. 

        Note that this runs on a SINGLE k value, determined by this class.
        """

        # Constants
        N = len(xn)
        self.flush()

        # Window the incoming signal
        xn = xn * np.hamming(len(xn))

        coeff = 2 * math.cos(self.get_w(N))
        for x in xn:
            self.s_n: float = x + coeff*self.s_n1 - self.s_n2
            self.s_n2, self.s_n1 = self.s_n1, self.s_n
        
        ret = (
            0.5 * coeff * self.s_n1 - self.s_n2,
            math.sin(self.get_w(N)) * self.s_n1,
            math.sqrt(self.s_n2**2 + self.s_n1**2 - coeff * self.s_n1 * self.s_n2)
        )

        return ret[2]


if __name__ == "__main__":

    WIND_SIZE = 64
    gN: int = 24*WIND_SIZE
    f_s = 4000
    xn = [0]*gN
    for i in range(0, gN//2):
        xn[i] = math.cos(2*math.pi*i*400/f_s) + math.cos(2*math.pi*i * 800/f_s)
    for i in range(gN//2, gN):
        xn[i] = math.cos(2*math.pi*i*400/f_s) + math.cos(2*math.pi*i * 40/f_s)


    # dft.plot_dft(xn, 32, f_s, "output")

    fig, ax = plt.subplots()


    bpg = BPGoertzel(400, f_s) # 400 Hz, not present, then present
    bpg2 = BPGoertzel(800, f_s) # 800 Hz, present then not
    bpg3 = BPGoertzel(40, f_s) # 40 Hz, present
    

    l1 = []
    l2 = []
    l3 = []

    delta = WIND_SIZE
    for i in range(0, int(gN/delta)):
        l1.append(bpg.goertzel(xn[i*delta:(i+1)*delta]))
        l2.append(bpg2.goertzel(xn[i*delta:(i+1)*delta]))
        l3.append(bpg3.goertzel(xn[i*delta:(i+1)*delta]))

    ax.plot(np.array(l1), label="400")
    ax.plot(np.array(l2), label="800")
    ax.plot(np.array(l3), label="40")
    plt.legend(loc="upper left")
    ax.grid()

    plt.show()

    pass

    


