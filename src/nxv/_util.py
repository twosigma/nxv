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
import heapq
from collections import OrderedDict

import networkx as nx


def _default_cost(u, v):
    return 1


def uniform_cost_traversal(sources, traverse, *, cost=None):
    """
    A Uniform-Cost Search without a goal.

    :param sources: An iterable of source nodes.
    :param traverse: A function ``f(u)`` that returns the successors of ``u``.
    :param cost: A function ``f(u, v)`` specifying the cost of traversing from ``u`` to ``v``.
    :return: Generates ``(c, u)`` where ``u`` is a traversed node and ``c`` is the cost of reaching that node.
    """
    if cost is None:
        cost = _default_cost

    visited = set()
    heap = []
    index = [0]

    def push(cu, u):
        heapq.heappush(heap, (cu, index[0], u))
        index[0] += 1

    def pop():
        cu, _, u = heapq.heappop(heap)
        return cu, u

    for u in sources:
        push(0, u)
    while heap:
        cu, u = pop()
        if u in visited:
            continue
        yield cu, u
        visited.add(u)
        for v in traverse(u):
            cv = cu + cost(u, v)
            push(cv, v)


def neighborhood(graph, nodes, *, radius=None, cost=None):
    """
    Get the subgraph in the neighborhood of the specified nodes.

    This is useful for viewing a small portion of a large graph.

    :param graph: A graph.
    :param nodes: An iterable of nodes.
    :param radius: The size of the neighborhood.
    :param cost: A function ``f(u, v)`` specifying the cost of traversing from ``u`` to ``v``.
    :return: The neighborhood subgraph.
    """

    def traverse(u):
        return nx.all_neighbors(graph, u)

    def subgraph_nodes():
        for cu, u in uniform_cost_traversal(nodes, traverse, cost=cost):
            if radius is not None and cu > radius:
                return
            yield u

    return graph.subgraph(subgraph_nodes())


def boundary(graph, subgraph):
    """
    Get the nodes in the subgraph that have neighbors in the graph but not in the subgraph.

    This is useful for conditionally styling nodes at the boundary of a subgraph. For example:

    ::

        boundary = nxv.boundary(graph, subgraph)
        style = nxv.Style(node=lambda u, d: {
            'style': 'dashed' if u in boundary else 'solid',
        })
        nxv.render(subgraph, style)


    :param graph: A graph.
    :param subgraph: A subgraph of the graph.
    :return: The nodes in the subgraph that have neighbors in the graph but not in the subgraph.
    """
    if not all(graph.has_node(node) for node in subgraph.nodes()):
        if all(subgraph.has_node(node) for node in graph.nodes()):
            raise ValueError(
                "The 'graph' argument is a proper subgraph of the 'subgraph' argument. This is likely "
                "because the arguments to boundary were passed in the wrong order."
            )
        else:
            raise ValueError("The subgraph contains nodes not in the graph.")
    return {
        node for node in subgraph.nodes() if subgraph.degree(node) < graph.degree(node)
    }


# directed, multi, ordered
GRAPH_TYPES = {
    (False, False, False): nx.Graph,
    (True, False, False): nx.DiGraph,
    (False, True, False): nx.MultiGraph,
    (True, True, False): nx.MultiDiGraph,
    (False, False, True): nx.OrderedGraph,
    (True, False, True): nx.OrderedDiGraph,
    (False, True, True): nx.OrderedMultiGraph,
    (True, True, True): nx.OrderedMultiDiGraph,
}
MULTI_GRAPH_TYPES = (
    nx.MultiGraph,
    nx.MultiDiGraph,
    nx.OrderedMultiGraph,
    nx.OrderedMultiDiGraph,
)
ORDERED_GRAPH_TYPES = (
    nx.OrderedGraph,
    nx.OrderedDiGraph,
    nx.OrderedMultiGraph,
    nx.OrderedMultiDiGraph,
)


def is_directed_graph(graph):
    """
    Get whether the graph has directed edges.

    :param graph: The graph.
    :return: True if the graph has directed edges.
    """
    return nx.is_directed(graph)


def is_multi_graph(graph):
    """
    Get whether the graph has multi-edges.

    :param graph: The graph.
    :return: True if the graph has multi-edges.
    """
    return isinstance(graph, MULTI_GRAPH_TYPES)


def is_ordered_graph(graph):
    """
    Get whether the graph has ordered nodes and edges.

    :param graph: The graph.
    :return: True if the graph has ordered nodes and edges.
    """
    return isinstance(graph, ORDERED_GRAPH_TYPES)


def create_graph(directed, multi, ordered):
    """
    Create an empty graph of the specified kind.

    :param directed: Should the graph have directed edges?
    :param multi: Should the graph allow multi-edges?
    :param ordered: Should the nodes and edges of the graph be ordered?
    :return: An empty graph of the specified type.
    """
    return GRAPH_TYPES[directed, multi, ordered]()


def to_ordered_graph(graph, node_key=None, edge_key=None, attr_key=None):
    """
    Create an ordered copy of the specified graph, with nodes and edges ordered by the specified key functions.

    :param graph: The graph to order.
    :param node_key: The node key function, ``node_key(u, d)``. Defaults to the identity function.
    :param edge_key: The edge key function, ``edge_key(u, v, d)``. If the graph has multi-edges, the signature should be
                     ``edge_key(u, v, k, d)`` instead, where ``k`` is the edge key. Defaults to the identity function.
    :param attr_key: The attribute key function, ``attr_key(k, v)``. Defaults to the identity function.
    :return: A copy of the graph with the nodes and edges ordered by the specified key functions.
    """
    result = create_graph(is_directed_graph(graph), is_multi_graph(graph), True)
    result.graph.update(graph.graph)
    for u, d in sorted(graph.nodes(data=True), key=node_key):
        result.add_node(u)
        result.nodes[u].update(OrderedDict(sorted(d.items(), key=attr_key)))
    if is_multi_graph(graph):
        for u, v, k, d in sorted(graph.edges(keys=True, data=True), key=edge_key):
            result.add_edge(u, v, k)
            result.edges[u, v, k].update(OrderedDict(sorted(d.items(), key=attr_key)))
    else:
        for u, v, d in sorted(graph.edges(data=True), key=edge_key):
            result.add_edge(u, v)
            result.edges[u, v].update(OrderedDict(sorted(d.items(), key=attr_key)))
    return result


def _relative_luminance_helper(x):
    if x <= 0.0:
        return 0.0
    if x <= 0.03928:
        return x / 12.92
    if x <= 1.0:
        return ((x + 0.055) / 1.055) ** 2.4
    return 1.0


def _relative_luminance(channels):
    # See: https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
    weights = (0.2126, 0.7152, 0.0722)
    return sum(
        weight * _relative_luminance_helper(channel)
        for weight, channel in zip(weights, channels)
    )


def _contrast_ratio(l1, l2):
    # See: https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def contrasting_color(channels, *, options=None):
    """
    Get a color that most contrasts with a specified color.

    :param channels: The RGB or RGBA color channels. Values should be in the range [0, 1].
    :param options: The possible contrasting colors. Defaults to black and white.
    :return: The color option that most contrasts the input color.
    """
    if options is None:
        options = ((0, 0, 0), (1, 1, 1))
    if not options:
        return (0, 0, 0)
    lum = _relative_luminance(channels)
    return max(
        options, key=lambda option: _contrast_ratio(lum, _relative_luminance(option))
    )
