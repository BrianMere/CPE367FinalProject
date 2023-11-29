from my_fifo import my_fifo
import math

class BandpassFilter:
    """A class to handle the difference equation 
    determined from a bandpass filter. This filter 
    is made using the Z-transform interpretation of a 
    bandpass filter, and then turning that into the 
    Difference Equation...
    
    Access all the methods of DifferenceEquation via:

    self.de.<method_name>...
    """

    def __init__(self, pole_radius : float, gain : float, f_c : float, f_s : float):
        self.de = DifferenceEquation([-2*pole_radius*math.cos(f_c/f_s), pole_radius**2], [], gain)

        
class DifferenceEquation:
    """Class definition of a difference equation, given some list 
    of constants for the coefficients for y[n] and x[n]
    of various shifted values
    
    We note that the following are equivalent:

    y[n] + a_1y[n-1] + a_2y[n-2] - ... = b_0x[n] + b_1x[n-1]

    ↕

    H(z) = b_0 + b_1z^{-1} + ... / 1 + a_1z^{-1} + a_2z^{-2} + ...

    We note that this object has memory, taking in one xn at a time, 
    and using the difference equation to get the next value in the line. 

    Args:
        A: list of A coefficients (a_1, a_2, ...) in that order
        B: list of B coefficients (b_1, b_2, ...). NOTE: b_0 is reserved for the next parameter
        B0: The b_0 coefficient.
        r: The resolution we want our filter to have, giving the number of bits. By default uses r = 10. 
    """

    def __init__(self, A : list[float], B: list[float], B0 : float, r : int = 10):
        self.A = A
        self.B = B
        self.B0 = B0
        self.r = r

        self.fifo_size = max(len(A), len(B))
        self.fifo_y : my_fifo = my_fifo(self.fifo_size)
        self.fifo_x : my_fifo = my_fifo(self.fifo_size)

        self.flush_system()

    def flush_system(self):
        """Flush the current queue back to steady state of 0's"""
        while not self.fifo_x.is_empty():
            self.fifo_x.dequeue()
        while not self.fifo_y.is_empty():
            self.fifo_y.dequeue()
        for i in range(0, self.fifo_size):
            self.fifo_y.enqueue(0)
            self.fifo_x.enqueue(0)

    def _get_C(self) -> int:
        """Get the C between our contained constants """
        return int(2**self.r)


    def current_yn(self, x_next : float) -> float:
        """Calculate next yn value. 

        x_next = x[n] (current)
        self.fifo_x.get(0) === x[n-1]
        self.fifo_x.get(1) === x[n-2]
        ... 
        and similar for y. 

        Returns y[n]. STORES the new y[n] and x[n] values in our internal fifos.
        
        Args:
            Current x[n] value

        Returns:
            Current y[n] value. 
        """
        C = self._get_C()
        y_next = 0.0

        # First do for B0
        b0 = round(C * self.B0)
        y_next += (b0 * x_next) / C

        # Then repeat for A, B
        for i, b in enumerate(self.B):
            # Do INT arithmetic for faster calcs. 
            bk = round(C * b)
            y_next += (bk * self.fifo_x.get(i)) / C

        for i, a in enumerate(self.A):
            ak = round(C * a)
            # Note for A we need to subtract these values. 
            y_next -= (ak * self.fifo_y.get(i)) / C

        # Update the values in our internal fifos.
        self.fifo_x.dequeue()
        self.fifo_x.enqueue(x_next)
        self.fifo_y.dequeue()
        self.fifo_y.enqueue(y_next)
        return y_next
    
    def yn(self, xn : list[float] | list[int], more_values : int = 0) -> list:
        """Calculate the list of values using our difference 
        equation coefficients. 
        
        Args:
            xn: input signal samples.
            more_values: The size of the number of samples of extra yn we want, which is added to the length of x
        
        Returns:
            The list of yn's, relative to the input signal provided. 
        """

        ret = []

        for x in xn:
            ret.append(self.current_yn(x))
        for _ in range(0, more_values):
            ret.append(self.current_yn(0.0))
        return ret
    
    def hn(self, number_values : int = None) -> list[float]:
        """Get h[n]. By default will use len(B) for the number of values. """
        if number_values is None:
            number_values = len(self.B)
        return self.yn([1], number_values)
            

if __name__ == "__main__":

    A = [-1, -1]
    B = [1]
     
    de = DifferenceEquation(A, B, 0.0)
    print(str(de.hn(100)))
    
        
        
        