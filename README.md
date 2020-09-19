<img src="./logo/logo-128.png" align="right" width="128px" height="128px">

# `nxv` renders NetworkX graphs using GraphViz

    import networkx as nx
    import nxv
    
    graph = nx.Graph()
    graph.add_edge("a", "b")
    output = nxv.render(graph, format="svg")
