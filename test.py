import networkx as nx

from clustice.coder import decode, encode
from clustice.geometry import make_layout
from clustice.gromacs import render
from clustice.topology import ice_graph
from clustice.water import tip4p

g = nx.dodecahedral_graph() # dodecahedral 20mer
# g = nx.cubical_graph()

# O-O distance
L = 0.27

layout = make_layout(g, edgelen=L)

# set orientations of the hydrogen bonds.
# if pos is given, the net dipole moment is minimized.
dg = ice_graph(g, pos=layout)
# dg = ice_graph(g)
id = encode(dg)
print(id)
# dg2 = decode(id)
# print(encode(dg2))
# assert nx.is_isomorphic(dg, dg2)


# put water molecules
gro = render(dg, layout, watermodel=tip4p)
with open(f'{id}.gro','w') as f:
    f.write(gro)
