# DFTBaby Documentation

DFTBaby implements long-range corrected DFTB / TD-DFTB workflows for excited states and non-adiabatic molecular dynamics (surface hopping), following the original DFTBaby methodology.

This documentation is organized for practical use:

- install only what your workflow needs
- follow step-by-step tutorials for common tasks
- use the example catalog for advanced/legacy workflows
- runtime/build configuration is managed via `pyproject.toml`

## Scope

- Stable production path: non-periodic molecular workflows.
- Periodic workflows are available but considered secondary/experimental compared to the molecular path.

## Quick Start (Stable Baseline)

```bash
git clone https://github.com/kangmg/DFTBaby.git
cd DFTBaby
pip install -r requirements-core.txt
pip install -e .
```

For reproducible Colab/CI runs:

```bash
pip install -r requirements-colab.txt
pip install -e .
```

## What To Read First

1. `Installation Profiles` for environment setup (`pip` or `uv`)
2. `Tutorials` for end-to-end runs (excited states, NAMD, scans, NEB)
3. `Run By Goal` for command quick-reference
4. `Configuration Guide` for `dftbaby.cfg` templates and key options
5. `Example Catalog` for all shipped example folders

## Original Usage Is Still Preserved

Legacy CLI workflows from the old wiki remain available, including:

- `DFTB2.py`
- `LR_TDDFTB.py`
- `optimize.py` (legacy) and `GeometryOptimization.py` (recommended)
- `initial_conditions.py`
- `SurfaceHopping.py`

Command-style aliases are documented in tutorials and usage pages:

- `dftbaby dftb2 ...`
- `dftbaby lrtddftb ...`
- `dftbaby surface-hopping ...`

## References

- [DFTBaby paper (arXiv:1703.04049)](https://arxiv.org/abs/1703.04049)
- [Legacy DFTBaby wiki main page](https://www.dftbaby.chemie.uni-wuerzburg.de/DFTBaby/mdwiki.html#!WIKI/main_page.md)
