import numpy as np
import os
import glob
import argparse

def get_dataid(dirn,tcenter):
       
    arr=[os.path.basename(r) for r in glob.glob(dirn+'/*.hdf5')]
    tin=[]
    for i in arr:
        j=(i.replace("L-L1_LOSC_4_V1-","").replace("-4096.hdf5",""))
        tin.append(np.int(j))
    tin=np.array(tin)
    tin=np.sort(tin)
    ind=(np.searchsorted(tin,tcenter))
    dataid=str(tin[ind-1])

    return dataid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='QL for LIGO data')
    parser.add_argument('-t', nargs=1, default=[1126259462.43], help='time center', type=float)
    args = parser.parse_args()    
    tcenter=args.t[0]
    dirn="/finback/OL1/"
    dataid=get_dataid(dirn,tcenter)
    print(dataid)

#for filename in sys.argv[1:]:
#    strain, time, chan_dict = rl.loaddata(filename)
#    print(filename.replace("/finback/OL1/L-L1_LOSC_4_V1-","").replace("-4096.hdf5",""),time[0],time[-1])

#placei, strainall, timeall, chan_dict=rs.read_strainset(datadir=datadir,dataid=dataid)
