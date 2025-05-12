#!/usr/bin/env python
from pathlib import Path
import re
from subprocess import check_output
from typing import Any

import click
from packaging.requirements import Requirement
import toml


@click.command(name="uvoutdated")
@click.help_option("-h", "--help")
@click.argument(
    "file",
    default=Path(".") / "pyproject.toml",
    metavar="pyproject.toml",
    type=click.Path(dir_okay=False, exists=True, readable=True),
)
def main(file: Path):
    """Print outdated direct dependencies in pyproject.toml."""
    project: dict[str, Any] = toml.load(file)["project"]
    deps: list[str] = [Requirement(dep).name for dep in project["dependencies"]]
    click.echo(outdated(deps), nl=False)


def outdated(deps: list[str]) -> str:
    output: str = ""
    # TODO cd to parent dir of path before running?
    outdated: str = check_output(["uv", "pip", "list", "--outdated"]).decode("utf-8")
    for index, line in enumerate(outdated.split("\n")):
        if index < 2:
            output += f"{line}\n"  # header rows
        else:
            pkg: str = line.split(" ")[0]
            for dep in deps:
                if re.match(r"^" + pkg + "$", dep):
                    output += f"{line}\n"
                    break
    return output


if __name__ == "__main__":
    main()
