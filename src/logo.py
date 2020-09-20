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
import os

import networkx as nx

import nxv


def main():
    os.makedirs("docs/_static/logo", exist_ok=True)
    graph = nx.Graph()
    nx.add_path(graph, [0, 1, 2, 3, 4, 5, 0])
    nx.add_star(graph, [6, 0, 1, 2, 3, 4, 5])
    for size in [16, 32, 40, 48, 64, 128, 256]:
        style = nxv.Style(
            graph={
                "pad": 1 / 8,
                "bgcolor": "#00000000",
                "size": "1,1",
                "ratio": 1,
                "dpi": size,
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
        for format in ["svg", "png"]:
            output = nxv.render(graph, style, algorithm="neato", format=format)
            with open(f"docs/_static/logo/logo-{size}.{format}", "wb") as f:
                f.write(output)


if __name__ == "__main__":
    main()
