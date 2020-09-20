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
from typing import Iterable, Optional

from nxv._functional import chain


class Style:
    """
    A specification for how to style a `NetworkX`_ graph using `GraphViz`_.

    See the `GraphViz attributes`_ documentation for information on what attributes
    are available to use with the ``graph``, ``node``, ``edge``, and ``subgraph`` parameters.

    :param graph: An optional dict of `GraphViz graph attributes`_, or a function ``f(g, d)`` that returns it, in which
                  ``g`` is the `NetworkX`_ graph and ``d`` is its attribute dict.
    :param node: An optional dict of `GraphViz node attributes`_, or a function ``f(u, d)`` that returns it, in which
                 ``u`` is a `NetworkX`_ node and ``d`` is its attribute dict.
    :param edge: An optional dict of `GraphViz edge attributes`_, or a function ``f(u, v, d)`` that returns it, in which
                 ``(u, v)`` is a `NetworkX`_ edge and ``d`` is its attribute dict. If styling a graph with multi-edges,
                 the signature should be ``f(u, v, k, d)`` instead, where ``k`` is the edge key.
    :param subgraph: An optional dict of `GraphViz subgraph attributes`_, or a function ``f(s)`` that returns it, in which
                     ``s`` is a subgraph key. This only applies when calling ``nxv.render`` with a ``subgraph_func``.
    """

    def __init__(self, *, graph=None, node=None, edge=None, subgraph=None):
        self.graph = graph or {}
        self.node = node or {}
        self.edge = edge or {}
        self.subgraph = subgraph or {}


def compose(styles: Iterable[Optional[Style]]) -> Style:
    """
    Compose a sequence of :class:`~nxv.Style` objects as a single :class:`~nxv.Style`.

    :param styles: An iterable of :class:`~nxv.Style` objects.
    :return: The composed :class:`~nxv.Style`.
    """
    styles = [style for style in styles if style]
    return Style(
        graph=chain(style.graph for style in styles),
        node=chain(style.node for style in styles),
        edge=chain(style.edge for style in styles),
        subgraph=chain(style.subgraph for style in styles),
    )
