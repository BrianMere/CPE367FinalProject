
from bandpass import DifferenceEquation, BandpassFilter
from dft import plot_dft

import math
import cmath

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
        self.bp_filt = BandpassFilter(0.9, 2.1, f_m, f_s)

    def get_mag(self, xn : list) -> float:
        """Get the magnitude of our class's f_m value. 
        
        Args:
            xn: Input data to calculate all at once. 
        """
        k = round(self.f_m / self.f_s) * len(xn)
        input_sig = self.bp_filt.de.yn(xn)
        return abs(self.goertzel(input_sig, k))

    def goertzel(self, xn : list[int], k : int) -> complex:
        """A Gortzel-Style Filter. 
        
        All this is is a filter that does two things in parallel:

        1) Apply an IIR filter to get s[n]
        2) While s[n] is being calculated, get y[n] from s[n]

        Args:
            xn: Signal data dump of some length N
            k: Get the k-th DFT constant from doing xn. Thus, the analyzed frequency is wo = 2pi*k/N
        """
        N = len(xn)
        j = complex(0.0, 1.0)
        wo = 2*math.pi*k / N
        sn_eq = DifferenceEquation([-2*math.cos(wo), 1], [], 1.0)
        sn : list[int] = sn_eq.yn(xn)
        return cmath.exp(j * 2 * cmath.pi * k / N)*sn[N-1] - sn[N-2]



if __name__ == "__main__":


    f_s = 4000
    xn = [1,2,3,4,5]
    xn = xn + [0] * (int(f_s/2) - len(xn))

    plot_dft(xn, len(xn), f_s, "output")

    for f_m in range(0, f_s, 1000):
        bpg = BPGoertzel(f_m, f_s)
        print(f"f_m : {f_m}, mag: {bpg.get_mag(xn)}")
    

    


