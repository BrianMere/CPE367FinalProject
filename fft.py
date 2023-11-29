import numpy as np 
from math import ceil, log2

def FFT(x: list[int]):
    """Do an FFT on x[n] to get X[k].  

    Works in O(nlog(n))
    """

    def FFT_r(x : list[int], l_idx : int, r_idx : int):
        """Recursive part of FFT"""
        N = r_idx - l_idx + 1
        if N == 1:
            return x[l_idx]
        else:
            m_idx = N // 2
            X_e = FFT_r(x, 0, m_idx) # Include middle index in left side for even case. 
            X_o = FFT_r(x, m_idx + 1, r_idx)
            # Get W_^k_N values in factor...
            factor = np.exp(-2j*np.pi*np.arange(N)/N)

            X : list = np.concatenate([X_e + factor[0:m_idx]*X_o, X_e+factor[m_idx+1:]*X_o]).tolist()
            return X


    return FFT_r(x, 0, len(x) - 1)
    
    
