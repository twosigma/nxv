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
import logging
import os
from functools import wraps

import networkx as nx

import nxv

EXAMPLES = []
LOGGER = logging.getLogger("nxv")


def main():
    logging.basicConfig(level="INFO")
    os.makedirs("docs/_static/example", exist_ok=True)
    for example in EXAMPLES:
        run_example(example)


def run_example(example):
    path = f"docs/_static/example/{example.__name__}.svg"
    with open(path, "wb") as f:
        LOGGER.info(f"Rendering {path}")
        f.write(nxv.render(**example(), format="svg"))


def register_example(example):
    EXAMPLES.append(example)
    return example


def after_example(predecessor_example):
    def decorator(example):
        @wraps(example)
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


if __name__ == "__main__":
    main()
