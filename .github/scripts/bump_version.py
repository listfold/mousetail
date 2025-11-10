#!/usr/bin/env python3
"""
Automatically increment the patch version in pyproject.toml
"""
import re
from pathlib import Path


def bump_version():
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    # Find the current version
    version_pattern = r'version\s*=\s*"(\d+)\.(\d+)\.(\d+)"'
    match = re.search(version_pattern, content)

    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    major, minor, patch = match.groups()
    new_patch = int(patch) + 1
    new_version = f"{major}.{minor}.{new_patch}"

    # Replace the version
    new_content = re.sub(
        version_pattern,
        f'version = "{new_version}"',
        content
    )

    pyproject_path.write_text(new_content)
    print(f"Version bumped to {new_version}")
    return new_version


if __name__ == "__main__":
    bump_version()
