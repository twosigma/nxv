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
from nxv._functional import _apply, chain, switch


def test_apply_lit():
    assert _apply(7) == 7


def test_apply_lit_ignores_arguments():
    assert _apply(7, "garbage1", garbage2="garbage3") == 7


def test_apply_func():
    assert _apply(lambda x, y: x + y, 2, 5) == 7


def test_apply_func_by_name():
    assert _apply(lambda x, y: x + y, x=2, y=5) == 7


def test_chain():
    func = chain([{"x": 7}, lambda name: {"name": name}, {"x": 8}])
    assert _apply(func, "john") == {"x": 8, "name": "john"}


def test_switch():
    func = switch(
        lambda x: x[0],
        {
            "A": lambda x: x.lower(),
            "B": lambda x: x.upper(),
        },
        default=lambda x: x[::-1],
    )
    assert _apply(func, "Apple") == "apple"
    assert _apply(func, "Banana") == "BANANA"
    assert _apply(func, "Cherry") == "yrrehC"
