import os

from pathlib import Path

import nox

PYTHON_ALL_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session: nox.Session) -> None:
    session.install("pytest")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.resolve(strict=True))
    session.run("pytest", "test", env=env)
