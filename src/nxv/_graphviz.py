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
import os
import platform
import re
from functools import lru_cache
from subprocess import PIPE, Popen
from typing import List, Optional


@lru_cache()
def is_windows() -> bool:
    return platform.system().lower() == "windows"


@lru_cache()
def get_windows_program_files() -> List[str]:
    possible = ["C:\\Program Files\\", "C:\\Program Files (x86)\\"]
    return [path for path in possible if os.path.isdir(path)]


@lru_cache()
def get_windows_graphviz_bins() -> List[str]:
    return [
        os.path.join(program_files, name, "bin")
        for program_files in get_windows_program_files()
        for name in os.listdir(program_files)
        if name.lower().startswith("graphviz")
        if os.path.isdir(os.path.join(program_files, name))
        if os.path.isdir(os.path.join(program_files, name, "bin"))
    ]


@lru_cache()
def try_get_graphviz_algorithm_path(graphviz_bin: str, algorithm: str) -> Optional[str]:
    for name in [algorithm, f"{algorithm}.exe"]:
        path = os.path.join(graphviz_bin, name)
        if os.path.isfile(path):
            return path
    return None


@lru_cache()
def get_graphviz_bins(graphviz_bin: Optional[str]) -> List[str]:
    from nxv import GraphVizInstallationNotFoundError

    if graphviz_bin:
        if not os.path.isdir(graphviz_bin):
            raise GraphVizInstallationNotFoundError(
                f"No GraphViz installation was found at the location specified "
                f"by the graphviz_bin parameter: {graphviz_bin}"
            )
        return [graphviz_bin]

    graphviz_bin = os.environ.get("GRAPHVIZ_BIN")
    if graphviz_bin:
        if not os.path.isdir(graphviz_bin):
            raise GraphVizInstallationNotFoundError(
                f"No GraphViz installation was found at the location specified "
                f"by the GRAPHVIZ_BIN environment variable: {graphviz_bin}"
            )
        return [graphviz_bin]

    if is_windows():
        graphviz_bins = get_windows_graphviz_bins()
        if not graphviz_bins:
            raise GraphVizInstallationNotFoundError(
                "No GraphViz installation was found at any of the standard Windows locations."
            )
        return graphviz_bins

    raise GraphVizInstallationNotFoundError(
        "No GraphViz installation was specified. "
        "Use either the graphviz_bin parameter or the GRAPHVIZ_BIN environment variable."
    )


@lru_cache()
def get_graphviz_algorithm_path(graphviz_bin: Optional[str], algorithm: str) -> str:
    from nxv import GraphVizAlgorithmNotFoundError

    graphviz_bins = get_graphviz_bins(graphviz_bin)
    for graphviz_bin in graphviz_bins:
        path = try_get_graphviz_algorithm_path(graphviz_bin, algorithm)
        if path:
            return path
    graphviz_bins_str = " OR ".join(graphviz_bins)
    raise GraphVizAlgorithmNotFoundError(
        f"No GraphViz algorithm named {algorithm} was found in the GraphViz installation: {graphviz_bins_str}"
    )


def run(gv, algorithm, format, graphviz_bin):
    """
    Runs a `GraphViz`_ layout algorithm on a `GraphViz`_ string to product an output with the specified format.

    :param gv: A `GraphViz`_ string.
    :param algorithm: A `GraphViz`_ layout algorithm.
    :param format: A `GraphViz`_ output format.
    :param graphviz_bin: The bin directory of the `GraphViz`_ installation.
                         Defaults to the ``GRAPHVIZ_BIN`` environment variable.
    :return: The output bytes.
    :raises GraphVizError: If `GraphViz`_ failed to run on the given inputs.
    """
    from nxv import GraphVizError

    algorithm_path = get_graphviz_algorithm_path(graphviz_bin, algorithm)
    p = Popen(
        [algorithm_path, f"-T{format}"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdin = gv.encode("utf-8")
    stdout, stderr = p.communicate(stdin)
    if p.returncode == 0:
        return stdout
    message = stderr.decode("utf-8")
    line_numbers = set(
        int(match.group(1)) for match in re.finditer(r"line (\d+)", message)
    )
    context_line_numbers = set(
        line_number + offset for line_number in line_numbers for offset in range(-2, 3)
    )
    if line_numbers:

        def prefix(line_number):
            return ">>>" if line_number in line_numbers else "   "

        message = "\n".join(
            [
                message,
                "   Line |",
                *(
                    f"{prefix(i)}{i:>4} | {line}"
                    for i, line in enumerate(gv.splitlines(), 1)
                    if i in context_line_numbers
                ),
            ]
        )
    raise GraphVizError(message)
