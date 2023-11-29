import numpy as np
import cmath as cm
import math

def goertzel(xn : list[int], f_s, *freqs: list[tuple]) -> list[tuple[complex]]:
    """Does the Goertzel Algorithm on the list 
    of xn samples, given some sample rate f_s

    It returns a list of X[k] from the list of frequencies
    Each X[k] is a complex number. 

    This algorithm runs in O(n) time where n is the size of xn. 
    Furthermore, if *freqs is size m, then it runs O(nm). 
    Hence, this algorithm is polynomic. 
    """

    window_size = len(xn)
    f_step = f_s / float(window_size)
    f_step_normalized = 1.0 / window_size

    # Convert our list of frequency tuples (ranges) into ranges of k's
    bins = set()
    for f_range in freqs:
        f_start, f_end = f_range
        k_start = int(math.floor(f_start / f_step))
        k_end = int(math.ceil(f_end / f_step))

        if k_end > window_size - 1: raise ValueError(f"Frequency out of range {k_end}")
        bins = bins.union(range(k_start, k_end))

    # For each bin (k-range) calculate the DFT term
    freqs = []
    results = []
    for k in bins:

        # Bin frequency and coefficients for the computation
        f = k * f_step_normalized # frequency 
        w_real = 2.0 * math.cos(2.0 * math.pi * f) # real component of complex result 
        w_imag = math.sin(2.0 * math.pi * f)

        # Do the calculation to get to s[N] (this is the O(n) part)
        d1, d2 = 0.0, 0.0
        for n in range(0, window_size):
            y = xn[n] + w_real * d1 - d2
            
            d2, d1 = d1, y


class Goertzel:

    def __init__(self, freq: float, sampRate: float):
        self.freq = freq
        self.digradfreq = freq*2*np.pi/sampRate
        self.sn = [0]*3

    def transfer(self, xn: int) -> complex:
        # s[n] = x[n]*2cos(omega)*s[n-1] - s[n-2]
        # y[n] = s[n] - exp(-jw)*s[n-1]
        self.sn[1] = self.sn[0]
        self.sn[2] = self.sn[1]
        self.sn[0] = xn*2*np.cos(self.digradfreq)*self.sn[1] - self.sn[2]
        yn = complex(self.sn[0], 0) - complex(np.cos(self.digradfreq)*self.sn[1], np.sin(self.digradfreq)*self.sn[1])
        return yn
    
    
