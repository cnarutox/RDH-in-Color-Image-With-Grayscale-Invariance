import numpy as np
from numpy import mat
import matlab
import matlab.engine
import scipy.io as sio

eng = matlab.engine.start_matlab()
def compresscoder(signal):
    L = max(signal.shape)
    signal = signal.astype(np.float)
    minS = signal[:].min()
    maxS = signal[:].max()
    w,t = np.histogram(signal,range=(minS,maxS+1))
    lo = np.size(w)
    # HistS = t[:-1] + np.diff(t)/2
    HistS = w[:lo-1]
    width = maxS-minS+1
    Ps = HistS.astype(np.float)/sum(HistS)
    Freq = np.ones([int(L),int(width)])
    for i in range(1,int(width)+1):
        Freq[:,i-1] = Ps[i-1]*Freq[:,i-1]
    signal=signal-min(signal)+1
    signal= signal.reshape(L,1)
    # sio.savemat('D:\\signal.mat', {'array': signal})
    # sio.savemat('D:\\Freq.mat', {'array': Freq})
    # signal_mat = sio.loadmat('D:\\signal.mat')
    # Freq_mat = sio.loadmat('D:\\Freq.mat')
    # Comp_bitstream=len(eng.arith_encode(matlab.double(signal),matlab.double(Freq_mat)))
    # return Comp_bitstream



