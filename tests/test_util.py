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
import networkx as nx
import pytest

from nxv import _util


def test_uniform_cost_traversal_unorderable_nodes():
    a, b, c, d = [object() for _ in range(4)]
    graph = nx.Graph()
    graph.add_edge(a, b)
    graph.add_edge(c, d)
    actual = list(_util.uniform_cost_traversal([a, c], graph.neighbors))
    expected = [(0, a), (0, c), (1, b), (1, d)]
    assert actual == expected


def test_neighborhood():
    g = nx.Graph()
    g.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
    h = _util.neighborhood(g, [1], radius=2)
    assert set(h.nodes()) == {1, 2, 3, 4}
    assert set(h.edges()) == {(1, 2), (1, 3), (2, 3), (3, 4)}


def test_boundary():
    g = nx.Graph()
    g.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
    h = g.subgraph({1, 2, 3})
    assert _util.boundary(g, h), {3}


def test_boundary_wrong_argument_order():
    g = nx.Graph()
    g.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
    h = g.subgraph({1, 2, 3})
    with pytest.raises(ValueError) as info:
        _util.boundary(h, g)
    assert str(info.value) == (
        "The 'graph' argument is a proper subgraph of the 'subgraph' "
        "argument. This is likely because the arguments to boundary were "
        "passed in the wrong order."
    )


def test_boundary_invalid_subgraph():
    g = nx.Graph()
    g.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
    h = nx.Graph()
    h.add_nodes_from([1, 2, 3, 7])
    with pytest.raises(ValueError) as info:
        _util.boundary(g, h)
    assert str(info.value) == "The subgraph contains nodes not in the graph."


def test_default_key_functions():
    g = nx.Graph()
    g.add_edges_from([(2, 0), (1, 2), (1, 0)])
    h = _util.to_ordered_graph(g)
    assert list(h.nodes()) == [0, 1, 2]
    assert list(h.edges()) == [(0, 1), (0, 2), (1, 2)]


def test_contrasting_color():
    instances = [
        ((0, 0, 0), (1, 1, 1)),
        ((1, 0, 0), (0, 0, 0)),
        ((0, 1, 0), (0, 0, 0)),
        ((0, 0, 1), (1, 1, 1)),
        ((1, 1, 0), (0, 0, 0)),
        ((1, 0, 1), (0, 0, 0)),
        ((0, 1, 1), (0, 0, 0)),
        ((1, 1, 1), (0, 0, 0)),
    ]
    for channels, expected in instances:
        assert _util.contrasting_color(channels) == expected
