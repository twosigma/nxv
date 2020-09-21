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
"""Utilities for interacting with the IPython execution context."""


def is_execution_context() -> bool:
    """Returns whether the current execution context is IPython."""
    try:
        return bool(__IPYTHON__)
    except NameError:
        return False


def assert_execution_context():
    """Asserts that the current execution context is IPython."""
    if not is_execution_context():
        raise ValueError(
            "Must be running in an IPython execution context "
            "to use an ipython/* format."
        )


def display(data, format):
    """Display SVG or image data in the current IPython execution context."""
    assert_execution_context()
    from IPython.display import SVG, Image, display

    formats = {"ipython/svg": SVG, "ipython/png": Image}
    constructor = formats.get(format, None)
    if constructor is None:
        raise ValueError(
            f"Invalid IPython format {format!r}. "
            f"Valid IPython formats are {set(formats)}."
        )
    display(constructor(data))
