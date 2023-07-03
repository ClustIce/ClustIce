import random

import networkx as nx


def obey_ice_rules(g):
    """
    Test if the directed graph g obeys the ice rules.
    """
    for v in g:
        id = g.in_degree(v)
        od = g.out_degree(v)
        if not (id in (1,2) and od in (1,2)):
            return False
    return True


def chain(g, seq):
    while True:
        last, head = seq[-2:]
        for next in g.neighbors(head):
            if next != last:
                break
        else:
            # no next node
            return seq
        seq.append(next)
        if next == seq[0]:
            # is cyclic
            return seq


def find_path(g):
    """
    Find the longest path in g. g must be a linear or a simple cyclic graph.
    """
    nodes = list(g.nodes())
    head = nodes[0]
    nei = [v for v in g.neighbors(head)]
    if len(nei) == 0:
        # lone node
        return []
    elif len(nei) == 1:
        # an end node, fortunately.
        return chain(g, [head, nei[0]])
    c0 = chain(g, [head, nei[0]])

    if c0[-1] != head:
        # linear chain graph
        # join the another side
        c1 = chain(g, [head, nei[1]])
        return list(reversed(c0)) + c1[1:]

    # cyclic graph
    # find the smallest label
    arg = 0
    for i, memb in enumerate(c0):
        if memb < c0[arg]:
            arg = i
    arg = 0
    cyc = c0[:-1]
    cyc = cyc[arg:] + cyc[:arg]
    cyc.append(cyc[0])
    return cyc


def divide(g):
    """
    Divide the graph into components

    A new algorithm suggested by Prof. Sakuma, Yamagata University.
    """

    nnode = len(g)
    #1. Split the nodes.

    # divided graph
    divg = nx.Graph(g)

    for v in g:
        nei = [x for x in divg.neighbors(v)]
        assert len(nei) <= 4, "degree must be <=4"
        # fill by Nones if number of neighbors is less than 4
        nei = (nei + [None, None, None, None])[:4]
        # two neighbor nodes that are passed away to the new node
        migrate = set(random.sample(nei, 2)) - set([None])
        # new node label
        newv = v + nnode
        # assemble edges
        for x in migrate:
            divg.remove_edge(x,v)
            divg.add_edge(newv,x)

    # divg is made of chains and cycles.
    return divg


def make_digraph(g, divg):
    """
    Set the orientations to the components.

    divg: the divided graph made of chains and cycles.
          divg is an undirected graph.
    """
    nnode = len(g)

    paths = []
    for c in nx.connected_components(divg):
        # a component of c is either a chain or a cycle.
        subg = divg.subgraph(c)
        nn = len(subg)
        ne = len([e for e in subg.edges()])
        assert nn == ne or nn == ne+1
        path = find_path(subg)
        paths.append(path)

    # arrange the orientations here if you want to balance the polarization
    # ...

    # target
    dg = nx.DiGraph(g)

    for path in paths:
        for i,j in zip(path, path[1:]):
            dg.remove_edge(i%nnode,j%nnode)

    return dg


def ice_graph(g):
    """
    Make a digraph that obeys the ice rules.

    A new algorithm suggested by Prof. Sakuma, Yamagata University.
    """

    divg = divide(g)
    dg = make_digraph(g, divg)
    return dg
