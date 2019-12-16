'''
计算V的方差，除以N-1
'''
import numpy as np
def cost(V):
    D = np.var(V,ddof = 1)
    return D