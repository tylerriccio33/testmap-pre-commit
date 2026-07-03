"""Sync this mirror's testmap pin to the latest release on PyPI (ruff-mirror style).

Run by .github/workflows/sync.yml. Rewrites pyproject.toml to `testmap==<latest>`
and prints that version to stdout so the workflow can tag the mirror `v<latest>`.
Prints nothing to stdout (so the workflow no-ops) when the latest release is below
the floor where testmap gained the coverage-gate exit code.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

# testmap < 0.3.0 always exits 0, so a hook built on it can't gate. Never pin
# below this; the mirror only exists to enforce coverage.
FLOOR = (0, 3, 0)
PYPROJECT = Path(__file__).parent / "pyproject.toml"


def _parse(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split(".")[:3])


def main() -> None:
    with urllib.request.urlopen("https://pypi.org/pypi/testmap/json") as response:
        latest = json.load(response)["info"]["version"]

    if _parse(latest) < FLOOR:
        print(f"latest testmap {latest} is below the {'.'.join(map(str, FLOOR))} floor", file=sys.stderr)
        return

    text = PYPROJECT.read_text(encoding="utf-8")
    # Replace whatever the single `testmap ...` requirement is (git pin or ==).
    pinned = re.sub(r'"testmap[^"]*"', f'"testmap=={latest}"', text)
    if pinned != text:
        PYPROJECT.write_text(pinned, encoding="utf-8")
    print(latest)  # the version the workflow should tag as v<latest>


if __name__ == "__main__":
    main()
