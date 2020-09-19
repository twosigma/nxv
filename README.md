<img src="./logo/logo-256.png" align="right" width="256px" height="256px">

# `nxv` renders NetworkX graphs using GraphViz

    import networkx as nx
    import nxv
    
    graph = nx.Graph()
    graph.add_edge("a", "b")
    output = nxv.render(graph, format="svg")
