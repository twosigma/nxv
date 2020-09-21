<img src="./docs/_static/logo/logo-128.png" align="right" width="128px" height="128px">

# `nxv` renders NetworkX graphs using GraphViz

    import networkx as nx
    import nxv
    
    graph = nx.Graph()
    style = nxv.Style(...)
    nxv.render(graph, style)

# Developing

- Install poetry: https://python-poetry.org/
- `pip install --user nox`