#!/usr/bin/python
import sys
import time
import base64
import random as random
import datetime
import time
import math
import matplotlib.pyplot as plt
import numpy as np

from my_fifo import my_fifo
# from cpe367_wav import cpe367_wav
from cpe367_sig_analyzer import cpe367_sig_analyzer
from mainfilter import GoertzelFilterComb, GoertzelCombs
from bandpass import BandpassFilterRange, DifferenceEquation


############################################
############################################
# define routine for detecting DTMF tones
def process_wav(fpath_sig_in):
###############################
# define list of signals to be displayed by and analyzer
# note that the signal analyzer already includes: 'symbol_val','symbol_det','error'
    more_sig_list = ['sig_1','high_freq', 'low_freq', '1336']
    # sample rate is 4kHz
    fs = 4000
    # instantiate signal analyzer and load data
    s2 = cpe367_sig_analyzer(more_sig_list,fs)
    s2.load(fpath_sig_in)
    s2.print_desc()


    ########################
    # students: setup filters
    # process input

    xin = 0

    # We'll use two sets of Goertzel Combs to detect the high and low value correspondingly
    fhigh = [1209, 1336, 1477, 1633]
    # HFDetect = GoertzelFilterComb(fhigh, fs, BandpassFilterRange(fhigh, 100, fs, 31, 1.4).de)
    flow = [697, 770, 852, 941]
    HFDetect = GoertzelCombs(fhigh, fs)
    # LFDetect = GoertzelFilterComb(flow, fs, BandpassFilterRange(flow, 100, fs, 31, 1.4).de)
    LFDetect = GoertzelCombs(flow, fs)
    # And use this lookup table for values
    tones : dict[float, dict[float, int]] = {}
    for f in fhigh:
        tones[f] = {}
    tones[1209][697] = 1
    tones[1336][697] = 2
    tones[1477][697] = 3
    tones[1633][697] = ord("A")
    tones[1209][770] = 4
    tones[1336][770] = 5
    tones[1477][770] = 6
    tones[1633][770] = ord("B")
    tones[1209][852] = 7
    tones[1336][852] = 8
    tones[1477][852] = 9 
    tones[1633][852] = ord("C")
    tones[1209][941] = ord("*")
    tones[1336][941] = 0
    tones[1477][941] = ord("#")
    tones[1633][941] = ord("D")

    WINDOW_SIZE = 32 # Size of our sample to use to pass to everything!
    p = 0.10 # Change this parameter to change O. 0.0 < p < 1.0, where as p->0 we have more resolute tone updates but slower computer times, and vice versa. 
    O = int(p * WINDOW_SIZE) # The amount of new samples to take before sending everything back through our main filter. 

    symbol_val_det = 0
    hf = fhigh[0]
    lf = flow[0]
    tf = 0

    # Define a place to put our temporary signals ...

    xnp = my_fifo(WINDOW_SIZE)
    for _ in range(0, WINDOW_SIZE):
        xnp.enqueue(0.0)
    i_o = 0
    

    for n_curr in range(s2.get_len()):
        # read next input sample from the signal analyzer
        xin = s2.get('xin',n_curr)

        ########################
        # students: evaluate each filter and implement other processing blocks
        ########################

        xnp.dequeue()
        xnp.enqueue(xin)
        i_o += 1
        
        if i_o == O:
            i_o = 0

            data = []
            for i in range(0, xnp.size()):
                data.append(xnp.get(i))
            # students: combine results from filtering stages
            # and find (best guess of) symbol that is present at this sample time
            # Update input and filters to get new values. 
            hf = HFDetect.get_best_signal_guess(data)
            lf = LFDetect.get_best_signal_guess(data)
            tf = HFDetect.probe[1] # 1336

        symbol_val_det = tones[hf][lf]
        
        s2.set('high_freq', n_curr, hf)
        s2.set('low_freq', n_curr, lf)
        s2.set('1336', n_curr, tf)

        # save intermediate signals as needed, for plotting
        # add signals, as desired!

        s2.set('sig_1',n_curr,xin)
        # save detected symbol
        s2.set('symbol_det',n_curr,symbol_val_det)
        # get correct symbol (provided within the signal analyzer)
        symbol_val = s2.get('symbol_val',n_curr)
        # compare detected signal to correct signal
        symbol_val_err = 0
        if symbol_val != symbol_val_det: 
            symbol_val_err = 1
        # save error signal
        s2.set('error',n_curr,symbol_val_err)

    # display mean of error signal
    err_mean = s2.get_mean('error')
    print('mean error = '+str( round(100 * err_mean,1) )+'%')
    # define which signals should be plotted
    plot_sig_list = more_sig_list + ['symbol_val','symbol_det','error']
    # plot results
    s2.plot(plot_sig_list)
    return True
############################################
############################################
# define main program
def main():
    # check python version!
    major_version = int(sys.version[0])
    if major_version < 3:
        print('Sorry! must be run using python3.')
        print('Current version: ')
        print(sys.version)
        return False
    # assign file name
    # fpath_sig_in = 'dtmf_signals_slow.txt'
    fpath_sig_in = 'dtmf_signals_fast.txt'
    # let's do it!
    return process_wav(fpath_sig_in)

############################################
############################################
# call main function
if __name__ == '__main__':
    main()
    quit()
