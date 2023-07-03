import numpy as np
import itertools as it
from logging import getLogger

def minimize_net_dipole(paths, pos):
    logger = getLogger()
    moments = []
    for path in paths:
        # dipole moment of a path; NOTE: No PBC.
        netdip = pos[path[-1]] - pos[path[0]] 
        moments.append(netdip)
    moments = np.array(moments)
    net = np.sum(moments, axis=0)
    best = None
    for coeff in it.product([1,-1], repeat=len(moments)):
        newnet = np.array(coeff) @ moments
        if newnet@newnet < net@net:
            net = newnet
            best = coeff
            logger.debug(net)
    for i in range(len(paths)):
        if coeff[i] < 0:
            paths[i] = paths[i][::-1]
    return paths
        
