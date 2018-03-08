import readligo as rl
from pathlib import Path

def read_strainset(datadir="/media/kawahara/finbacko1",rel=1,ver="O",placelist=["L","H"],dataid=1126256640):
    strain=[]
    time=[]
    chan_dict=[]
    place=[]
    for place_ in placelist:
        filename=getfilename(datadir,rel,"O",place_,dataid)
        print(filename)
        try:
            strain_, time_, chan_dict_ = rl.loaddata(filename, place_+str(rel))
            strain.append(strain_)
            time.append(time_)
            chan_dict.append(chan_dict_)
            place.append(place_)
        except:
            print("Could not read "+filename)
            
    return place, strain, time, chan_dict

def getfilename(datadir,rel,ver,place,dataid,resl="4096",tag="_LOSC_4_V1-"):
    sr=str(rel)
    eachf=place+"-"+place+sr+tag+str(dataid)+"-"+resl+".hdf5"
    filename=Path(datadir).joinpath(Path("O"+place+sr))
    filename=filename.joinpath(Path(eachf))
    return filename
    
#    filenameH=Path(datadir).joinpath(Path("OH"+str(rel)))
#    filenameH=filenameH.joinpath(Path("H-H1_LOSC_4_V1-1126256640-4096.hdf5"))
#    strainH, timeH, chan_dict_H1 = rl.loaddata(filenameH, 'H1')
#    strainL, timeL, chan_dict_L1 = rl.loaddata(filenameL, 'L1')

if __name__ == "__main__":
    place, strain, time, chan_dict=read_strainset()
    


