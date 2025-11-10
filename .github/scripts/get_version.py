#!/usr/bin/env python3
"""
Get the current version from pyproject.toml
"""
import re
from pathlib import Path


def get_version():
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    # Find the current version
    version_pattern = r'version\s*=\s*"(\d+\.\d+\.\d+)"'
    match = re.search(version_pattern, content)

    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    return match.group(1)


if __name__ == "__main__":
    print(get_version())
