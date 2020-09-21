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
import tempfile

import nox

PYTHON_VERSIONS = ["3.6", "3.7", "3.8"]
SOURCES = ["src", "tests", "noxfile.py"]


def install_with_constraints(session, *args, **kwargs):
    with tempfile.TemporaryDirectory() as temp:
        requirements = os.path.join(temp, "requirements.txt")
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements}",
            external=True,
        )
        session.install(f"--constraint={requirements}", *args, **kwargs)


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    args = session.posargs or SOURCES
    install_with_constraints(
        session, "flake8", "flake8-black", "flake8-bugbear", "flake8-import-order"
    )
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", *args, external=True)
