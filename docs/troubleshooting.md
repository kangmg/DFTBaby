# Troubleshooting

## 1) Start From a Known-Stable Profile

```bash
pip install -r requirements-core.txt
pip install -e .
```

Or use pinned Colab/CI versions:

```bash
pip install -r requirements-colab.txt
pip install -e .
```

Install optional packs only when needed:

```bash
pip install ".[plot]"
pip install ".[metadynamics]"
pip install ".[advanced]"
```

## 2) f2py / Compiler Mismatch

Most extension build failures come from mismatched Python/NumPy/compiler paths.

Check:

```bash
python3 --version
python3 -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
python3 -m numpy.f2py -h >/dev/null
gfortran --version
```

Always compile with `python3 -m numpy.f2py` (already used by Makefiles). Avoid using a standalone `f2py` from another environment.

## 3) Build the Minimum Needed Extensions

Compile only the directory needed by your target feature:

- Core TD-DFTB speedup: `DFTB/extensions`
- Force-field/QM-MM: `DFTB/ForceField/src`
- Poisson workflows: `DFTB/Poisson/src`
- Multiple-scattering workflows: `DFTB/MultipleScattering/src`

In each directory use:

```bash
make clean && make
```

## 4) Common Runtime Configuration Pitfall

Old examples may use `scf_conv`; current key is `scf_conf` in `dftbaby.cfg`.

## 5) Quick Smoke Test

```bash
DFTB2.py --help
LR_TDDFTB.py --help
SurfaceHopping.py --help
initial_conditions.py --help
python3 -c "from DFTB.Dynamics.SurfaceHopping import main; print('ok')"
```

For periodic jobs, run a short NonSCC and SCC sanity run before launching production trajectories.

If instability remains, create a fresh virtual environment and reinstall one profile from scratch.
