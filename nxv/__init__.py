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
"""Render NetworkX graphs using GraphViz"""

__author__ = "Timothy Shields"
__maintainer__ = "Timothy Shields"
__email__ = "Timothy.Shields@twosigma.com"
__version__ = "0.1.0"

from nxv import html_like, styles
from nxv._functional import chain, switch
from nxv._graphviz import (
    GraphVizAlgorithmNotFoundError,
    GraphVizError,
    GraphVizInstallationNotFoundError,
)
from nxv._rendering import render
from nxv._style import Style
from nxv._util import boundary, contrasting_color, neighborhood, to_ordered_graph

__all__ = [
    "render",
    "Style",
    "chain",
    "switch",
    "neighborhood",
    "boundary",
    "to_ordered_graph",
    "contrasting_color",
    "styles",
    "html_like",
    "GraphVizInstallationNotFoundError",
    "GraphVizAlgorithmNotFoundError",
    "GraphVizError",
]
