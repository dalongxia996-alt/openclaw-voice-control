#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
REQUIREMENTS = ROOT / "requirements.txt"


def parse_pyproject_dependencies(text: str) -> list[str]:
    lines = text.splitlines()
    in_deps = False
    deps: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line.startswith("dependencies") and line.endswith("["):
            in_deps = True
            continue
        if in_deps and line == "]":
            break
        if in_deps:
            if line.endswith(","):
                line = line[:-1]
            if line.startswith('"') and line.endswith('"'):
                deps.append(line[1:-1])
    return deps


def parse_requirements(text: str) -> list[str]:
    deps: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        deps.append(line)
    return deps


def main() -> int:
    pyproject_deps = parse_pyproject_dependencies(PYPROJECT.read_text(encoding="utf-8"))
    requirements_deps = parse_requirements(REQUIREMENTS.read_text(encoding="utf-8"))

    py_set = set(pyproject_deps)
    req_set = set(requirements_deps)

    missing_in_requirements = sorted(py_set - req_set)
    missing_in_pyproject = sorted(req_set - py_set)

    if not missing_in_requirements and not missing_in_pyproject:
        print("dependency sync check: PASS")
        return 0

    print("dependency sync check: FAIL")
    if missing_in_requirements:
        print("- present in pyproject.toml but missing in requirements.txt:")
        for dep in missing_in_requirements:
            print(f"  - {dep}")
    if missing_in_pyproject:
        print("- present in requirements.txt but missing in pyproject.toml:")
        for dep in missing_in_pyproject:
            print(f"  - {dep}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
