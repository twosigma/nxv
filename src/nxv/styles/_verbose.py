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
from nxv._style import Style


def _verbose_edge(*args):
    if len(args) == 3:
        u, v, d = args
        return {"label": str(d)}
    else:
        u, v, e, d = args
        return {"label": f"{e}\n{d}"}


def verbose() -> Style:
    """
    Get a verbose :class:`~nxv.Style` that shows all of the data in a graph.

    :return: A verbose :class:`~nxv.Style`.
    """
    return Style(
        graph=lambda g, d: {"label": f"Graph Attributes: {d}", "labelloc": "t"},
        node=lambda u, d: {"label": f"{u}\n{d}", "shape": "box"},
        edge=_verbose_edge,
    )
