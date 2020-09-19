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
"""Utilities for composing functions"""


def _apply(func, *args, **kwargs):
    """
    Applies a maybe-function to positional and named arguments.

    The result is ``func(*args, **kwargs)`` if ``callable(func)``, otherwise ``func``.

    :param func: A value that is optionally callable.
    :param args: The positional arguments passed to ``func``, if it is callable.
    :param kwargs: The named arguments passed to ``func``, if it is callable.
    :return: ``func(*args, **kwargs)`` if ``callable(func)``. Otherwise, returns ``func``.
    """
    if callable(func):
        return func(*args, **kwargs)
    else:
        return func


def chain(funcs):
    """
    Chains a sequence of dict-returning functions together to form a new dict-returning function.

    The result is a function ``f(*args, **kwargs)`` that returns
    ``{**apply(funcs[0], *args, **kwargs), **apply(funcs[1], *args, **kwargs), ...}``.

    :param funcs: An iterable of functions that return dicts.
    :return: A function ``f(*args, **kwargs)`` that returns
             ``{**apply(funcs[0], *args, **kwargs), **apply(funcs[1], *args, **kwargs), ...}``.
    """
    funcs = list(funcs)

    def func(*args, **kwargs):
        result = {}
        for f in funcs:
            result.update(_apply(f, *args, **kwargs))
        return result

    return func


def switch(key, funcs, *, default=None):
    """
    Combines a dict of keyed functions to form a new function.

    The result is a function ``f(*args, **kwargs)`` that returns
    ``apply(funcs[key(*args, **kwargs)], *args, **kwargs)``.

    If ``key(*args, **kwargs)`` is not in ``funcs`` but ``default`` is present,
    ``apply(default, *args, **kwargs)`` will be returned instead.

    :param key: The key selector function.
    :param funcs: The mapping from keys to functions.
    :param default: An optional default function for keys that do not appear in ``funcs``.
    :return: The function ``f(*args, **kwargs)`` that returns ``apply(funcs[key(*args, **kwargs)], *args, **kwargs)``.
    """

    def func(*args, **kwargs):
        k = key(*args, **kwargs)
        if k not in funcs and default is not None:
            return _apply(default, *args, **kwargs)
        return _apply(funcs[k], *args, **kwargs)

    return func
