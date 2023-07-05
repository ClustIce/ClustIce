import itertools as it
from logging import getLogger

import numpy as np


def minimize_net_dipole(paths, pos, maxiter=1000):
    """Minimize the net polarization by flipping paths.

    NOTE: PBC is not considered.

    Args:
        paths (_type_): List of directed paths
        pos (_type_): Positions of the nodes
        maxiter (int, optional): Number of random orientations for the paths. Defaults to 1000.

    Returns:
        list of paths: Optimized paths.
    """
    logger = getLogger()

    # polarized chains and cycles. Small cycle of dipoles are eliminated.
    polarized = []

    dipoles = []
    for i, path in enumerate(paths):
        # dipole moment of a path; NOTE: No PBC.
        if path[0] != path[-1]:
            # If no PBC, a chain pol is simply an end-to-end pol.
            chain_pol = pos[path[-1]] - pos[path[0]]
            dipoles.append(chain_pol)
            polarized.append(i)
    dipoles = np.array(dipoles)

    # brute-force search; too slow for large clusters
    # net = np.sum(dipoles, axis=0)
    # parity_optimal = None
    # for parity in it.product([1,-1], repeat=len(dipoles)):
    #     net_pol = np.array(parity) @ dipoles
    #     if net_pol@net_pol < net@net:
    #         net = net_pol
    #         parity_optimal = parity
    #         logger.debug(net)

    pol_optimal = np.sum(dipoles, axis=0)
    parity_optimal = None
    for loop in range(maxiter):
        parity = np.random.randint(2, size=len(dipoles)) * 2 - 1
        net_pol = parity @ dipoles
        if net_pol @ net_pol < pol_optimal @ pol_optimal:
            pol_optimal = net_pol
            parity_optimal = parity
            logger.info(f"{loop} {pol_optimal} dipole")
            if pol_optimal @ pol_optimal < 1e-10:
                break

    for i, dir in zip(polarized, parity_optimal):
        if dir < 0:
            paths[i] = paths[i][::-1]
    return paths
