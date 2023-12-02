import cmath
import math

import matplotlib.pyplot as plt
import numpy as np

def dft(xn : list[float], N : int) -> list[complex]:
    """Do the dft with some input signal `xn` over a range of samples `N`
    
    Evaluates the dft at all 0 <= k < N
    """
    ks = [complex(0,0)]*N
    j = complex(0,1)

    for k in range(0, N):
        sum : complex = 0
        for i in range(0,N):
            sum += xn[i]*cmath.exp(-1 * j * 2 * math.pi * k * i / N)
        ks[k] = sum / complex(N,0)
    return ks

def dft_mag(xn : list[float], N : int) -> list[float]:
    c_l = dft(xn, N)
    for i in range(0, N):
        c_l[i] = cmath.polar(c_l[i])[0]
    return c_l

def get_f0_mag(kn : list[float], fs : float) -> float:
    """Get some weighted "peak" frequency from the formula given."""
    sumtop = 0
    sumbot = 0
    T = max(kn)
    for k in range(0, len(kn)//2):
        if(kn[k] > T/2):
            mag = kn[k]
            f_k = fs * k / len(kn)
            sumtop += f_k * mag
            sumbot += mag
    if sumbot != 0:
        return sumtop / sumbot
    return 0

def plot_dft(xn : list[float], N : int, fs : float, fname : str | None):

    fig, ax = plt.subplots()
    kn = [0.0] * N
    Xk = dft_mag(xn, N)
    for i in range(0, N):
        kn[i] = i / N * fs

    ax.plot(np.array(kn[0:len(kn)//2]), np.array(Xk[0:len(Xk)//2]))

    ax.set(xlabel='Frequency (Hz)', ylabel='Magnitude', title='DFT Plot')
    ax.grid()

    fig.savefig('image_file.png')

    
    
    with open(f'{fname}.txt', 'w') as f:
        f.write(f"Data for {fname}: ...\n")
        # freq of the peak
        f.write(f"fp: {kn[Xk.index(max(Xk))]}\n")
        # freq of the peak using weighted average
        freqAvg = get_f0_mag(Xk, fs)
        f.write(f"f0: {freqAvg}\n")
        # measured air gap in inches
        airGap = 343*39.3701*0.5/freqAvg	
        f.write(f"ag: {airGap} (in)\n")
        f.close()
    
    if fname == None:
        plt.show()
    else:
        plt.savefig(f"{fname}.png")


    

