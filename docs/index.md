# DFTBaby Documentation

DFTBaby implements long-range corrected DFTB / TD-DFTB workflows for excited states and non-adiabatic molecular dynamics (surface hopping), following the original DFTBaby methodology.

This documentation is intentionally minimal:

- choose a stable install profile first
- enable only the features you need
- compile only the native extensions needed for your workflow

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

## Original Usage Is Preserved

Legacy CLI workflows from the old wiki are still supported and documented, including:

- `DFTB2.py`
- `LR_TDDFTB.py`
- `optimize.py` (legacy) and `GeometryOptimization.py` (recommended)
- `initial_conditions.py`
- `SurfaceHopping.py`

See `Run By Goal` for the updated short manual that keeps the original flow.

## References

- [DFTBaby paper (arXiv:1703.04049)](https://arxiv.org/abs/1703.04049)
- [Legacy DFTBaby wiki main page](https://www.dftbaby.chemie.uni-wuerzburg.de/DFTBaby/mdwiki.html#!WIKI/main_page.md)
