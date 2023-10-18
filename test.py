from logging import DEBUG, INFO, basicConfig, getLogger

import networkx as nx
import numpy as np

from genice_core.coder import decode, encode
from genice_core.geometry import make_layout
from clustice.graph import great_icosahedron, great_decahedron
from genice_core.gromacs import render
from genice_core.topology import ice_graph
from genice_core.water import tip4p

logger = getLogger()
basicConfig(level=INFO)

np.random.seed(12345)

# g = nx.dodecahedral_graph()  # dodecahedral 20mer
# g = nx.cubical_graph()
# g = great_icosahedron(2)
g = great_decahedron(20)

# O-O distance
L = 0.27

# estimate of the positions of the nodes
# layout = make_layout(g, edgelen=L)
# or, extract the embedded coords in g
layout = np.array([g.nodes[v]["pos"] for v in g])

# set orientations of the hydrogen bonds.
# if pos is given, the net dipole moment is minimized.
dg = ice_graph(g, pos=layout)

test_encoder = False
if test_encoder:
    id = encode(dg)
    dg2 = decode(id)
    assert nx.is_isomorphic(dg, dg2)


# put water molecules
gro = render(dg, layout, watermodel=tip4p)
with open(f"save.gro", "w") as f:
    f.write(gro)
