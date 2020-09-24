#
# Copyright 2020 Two Sigma Open Source, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Optional, Union

import networkx as nx

from nxv import _graphviz, _ipython
from nxv._functional import _apply
from nxv._style import Style, compose
from nxv._util import is_multi_graph
from nxv.html_like._html_like import HtmlLike, render_html_like

_root_style = Style(node=lambda u, d: {"label": str(u)})

COLOR_ATTRIBUTES = {
    "bgcolor",
    "color",
    "fillcolor",
    "fontcolor",
    "labelfontcolor",
    "pencolor",
}
LABEL_ATTRIBUTES = {"label", "headlabel", "taillabel"}


def _to_gv_string(value, attribute=None):
    if value is None:
        return '""'
    if attribute is not None:
        if attribute in COLOR_ATTRIBUTES and not isinstance(value, str):
            return _to_gv_string(color(value))
        if attribute in LABEL_ATTRIBUTES and isinstance(value, HtmlLike):
            return "<" + render_html_like(value) + ">"
    value = str(value)
    if not value:
        return '""'
    escape_char = "\\"
    need_escape = {'"', escape_char}

    # These characters break GraphViz
    broken_chars = {chr(0), chr(26)}

    if set(value) & (need_escape | broken_chars):
        value = "".join(
            escape_char + c if c in need_escape else c
            for c in value
            if c not in broken_chars
        )

    return f'"{value}"'


def _attributes_modifier(attrs):
    attrs_str = ", ".join(
        f"{k}={_to_gv_string(v, attribute=k)}" for k, v in attrs.items()
    )
    return f"[{attrs_str}]"


def _graph_identifier(graph_type, name):
    assert graph_type in {"graph", "digraph", "subgraph"}
    return f"{graph_type} {_to_gv_string(name)}"


def _graph_attrs_declaration(attrs):
    return f"graph {_attributes_modifier(attrs)};"


def _indent(value):
    return 4 * " " + value


def _block(prefix, lines):
    begin = (prefix + " {") if prefix else "{"
    end = "}"
    return [begin] + list(map(_indent, lines)) + [end]


def _default_subgraph_func(u, d):
    return None


def _to_gv(graph, style: Style, subgraph_func=None):
    """
    Serializes a `NetworkX`_ graph as a `GraphViz`_ string.

    :param graph: A `NetworkX`_ ``Graph``, ``DiGraph``, ``MultiGraph``, or ``MultiDiGraph``.
    :param style: A :class:`~nxv.Style` object.
    :param subgraph_func: An optional function ``f(u, d)`` that returns a subgraph key,
                          where ``u`` is a `NetworkX`_ node and ``d`` is its attribute dict.
    :return: The raw `GraphViz`_ string format to pass as input to one of the GraphViz layout algorithms.
    """

    if subgraph_func is None:
        subgraph_func = _default_subgraph_func

    graph_attrs = _apply(style.graph, graph, graph.graph)
    graph_type = graph_attrs.get(
        "type", "digraph" if nx.is_directed(graph) else "graph"
    )
    assert graph_type in {"graph", "digraph"}
    edge_str = {"graph": "--", "digraph": "->"}[graph_type]
    ids = {u: f"node{i:04}" for i, u in enumerate(graph.nodes())}

    no_subgraph_nodes = []
    subgraph_nodes = {}
    for u, d in graph.nodes(data=True):
        subgraph = _apply(subgraph_func, u, d)
        if subgraph is None:
            no_subgraph_nodes.append((u, d))
        else:
            subgraph_nodes.setdefault(subgraph, []).append((u, d))

    def node_declaration(u, d):
        node_attrs = _apply(style.node, u, d)
        return f"{ids[u]} {_attributes_modifier(node_attrs)};"

    def edge_declaration(*edge):
        u, v = edge[:2]
        edge_attrs = _apply(style.edge, *edge)
        return f"{ids[u]} {edge_str} {ids[v]} {_attributes_modifier(edge_attrs)};"

    def subgraph_declaration(subgraph, nodes, attrs):
        return _block(
            _graph_identifier("subgraph", attrs.get("name", str(subgraph))),
            [_graph_attrs_declaration(attrs)]
            + [node_declaration(u, d) for u, d in nodes],
        )

    edges_kwargs = (
        {"keys": True, "data": True} if is_multi_graph(graph) else {"data": True}
    )

    lines = _block(
        _graph_identifier(graph_type, graph_attrs.get("name", "G")),
        (
            [_graph_attrs_declaration(graph_attrs)]
            + [node_declaration(u, d) for u, d in no_subgraph_nodes]
            + [
                line
                for subgraph, nodes in subgraph_nodes.items()
                for line in subgraph_declaration(
                    subgraph, nodes, _apply(style.subgraph, subgraph)
                )
            ]
            + [edge_declaration(*edge) for edge in graph.edges(**edges_kwargs)]
        ),
    )

    return "\n".join(lines)


def render(
    graph: Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph],
    style: Optional[Style] = None,
    *,
    algorithm: Optional[str] = None,
    format: Optional[str] = None,
    graphviz_bin: Optional[str] = None,
    subgraph_func=None,
) -> Optional[bytes]:
    """
    Render a `NetworkX`_ graph using `GraphViz`_.

    In a Jupyter notebook, this will automatically display as an SVG.

    :param graph: A `NetworkX`_ graph.
    :param style: A style specifying how graph nodes and edges should map to `GraphViz attributes`_.
    :param subgraph_func: An optional function ``f(u, d)`` that returns a subgraph key,
                          where ``u`` is a `NetworkX`_ node and ``d`` is its attribute dict.
                          If it returns ``None`` the node is not in any subgraph.
    :param algorithm: The `GraphViz`_ layout algorithm.
                      Valid options include
                      ``"circo"``, ``"dot"``, ``"fdp"``, ``"neato"``, ``"osage"``, ``"sfdp"``, ``"twopi"``.
                      Defaults to ``"dot"``.
    :param format: The `GraphViz`_ output format. Valid options include ``"svg"`` and ``"raw"``. In a Jupyter
                   notebook, prefixing the ``format`` with ``"ipython/"`` will automatically display the rendered
                   output.
                   When running in an interactive setting like a Jupyter notebook, the default is ``"ipython/svg"``.
                   Otherwise, this parameter is required.
    :param graphviz_bin: The ``bin`` directory of the `GraphViz`_ installation.
                         Defaults to the ``GRAPHVIZ_BIN`` environment variable.
                         If neither this parameter nor the ``GRAPHVIZ_BIN`` environment variable is set,
                         then nxv will try to autodetect the ``bin`` directory of the `GraphViz`_ installation.
                         This behavior is for convenience and should not be relied on in production settings.
    :return: If ``format`` is not an ``"ipython/*"`` format, the render output; otherwise, ``None``.
    :raises GraphVizInstallationNotFoundError: If nxv cannot find a `GraphViz`_ installation.
    :raises GraphVizAlgorithmNotFoundError: If nxv cannot find the specified algorithm in a `GraphViz`_ installation.
    :raises GraphVizError: If `GraphViz`_ failed to run on the given inputs.
    """
    if algorithm is None:
        algorithm = "dot"
    if not algorithm or not isinstance(algorithm, str):
        raise ValueError("The algorithm parameter must be the str name of a valid GraphViz algorithm.")

    if format is None:
        if _ipython.is_execution_context():
            format = "ipython/svg"
        else:
            raise ValueError(
                "You must specify a format when not in an IPython execution context."
            )

    is_ipython_format = format.startswith("ipython/")
    if is_ipython_format:
        _ipython.assert_execution_context()
    graphviz_format = format.split("/", 1)[1] if is_ipython_format else format

    style = compose([_root_style, style])
    gv = _to_gv(graph, style, subgraph_func=subgraph_func)

    if graphviz_format == "raw":
        if is_ipython_format:
            print(gv)
            return None
        else:
            return gv

    output = _graphviz.run(gv, algorithm, graphviz_format, graphviz_bin)

    if is_ipython_format:
        _ipython.display(output, format)
        return None
    else:
        return output


def _clamp(a, b, value):
    return max(a, min(b, value))


def _to_byte(value):
    return _clamp(0, 255, int(256 * float(value)))


def color(channels):
    """
    Convert RGB or RGBA color channel values to a `GraphViz`_ color string.

    :param channels: The color channel values, either RGB or RGBA. Values should be in the range [0, 1].
    :return: The `GraphViz`_ color string.
    """
    assert len(channels) in (3, 4)
    return "#" + "".join(f"{_to_byte(value):02X}" for value in channels)
