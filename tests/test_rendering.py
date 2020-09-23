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
import textwrap

import networkx as nx
import pytest

import nxv
import nxv.html_like as H


def test_render():
    graph = nx.DiGraph()
    nx.add_path(graph, [0, 1, 2, 3])
    graph.add_edges_from([("even", 0), ("even", 2), ("odd", 1), ("odd", 3)])

    def int_color(n):
        return "gray" if n % 2 == 0 else "darkred"

    style = nxv.Style(
        graph={"label": "Beware the odd numbers!", "labelloc": "t"},
        node=nxv.switch(
            lambda u, d: type(u),
            {
                str: {"shape": "diamond"},
                int: lambda u, d: {
                    "shape": "circle",
                    "style": "filled",
                    "color": int_color(u),
                    "fontcolor": "white",
                },
            },
        ),
        edge=nxv.switch(
            lambda u, v, d: (type(u), type(v)),
            {
                (str, int): lambda u, v, d: {"color": int_color(v)},
                (int, int): {"dir": "none", "style": "dashed"},
            },
        ),
    )

    nxv.render(graph, style, format="svg")


def test_render_multi():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, key="LessThan")
    graph.add_edge(0, 2, key="LessThan")
    graph.add_edge(1, 2, key="LessThan")
    graph.add_edge(0, 1, key="Successor")
    graph.add_edge(1, 2, key="Successor")

    style = nxv.Style(
        edge=nxv.switch(
            lambda u, v, k, d: k,
            {
                "LessThan": lambda u, v, k, d: {
                    "color": "red",
                    "label": f"{u} < {v}",
                },
                "Successor": lambda u, v, k, d: {
                    "color": "blue",
                    "label": f"{u} + 1 = {v}",
                },
            },
        )
    )

    nxv.render(graph, style, format="svg")


def test_render_strange_characters():
    graph = nx.Graph()
    nx.add_path(graph, range(1000))
    style = nxv.Style(node=lambda u, d: {"label": f"{u}:{chr(u)}"})
    nxv.render(graph, style, format="svg")


def test_multiline_labels():
    graph = nx.OrderedDiGraph()
    graph.add_node(0, label="A\nB")
    graph.add_node(1, label="C\nD")
    graph.add_edge(0, 1)
    style = nxv.Style(node=lambda u, d: d)
    actual = nxv.render(graph, style, format="raw")
    expected = textwrap.dedent(
        """
        digraph "G" {
            graph [];
            node0000 [label="A
        B"];
            node0001 [label="C
        D"];
            node0000 -> node0001 [];
        }
        """
    ).strip()
    assert actual == expected


def test_html_like_labels():
    graph = nx.OrderedDiGraph()
    graph.add_node(
        0,
        label=H.table(
            [
                H.table_row([H.table_cell("A", attributes={"COLSPAN": 2})]),
                H.table_row([H.table_cell("C"), H.table_cell("D")]),
            ]
        ),
    )
    graph.add_node(1, label=H.bold('3 < 7 "hello" & "world" 5 > 2'))
    graph.add_node(2, label=H.join(["hello", H.italic("world")]))
    graph.add_edge(0, 1)
    style = nxv.Style(node=lambda u, d: d)
    actual = nxv.render(graph, style, format="raw")
    expected = textwrap.dedent(
        """
        digraph "G" {
            graph [];
            node0000 [label=<<TABLE><TR><TD COLSPAN="2">A</TD></TR><TR><TD>C</TD><TD>D</TD></TR></TABLE>>];
            node0001 [label=<<B>3 &lt; 7 &quot;hello&quot; &amp; &quot;world&quot; 5 &gt; 2</B>>];
            node0002 [label=<hello<I>world</I>>];
            node0000 -> node0001 [];
        }
        """
    ).strip()
    assert actual == expected


def test_subgraph_indentation():
    graph = nx.OrderedDiGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B")
    actual = nxv.render(graph, subgraph_func=lambda u, d: u, format="raw")
    expected = textwrap.dedent(
        """
        digraph "G" {
            graph [];
            subgraph "A" {
                graph [];
                node0000 [label="A"];
            }
            subgraph "B" {
                graph [];
                node0001 [label="B"];
            }
            node0000 -> node0001 [];
        }
        """
    ).strip()
    assert actual == expected


def test_color():
    from nxv._rendering import color

    instances = [
        ((0, 0, 0), "#000000"),
        ((1, 1, 1), "#FFFFFF"),
        ((0, 0, 0, 0), "#00000000"),
        ((1, 1, 1, 1), "#FFFFFFFF"),
        ((0.5, 0.5, 0.5), "#808080"),
        ((0.5, 0.5, 0.5, 0.5), "#80808080"),
    ]
    for channels, expected in instances:
        actual = color(channels)
        assert actual == expected


def test_render_invalid():
    graph = nx.Graph()
    graph.add_node(0)
    style = nxv.Style(
        node={"label": H.table(["x"], attributes={"notanattribute": "y"})}
    )
    with pytest.raises(nxv.GraphVizError):
        nxv.render(graph, style, format="svg")
