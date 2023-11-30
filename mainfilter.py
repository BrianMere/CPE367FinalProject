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

    def __init__(self, freqs : list[float], f_s : float):
        self.freqs = freqs # Frequencies to look for.
        self.f_s = f_s # Sampling frequency

        self.f_filter : dict[float, BPGoertzel] = {} # Dict of internal filters for each f in freq
        for f in freqs:
            self.f_filter[f] = BPGoertzel(f, self.f_s)

    def get_best_signal_guess(self, xn : list[float]) -> float:
        """Given the state of this GoertzelComb, determine the best guess of the 
        
        The best part about this is that all frequencies are run 
        in parallel, so we have a speedup of the number of 
        frequencies we want to detect.

        Args:
            xn: List of sample inputs to run our filters over...
        """

        def best_guess(lf : list[float], Xk_mag : list[float]) -> float:
            """Take in a list of corresponding frequencies and 
            magnitudes of DFT to determine the best guess of the 
            scanned frequency.

            f_0 = (\sum_k f_k |X[k]|) / (\sum_k |X[k]|)
            """
            
            return lf[min(range(len(Xk_mag)), key=Xk_mag.__getitem__)]
        
            # top = 0.0
            # bot = 0.0
            # if len(lf) != len(Xk_mag):
            #     raise ValueError("Expected lists of the same length")
            # for k in range(0, len(lf)):
            #     top += lf[k] * Xk_mag[k]
            #     bot += Xk_mag[k]
            # return top / bot

        mpu = Multiprocessor()
        for f in self.freqs:
            mpu.run(self.f_filter[f].get_mag, xn)
        ret : list[float] = mpu.wait_all()
        f0 = best_guess(self.freqs, ret)
        # Return the closest key to f0 available
        return min(self.freqs, key=lambda x : abs(x - f0))
    
    
    
if __name__ == "__main__":
    f_s = 4000 
    f = [1209, 1336, 1477, 1633]
    xn = [1,2,3,4,5]

    gc = GoertzelCombs(f, f_s)
    print(str(gc.get_best_signal_guess()))

        



    