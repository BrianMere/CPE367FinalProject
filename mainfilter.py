from goertzel import BPGoertzel
from multiprocessor import Multiprocessor

class GoertzelCombs:
    """The main, overarching filter for this project...
    
    This should be a filter that takes in a list of xn's of 
    some predetermined size, and looks for frequencies specified in 
    a list. 

    Mainly, it's doing a bandpass filter for each frequency, then 
    doing a Goertzel filter, then doing some frequency analysis 
    to determine the peak frequency and the confidence that that 
    asked frequency is primarily in the main signal xn.
    """

    def __init__(self, freqs : list[float], f_s : float, resolution : float = 0.01):
        self.freqs = freqs # Frequencies to look for.
        self.f_s = f_s # Sampling frequency

        self.f_filter : dict[float, BPGoertzel] = {} # Dict of internal filters for each f in freq
        for f in freqs:
            self.f_filter[f] = BPGoertzel(f, self.f_s, resolution)
        self.probe : list[float] = [0.0] * len(freqs)

    def get_best_signal_guess(self, x_in : float) -> float:
        """Given the state of this GoertzelComb, determine the best guess of the 
        
        The best part about this is that all frequencies are run 
        in parallel, so we have a speedup of the number of 
        frequencies we want to detect.

        Args:
            x_in: New sample
        """

        def best_guess(lf : list[float], Xk_mag : list[float]) -> float:
            """Take in a list of corresponding frequencies and 
            magnitudes of DFT to determine the best guess of the 
            scanned frequency.

            f_0 = (\sum_k f_k |X[k]|) / (\sum_k |X[k]|)
            """
            
            return lf[min(range(len(Xk_mag)), key=Xk_mag.__getitem__)]

        # mpu = Multiprocessor()
        ret : list[float] = [0.0] * len(self.freqs)
        for i, f in enumerate(self.freqs):
            # mpu.run(self.f_filter[f].get_mag, x_in)
            ret[i] = self.f_filter[f].get_mag(x_in)
        # ret : list[float] = mpu.wait_all()
        self.probe = ret
        f0 = best_guess(self.freqs, ret)
        # Return the closest key to f0 available
        return min(self.freqs, key=lambda x : abs(x - f0))
    
    
    
if __name__ == "__main__":
    f_s = 4000 
    f = [1209, 1336, 1477, 1633]
    xn = [1,2,3,4,5]

    gc = GoertzelCombs(f, f_s)
    print(str(gc.get_best_signal_guess()))

        



    