# DFTBaby

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NumPy 1.26+](https://img.shields.io/badge/numpy-1.26+-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Tight-binding DFT calculations for ground and excited states with non-adiabatic molecular dynamics**

DFTBaby is a software package for tight-binding DFT calculations on ground and excited states of molecules and for non-adiabatic molecular dynamics simulations.

📚 **[Documentation (Material for MkDocs)](https://kangmg.github.io/DFTBaby/)** | 📋 **[Migration Guide](PYTHON3_MIGRATION.md)**

---

## 🎯 Features

- **Electronic Parametrization**
  - Pseudo-orbitals from atomic DFT calculations using libxc non-hybrid functionals
  - Slater-Koster files generation for Hamiltonian, overlap, and dipoles

- **DFTB Calculations**
  - Long-range correction
  - Grimme's dispersion correction (experimental)
  - Repulsive potentials from Hotbit

- **TD-DFTB (Excited States)**
  - Excited states with/without long-range correction
  - Analytical excited state gradients

- **QM/MM**
  - TD-DFTB for QM, UFF/DREIDING for MM
  - Periodic boundary conditions for molecular crystals

- **Non-adiabatic Dynamics**
  - Surface hopping trajectories
  - Electronic coefficients in locally diabatic basis

- **Analysis Tools**
  - Cube files for MOs, transition densities, difference densities
  - External visualization via Molden/Cube outputs (recommended)

---

## 📦 Installation

### Requirements

- **Python**: 3.10 or newer
- **NumPy**: 1.26.4 or newer
- **SciPy**: 1.11.4 or newer
- **BLAS and LAPACK**
- **f2py** (included with NumPy)
- **setuptools** and **wheel** (for extension builds on Python 3.12+)
- **libxc** 3.0.0 (optional, for pseudoorbital calculations)

**Optional feature dependencies:**

- **Matplotlib** (`.[plot]`) for plotting/analysis scripts
- **Sympy + Matplotlib** (`.[metadynamics]`) for metadynamics mode
- **mpmath** (`.[advanced]`) for selected advanced integral/continuum modules

> **Note**: This project supports Python 3.10+ and NumPy 1.26+ (including NumPy 2.x).
> See [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md) for details.
> Packaging and entry points are managed in `pyproject.toml`.

### Recommended Versions (Colab/CI)

For the most reproducible setup (including Google Colab), install pinned dependencies:

```bash
pip install -r requirements-colab.txt
```

### Lightweight Core Setup

For stable non-plotting core workflows with fewer dependencies:

```bash
pip install -r requirements-core.txt
pip install -e .
```

Optional feature sets:

```bash
# Plotting/analysis scripts
pip install ".[plot]"

# Metadynamics features (dyn_mode="M")
pip install ".[metadynamics]"

# Advanced continuum/integral modules requiring mpmath
pip install ".[advanced]"

# Everything optional
pip install ".[full]"
```

### Quick Install

```bash
# Clone the repository
git clone https://github.com/kangmg/DFTBaby.git
cd DFTBaby

# Install with pip (recommended)
pip install .

# Or for development mode
pip install -e .
```

### uv Workflow

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements-core.txt
uv pip install -e .
```

Run with command-style CLI:

```bash
uv run dftbaby dftb2 molecule.xyz
uv run dftbaby lrtddftb molecule.xyz --nstates=5
```

### Compiling Fortran Extensions

Some features require compiled Fortran extensions:

```bash
# Core extensions
cd DFTB/extensions/
make clean && make
cd -

# Force field (for QM/MM)
cd DFTB/ForceField/src/
make clean && make
cd -

# Multiple scattering method
cd DFTB/MultipleScattering/src/
make clean && make
cd -
```

### Performance Optimization

For optimal performance, use NumPy/SciPy compiled with Intel MKL:

```bash
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

---

## 🚀 Quick Start

### Command-Line Programs

After installation, the following programs are available:

| Program | Description |
|---------|-------------|
| `DFTB2.py` | Ground state calculations, molecular orbitals |
| `LR_TDDFTB.py` | Ground and excited states, gradients |
| `GeometryOptimization.py` | Geometry optimization on ground/excited states |
| `SurfaceHopping.py` | Non-adiabatic molecular dynamics |

Modern aliases:

- `dftbaby dftb2 ...` / `dftbaby-dftb2 ...`
- `dftbaby lrtddftb ...` / `dftbaby-lrtddftb ...`
- `dftbaby surface-hopping ...` / `dftbaby-surface-hopping ...`

All programs support `--help` to show available options:

```bash
LR_TDDFTB.py --help
```

### Python Module

```python
from DFTB import XYZ, AtomicData
from DFTB.DFTB2 import DFTB2
from DFTB.LR_TDDFTB import LR_TDDFTB

# Your code here
```

### Example: TD-DFTB Calculation

```bash
# Compute excited states and save a spectrum
LR_TDDFTB.py molecule.xyz --nstates=5 --spectrum_file=molecule.spec
dftbaby lrtddftb molecule.xyz --nstates=5 --spectrum_file=molecule.spec
```

### Example: Non-adiabatic Dynamics

Create a folder with:
- `dynamics.in` - Initial geometry (bohr) and velocities (a.u.)
- `dftbaby.cfg` - Configuration file (see `DFTB/dftbaby.cfg` template)

Then run:
```bash
SurfaceHopping.py
```

Results are saved to `dynamics.xyz`, `energy_#.dat`, and `state.dat`.

📂 See `examples/NAMD/` for a complete example.

---

## 📊 Visualization

Recommended:

- export cube/molden data from DFTBaby
- inspect with external viewers (VMD, PyMOL, OVITO, Molden)

Legacy GUI mode (`--graphical=1`) is still available via optional `.[gui]` dependencies (Mayavi), but not recommended for minimal stable setups.

---

## ⚠️ Known Limitations

- **Minimal basis**: Valence orbitals only - Rydberg states not described
- **Monopole approximation**: May produce spurious low-lying dark states
- **Memory**: Large molecules may exceed memory during gradient calculations
- **Repulsive potentials**: Only H, C, N, O fully parametrized (dummy potentials exist for S, Ag, etc.)

---

## 🧪 Testing

```bash
# Run syntax validation
python3 tests/test_syntax_validation.py

# Run package build tests
python3 tests/test_package_build.py

# Run compilation tests
python3 tests/test_compilation.py
```

**Test Results:**
- ✅ 100% syntax validation pass on tracked Python files
- ✅ All critical patterns validated
- ✅ NumPy 1.26+/2.x compatibility for core workflows

---

## 📖 Documentation

- **Full Documentation**: [https://kangmg.github.io/DFTBaby/](https://kangmg.github.io/DFTBaby/)
- **Documentation Framework**: Material for MkDocs
- **Tutorials**: step-by-step workflows for excited states, NAMD, scans, NEB, and optional advanced modules
- **Build docs locally**:

```bash
pip install ".[docs]"
mkdocs serve
```

```bash
mkdocs build
```

- **Migration Guide**: [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md)
- **Examples**: See `examples/` directory

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Original Author**: Alexander Humeniuk
- **Python 3 Migration**: kangmg

---

## 🔗 Links

- **Repository**: https://github.com/kangmg/DFTBaby
- **Documentation**: https://kangmg.github.io/DFTBaby/

---

## 📝 Citation

If you use DFTBaby in your research, please cite:

```bibtex
@software{dftbaby,
  title = {DFTBaby: Tight-binding DFT for excited states and dynamics},
  author = {Humeniuk, Alexander},
  url = {http://dftbaby.chemie.uni-wuerzburg.de/},
  year = {2015}
}
```

---

## 🆕 What's New

### Version 0.1.0 (2025)
- ✅ **Python 3 compatibility improvements**
- ✅ **NumPy compatibility improvements**
- ✅ **Modern build system** (pyproject.toml)
- ✅ **Comprehensive tests** (300+ fixes validated)
- ✅ **Updated dependencies** (NumPy/SciPy modern baseline with optional packs)
- ✅ **30 command-line tools** as entry points
- ✅ **Automated documentation** deployment

See [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md) for complete migration details.
