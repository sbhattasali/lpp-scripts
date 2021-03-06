#! /usr/bin/env python
# Time-stamp: <2017-06-16 15:19:42 cp983411>

import getopt, sys
import numpy as np
import pandas as pd
from nistats.hemodynamic_models import compute_regressor

import matplotlib.pyplot as plt

def usage():
    print("Generate predicted hrf + derivative responses from an events file")
    print("""
    -i input_file : a csv files with columns 'onset' and 'amplitude'
    -t xx         : xx is the Time of Repetion (or scanning sampling rate), in sec
    -n nn         : nn is the total number of scans
    -o output_file  : will contain 2 columns: hrf and its derivative

Example:
    events2hrf -t 2.0 -n 600 -i f0_short.csv -o f0_reg.csv
""")

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:n:hi:o:", ["tr", "nscans", "help", "input=", "output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

outputf = "output.csv"
inputf = "input.csv"

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit(2)
    elif o in ("-t", "--tr"):
        tr = float(a)
    elif o in ("-n", "--nscans"):
        nscans = int(a)
    elif o in ("-o", "--output"):
        outputf = a
    elif o in ("-i", "--input"):
        inputf = a


if inputf is None:
    usage()
    sys.exit(2)

endpoint = nscans * tr

frame_times = np.arange(0.0, endpoint, tr)

    
a = pd.read_csv(inputf)
n_events = len(a)
onsets = a.onset
amplitudes = a.amplitude
durations = np.zeros(n_events)


x = compute_regressor(exp_condition = np.vstack((onsets, durations, amplitudes)),
                     hrf_model="spm",
                     frame_times = frame_times,
                     oversampling=10)

x2 = pd.DataFrame(x[0], columns=['hrf'])
#plt.plot(x2.hrf)
#plt.show()
x2.to_csv(outputf, index=False, header=False)

