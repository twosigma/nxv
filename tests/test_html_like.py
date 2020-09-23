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
import nxv.html_like as H


def test_html_like_str():
    cases = [
        (H.join([]), ""),
        (
            H.join([H.bold("hello"), H.line_break(), H.italic("world")]),
            "<B>hello</B><BR/><I>world</I>",
        ),
        (
            H.font("x = 7", {"fontname": "monospace"}),
            '<FONT fontname="monospace">x = 7</FONT>',
        ),
        (H.underline("ABC"), "<U>ABC</U>"),
        (H.overline("ABC"), "<O>ABC</O>"),
        (H.join(["x", H.subscript("0")]), "x<SUB>0</SUB>"),
        (H.join(["i", H.superscript("2"), " = -1"]), "i<SUP>2</SUP> = -1"),
        (H.strikethrough("todo"), "<S>todo</S>"),
        (
            H.table([H.table_row([H.table_cell("x")])]),
            "<TABLE><TR><TD>x</TD></TR></TABLE>",
        ),
        (H.horizontal_rule(), "<HR/>"),
        (H.vertical_rule(), "<VR/>"),
        (H.image({"url": "http://example.com"}), '<IMG url="http://example.com"/>'),
    ]
    for value, expected in cases:
        actual = str(value)
        assert actual == expected


def test_html_like_repr():
    value = H.horizontal_rule()
    actual = repr(value)
    expected = "HtmlLike('HR', children=None, attributes={})"
    assert actual == expected
