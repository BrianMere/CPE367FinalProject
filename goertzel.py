
from bandpass import DifferenceEquation
import math
import cmath

def goertzel(xn : list[int], k : int) -> complex:
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
    hn = [1,2,3,4,5]

    for i in range(0, len(hn)):
        print(str(goertzel(hn, i)))

