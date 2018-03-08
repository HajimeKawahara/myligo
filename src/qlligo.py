import readligo as rl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import sys
import readset as rs
import coreprocess as cp
import searchfile as sf
import argparse

def qldata(datadir,
           dataid=1126256640,
           t0 = 1126259462.43,
           deltat = 15,  # Number of seconds on each side of data
           high_freq = 600., #band pass Hz
           low_freq  = 30.,  #band pass Hz
           fmin = 10.,
           fmax = 2000.,
           fig=False):
    place, strainall, timeall, chan_dict=rs.read_strainset(datadir=datadir,dataid=dataid)
    nplace=len(place)
    print(place)
    if (np.sum((timeall[0]-timeall[1])**2)) == 0.0:
        time=timeall[0]
    else:
        print("Under development")
        sys.exit()
        
    dt = time[1] - time[0]
    fs = int(np.round(1/dt))
    print ("Found {0} seconds of data".format(strainall[0].size*dt))
#    t0=time[0]
        
    # the time sample interval (uniformly sampled!)
    rel_time = time - t0
    
    #-- How much data to use for the ASD?
    N_samp = deltat*fs
    strain_segall=[]
    time_segall=[]
    # number of sample for the fast fourier transform:
    NFFT = 1*fs

    for iplace in range(0,nplace):
        strain_seg,time_seg = cp.get_seg(rel_time,dt,strainall[iplace],N_samp)
        Pxx, freqs = mlab.psd(strain_seg, Fs = fs, NFFT=NFFT, noverlap=NFFT/2, window=np.blackman(NFFT))
        # We will use interpolations of the ASDs computed above for whitening:
        psd = interp1d(freqs, Pxx)
        # now whiten the data
        strain_whiten_seg = cp.whiten(strain_seg,psd,dt)
        bb, ab = butter(4, [low_freq*2./fs, high_freq*2./fs], btype='band')    
        strain_whitenbp = filtfilt(bb, ab, strain_whiten_seg)
        strain_segall.append(strain_whitenbp)
        time_segall.append(time_seg)        
    
    fig2 = plt.figure(figsize=(20,2))
    off=0.0
    for iplace in range(0,nplace):
        plt.plot(time_segall[iplace],strain_segall[iplace]+off,label=place[iplace])
        off=off+5.0
    plt.ylim([-5,10])
    plt.xlabel('time (s) since '+str(t0))
    plt.ylabel('whitented strain')
    plt.legend(loc='lower left')
    plt.title('WHITENED strain')
    plt.savefig("ql.png")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='QL for LIGO data')
    parser.add_argument('-d', nargs=1, default=["/finback"], help='data directory', type=str)
    parser.add_argument('-t', nargs=1, default=[1126259462.43], help='GPS time center', type=float)
    parser.add_argument('-c', nargs=1, default=[600.0,30.0], help='frequency filter ', type=float)
    parser.add_argument('-l', nargs=1, default=[15], help='time width', type=int)

    args = parser.parse_args()
    tcenter=args.t[0]
    dirn=args.d[0]
    high_freq=args.c[0]
    low_freq=args.c[1]
    deltat=args.l[0]

    
    dataid=sf.get_dataid(dirn+"/OL1/",tcenter)
    qldata(datadir=dirn,
           dataid=dataid,
           t0 = tcenter,
           deltat = deltat,  # Number of seconds on each side of data
           high_freq = high_freq, #band pass Hz
           low_freq  = low_freq,  #band pass Hz
           fmin = 10.,
           fmax = 2000.,
           fig=False)
