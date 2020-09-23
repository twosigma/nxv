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
import nxv


def test_styles_font_fontname():
    style = nxv.styles.font(fontname="monospace")
    assert style.graph == {"fontname": "monospace"}
    assert style.node == {"fontname": "monospace"}
    assert style.edge == {"fontname": "monospace"}


def test_styles_font_fontsize():
    style = nxv.styles.font(fontsize=20)
    assert style.graph == {"fontsize": 20}
    assert style.node == {"fontsize": 20}
    assert style.edge == {"fontsize": 20}


def test_styles_verbose():
    style = nxv.styles.verbose()
    assert style.graph(None, {"x": "y"}) == {
        "label": "Graph Attributes: {'x': 'y'}",
        "labelloc": "t",
    }
    assert style.node(1, {"a": "b"}) == {"label": "1\n{'a': 'b'}", "shape": "box"}
    assert style.edge(1, 2, {"a": "b"}) == {"label": "{'a': 'b'}"}
    assert style.edge(1, 2, "key", {"a": "b"}) == {"label": "key\n{'a': 'b'}"}
