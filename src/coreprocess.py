import readligo as rl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import sys
import readset as rs

# -- Center the ASD segment on the requested time
def get_seg(rel_time,dt,strain,N_samp):
    indx = np.where(np.abs(rel_time) < dt)[0][0]
    strain_seg = strain[indx-N_samp : indx+N_samp]
    time_seg = rel_time[indx-N_samp : indx+N_samp]
    return strain_seg, time_seg

def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)

    # whitening: transform to freq domain, divide by asd, then transform back, 
    # taking care to get normalization right.
    hf = np.fft.rfft(strain)
    white_hf = hf / (np.sqrt(interp_psd(freqs) /dt/2.))
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht


