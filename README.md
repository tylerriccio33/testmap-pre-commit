# testmap-pre-commit

A [pre-commit](https://pre-commit.com) mirror for
[testmap](https://github.com/tylerriccio33/testmap), in the same style as
`ruff-pre-commit`. It turns `testmap report` into a coverage gate: if any feature
is missing a required test kind, the hook fails and blocks the commit.

## Usage

Add it to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/tylerriccio33/testmap-pre-commit
    rev: v0.1.0
    hooks:
      - id: testmap
```

The hook reads `[tool.testmap]` from your `pyproject.toml` (the kind taxonomy and
which kinds each feature requires) exactly as `testmap report` does on the CLI.

## How it works

This repo is never published to PyPI. pre-commit clones it at the pinned `rev`,
installs it, and the install pulls in the matching `testmap`; the hook then runs
`testmap report`, whose non-zero exit on a missing kind fails the commit.

Each release tag pins a specific `testmap` version, so a given `rev` always
installs the same tool.

## Staying in sync

`.github/workflows/sync.yml` runs daily (and on demand): it checks PyPI for the
latest `testmap`, rewrites the pin to `testmap==<version>`, and pushes a matching
`v<version>` tag — so the mirror tracks releases with no manual step. The current
`v0.1.0` is a bootstrap pinned to a testmap commit; once `testmap>=0.3.0` is on
PyPI the workflow takes over and cuts version-aligned tags.
