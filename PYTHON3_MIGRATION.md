# Python 3 Modernization Status

## Scope

DFTBaby was migrated from legacy Python-2-era code to a Python 3 baseline focused on:

- stable molecular (non-periodic) workflows
- reproducible dependency profiles (core vs Colab/CI)
- selective native-extension builds (compile only required features)

## Current Runtime Targets

- Python: `>=3.10`
- Core NumPy/SciPy baseline: `numpy==1.26.4`, `scipy==1.11.4`
- Modern packaging: `pyproject.toml` + editable installs (`pip install -e .`)

## Completed Modernization

- Python-2 print redirection (`print >>`) removed from active code paths.
- Legacy constructs removed/updated:
  - `xrange`, `iteritems`, `itervalues`, `sys.maxint`, old exception syntax
- `optparse` compatibility paths updated for Python 3 output behavior.
- Blender helper scripts were rewritten into Python-3-safe modules:
  - parsing logic retained
  - obsolete Blender-2.49 rendering path is now an explicit compatibility shim
- Import fallbacks for pseudo-atom modules were tightened to avoid swallowing unrelated import errors.

## Verification Snapshot

The following checks pass in the current tree:

- `python3 -m compileall -q DFTB tests`
- `python3 tests/test_package_build.py`
- `python3 tests/test_syntax_validation.py`
- `python3 tests/test_python3_compatibility.py`
- `python3 tests/test_compilation.py`

Syntax validation currently reports:

- `295 / 295` Python files valid
- no deprecated Python-2 patterns in production code

## Known Functional Boundaries

- Primary hardening target is non-periodic molecular workflows.
- Periodic workflows have smoke-test coverage but should still be treated as a secondary path compared to non-periodic production use.
- Optional visualization stacks (legacy Blender/GUI style tools) are not a primary production target.

## Installation Profiles

```bash
# Minimal stable baseline
pip install -r requirements-core.txt
pip install -e .

# Reproducible Colab/CI baseline
pip install -r requirements-colab.txt
pip install -e .
```

## Documentation

- Main docs framework: MkDocs (`mkdocs.yml`, `docs/`)
- Legacy Sphinx/ReadTheDocs tree remains only as archival reference

