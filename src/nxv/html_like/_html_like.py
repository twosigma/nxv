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
def render_html_like_str(value):
    # It's very important we escape '&' first, as it is itself used in escaping.
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_html_like(value):
    if isinstance(value, HtmlLike):
        return str(value)
    return render_html_like_str(value)


class HtmlLike:
    def __init__(self, name, children=None, attributes=None):
        self.name = name
        self.children = None if children is None else tuple(children)
        self.attributes = {k: v for k, v in (attributes or {}).items() if v is not None}

    def __str__(self):
        children = (
            None
            if self.children is None
            else "".join(render_html_like(child) for child in self.children)
        )
        attrs = "".join(
            f' {k}="{render_html_like_str(v)}"' for k, v in self.attributes.items()
        )
        if self.name is None:
            assert not attrs
            return children or ""
        if self.children is None:
            return f"<{self.name}{attrs}/>"
        return f"<{self.name}{attrs}>{children}</{self.name}>"

    def __repr__(self):
        return f"HtmlLike({self.name!r}, children={self.children!r}, attributes={self.attributes!r})"


def join(children):
    return HtmlLike(None, children=children)


def line_break(attributes=None):
    return HtmlLike("BR", attributes=attributes)


def font(content, attributes=None):
    return HtmlLike("FONT", children=[content], attributes=attributes)


def italic(content):
    return HtmlLike("I", children=[content])


def bold(content):
    return HtmlLike("B", children=[content])


def underline(content):
    return HtmlLike("U", children=[content])


def overline(content):
    return HtmlLike("O", children=[content])


def subscript(content):
    return HtmlLike("SUB", children=[content])


def superscript(content):
    return HtmlLike("SUP", children=[content])


def strikethrough(content):
    return HtmlLike("S", children=[content])


def table(rows, attributes=None):
    return HtmlLike("TABLE", children=rows, attributes=attributes)


def table_row(cells):
    return HtmlLike("TR", children=cells)


def horizontal_rule():
    return HtmlLike("HR")


def table_cell(content, attributes=None):
    return HtmlLike("TD", children=[content], attributes=attributes)


def vertical_rule():
    return HtmlLike("VR")


def image(attributes=None):
    return HtmlLike("IMG", attributes=attributes)
