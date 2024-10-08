from logging import DEBUG, INFO, basicConfig, getLogger

import networkx as nx

# import py3Dmol
from genice2.genice import GenIce
from genice2.plugin import Format, Lattice
from clustice.gromacs import render
from clustice.water import tip4p
import genice_core

logger = getLogger()
basicConfig(level=DEBUG)

lattice = Lattice("1h")
formatter = Format("raw", stage=(1, 2))
raw = GenIce(lattice, signature="Ice Ih", rep=(3, 3, 3)).generate_ice(formatter)

# graph is the topology of the hydrogen-bond network
g = nx.Graph(raw["graph"])
# reppositions contains the positions of CoM of water in fractional coordinate
layout = raw["reppositions"]
# repcell is the cell matrix (transposed)
cell = raw["repcell"]

# set orientations of the hydrogen bonds.
dg = genice_core.ice_graph(
    g, vertexPositions=layout, isPeriodicBoundary=True, dipoleOptimizationCycles=200
)

# put water molecules
gro = render(
    dg,
    layout @ cell,
    water_model=tip4p,
    cell_matrix=cell,
)
with open(f"save.gro", "w") as f:
    f.write(gro)

# # show
# view = py3Dmol.view()
# view.addModel(gro, "gro")
# view.setStyle({"stick": {}})
# view.addUnitCell()
# view.zoomTo()
# view.show()
