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
import functools
import logging
import os
import shutil

import networkx as nx

import nxv

EXAMPLES = []
LOGGER = logging.getLogger("nxv")


def main():
    logging.basicConfig(level="INFO")
    build_examples()
    build_logo()


def build_examples():
    shutil.rmtree("docs/_static/example", ignore_errors=True)
    os.makedirs("docs/_static/example", exist_ok=True)
    for example in EXAMPLES:
        build_example(example)


def build_example(example):
    path = f"docs/_static/example/{example.__name__}.svg"
    LOGGER.info(f"Rendering {path}")
    with open(path, "wb") as f:
        f.write(nxv.render(**example(), format="svg"))


def register_example(example):
    EXAMPLES.append(example)
    return example


def after_example(predecessor_example):
    def decorator(example):
        @functools.wraps(example)
        def decorated_example():
            return example(**predecessor_example())

        return decorated_example

    return decorator


@register_example
def networkx_plus_graphviz():
    # BEGIN EXAMPLE
    graph = nx.DiGraph()
    graph.add_edge("NetworkX", "+")
    graph.add_edge("GraphViz", "+")
    graph.add_edge("+", "nxv")

    style = nxv.Style(
        node=lambda u, d: {"shape": "circle" if u == "+" else "box"},
    )
    style = nxv.compose([style, nxv.styles.font(fontname="Lato")])
    # END EXAMPLE
    return dict(graph=graph, style=style)


@register_example
def quickstart_graph():
    # BEGIN EXAMPLE
    graph = nx.Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    # END EXAMPLE
    return dict(graph=graph)


@register_example
@after_example(quickstart_graph)
def quickstart_graph_style(graph):
    # BEGIN EXAMPLE
    style = nxv.Style(
        graph={"rankdir": "LR"},
        node={"shape": "square"},
        edge={"style": "dashed"},
    )
    # END EXAMPLE
    return dict(graph=graph, style=style)


@register_example
@after_example(quickstart_graph)
def quickstart_graph_functional_style(graph):
    # BEGIN EXAMPLE
    style = nxv.Style(
        graph={"rankdir": "LR"},
        node=lambda u, d: {"shape": "circle" if u in "AEIOU" else "square"},
        edge=lambda u, v, d: {"style": "dashed", "label": u + v},
    )
    # END EXAMPLE
    return dict(graph=graph, style=style)


def build_logo():
    shutil.rmtree("docs/_static/logo", ignore_errors=True)
    os.makedirs("docs/_static/logo", exist_ok=True)
    graph = nx.Graph()
    nx.add_path(graph, [0, 1, 2, 3, 4, 5, 0])
    nx.add_star(graph, [6, 0, 1, 2, 3, 4, 5])
    style = nxv.Style(
        graph={
            "pad": 1 / 8,
            "bgcolor": "#00000000",
            "size": "1,1",
            "ratio": 1,
        },
        node=lambda u, d: {
            "shape": "circle",
            "label": None,
            "width": 3 / 4,
            "style": "filled",
            "fillcolor": "#009AA6" if u % 2 else "#E37222",
            "penwidth": 5,
        },
        edge={"penwidth": 5},
    )
    path = "docs/_static/logo/logo.svg"
    LOGGER.info(f"Rendering {path}")
    with open(path, "wb") as f:
        f.write(nxv.render(graph, style, algorithm="neato", format="svg"))
    for size in [16, 32, 40, 48, 64, 128, 256]:
        style_with_dpi = nxv.compose([style, nxv.Style(graph={"dpi": size})])
        path = f"docs/_static/logo/logo-{size}.png"
        LOGGER.info(f"Rendering {path}")
        with open(path, "wb") as f:
            f.write(nxv.render(graph, style_with_dpi, algorithm="neato", format="png"))


if __name__ == "__main__":
    main()
