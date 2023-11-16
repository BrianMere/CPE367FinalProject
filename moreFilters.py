from iirs import CombFilter

class BigComb:
    """Comb filter after bigplus"""
    def __init__(self, tau : int, gain : float):
        self.comb = CombFilter(tau, gain)
        self.tau = tau
        self.gain = gain
    
    def get_y(self, x : float):
        return self.comb.get_y(x)*(1-self.gain**2)-(self.gain*x)


if __name__ == "__main__":

    cf = BigComb(1, 0.7)

    print(cf.get_y(1))
    for i in range(1, 10):
        print(cf.get_y(0))