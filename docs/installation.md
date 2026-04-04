# Installation Profiles

Install only what your workflow needs.

## Recommended Baseline Versions

- Python `3.10` to `3.12`
- NumPy `1.26.4`
- SciPy `1.11.4`
- `gfortran` (only if building native extensions)

## 1) Core (Lightweight, Default)

```bash
pip install -r requirements-core.txt
pip install -e .
```

Use this for stable ground/excited-state workflows without extra features.

## 2) Reproducible (Colab/CI)

```bash
pip install -r requirements-colab.txt
pip install -e .
```

Use this when exact reproducibility matters.

## 3) Optional Feature Packs

```bash
pip install ".[plot]"         # plotting and spectra helpers
pip install ".[metadynamics]" # SurfaceHopping dyn_mode="M"
pip install ".[advanced]"     # advanced modules (mpmath)
pip install ".[gui]"          # legacy GUI stack (mayavi)
pip install ".[full]"         # all optional packs
```

## 4) Compile Only What You Need

You do not need to compile all Fortran/C extensions. Build only target features.

```bash
# Core TD-DFTB acceleration (recommended for dynamics performance)
cd DFTB/extensions && make clean && make

# Force-field / QM-MM workflows
cd DFTB/ForceField/src && make clean && make

# Poisson workflows
cd DFTB/Poisson/src && make clean && make

# Multiple-scattering workflows
cd DFTB/MultipleScattering/src && make clean && make
```

## 5) Toolchain Sanity Check

```bash
python3 --version
python3 -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
python3 -m numpy.f2py -h >/dev/null
gfortran --version
```

`python3 -m numpy.f2py` is important because it guarantees the compiler uses the same NumPy as your active Python environment.

## Docs Build

```bash
pip install ".[docs]"
mkdocs serve
```
