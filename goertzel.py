
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

    def __init__(self, N: int, k: int):
        self.N = N
        self.k = k
        #self.k = round((self.f_m / self.f_s) * self.N)
        #self.sn = my_fifo(self.N)
        self.s_n = 0
        self.s_n1 = 0
        self.s_n2 = 0
        self.wo = 2*math.pi*self.k / self.N # this guy was defined on k and N!
        #self.deq = DifferenceEquation([-2*math.cos(self.wo), 1], [], 1.0)
        #self.fifo_y = my_fifo(self.N)
        self.flush()

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
        self.s_n2 = self.s_n1
        self.s_n1 = self.s_n
        self.s_n: float = x_in + 2*math.cos(self.wo)*self.s_n1 - self.s_n2
        # i_n: float = self.deq.current_yn(x_in)
        # assert s_n == i_n
        #self.sn.dequeue()
        #self.sn.enqueue(s_n)
        
        #self.fifo_y.dequeue()
        # difference equation for going from s[n] to y[n]
        y_n : complex = complex(self.s_n) - cmath.exp(-1 * j * self.wo)*complex(self.s_n1)
        #self.fifo_y.enqueue(y_n)
        
        return y_n

    def goertzel_list(self, xn : list[float]):
        y_l : list = []
        for x in xn:
            y_l.append(self.get_mag(x))
        self.flush()
        sum = 0.0
        y_p = y_l[0]
        for y_n in y_l:
            if y_n != y_l[0]:
                sum += y_n - y_p  
            y_p = y_n 
        return sum / (len(xn) - 1)


if __name__ == "__main__":

    gN: int = 200
    f_s = 4000
    xn = [0]*gN
    for i in range(0, gN//2):
        xn[i] = math.cos(2*math.pi*i*0.03) + math.cos(2*math.pi*i * 0.1)
    for i in range(gN//2, gN):
        xn[i] = math.cos(2*math.pi*i*0.03) + math.cos(2*math.pi*i * 0.01)


    dft.plot_dft(xn, 32, f_s, "output")

    fig, ax = plt.subplots()

    bpg = BPGoertzel(gN, 2) # 40 Hz, not present, then present
    bpg2 = BPGoertzel(gN, 20) # 400 Hz, present then not
    bpg3 = BPGoertzel(gN, 6) # 120 Hz, present

    l1 = []
    l2 = []
    l3 = []

    delta = 5
    for i in range(0, int(gN/delta)):
        l1.append(bpg.goertzel_list(xn[i*delta:(i+1)*delta]))
        l2.append(bpg2.goertzel_list(xn[i*delta:(i+1)*delta]))
        l3.append(bpg3.goertzel_list(xn[i*delta:(i+1)*delta]))

    ax.plot(np.array(l1))
    ax.plot(np.array(l2))
    ax.plot(np.array(l3))
    # ax.plot(np.array(xn))
    ax.grid()

    plt.show()

    pass

    


