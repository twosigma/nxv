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
"""
Functions for building GraphViz HTML-like labels.

See https://www.graphviz.org/doc/info/shapes.html#html
"""

from nxv.html_like._html_like import (
    bold,
    font,
    horizontal_rule,
    image,
    italic,
    join,
    line_break,
    overline,
    strikethrough,
    subscript,
    superscript,
    table,
    table_cell,
    table_row,
    underline,
    vertical_rule,
)

__all__ = [
    "join",
    "line_break",
    "font",
    "italic",
    "bold",
    "underline",
    "overline",
    "subscript",
    "superscript",
    "strikethrough",
    "table",
    "table_row",
    "horizontal_rule",
    "table_cell",
    "vertical_rule",
    "image",
]
