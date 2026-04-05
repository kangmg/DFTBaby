# Tutorials

This page provides step-by-step workflows you can run directly in this repository.

## Before You Start

Use one environment profile first:

```bash
pip install -r requirements-core.txt
pip install -e .
```

or with `uv`:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements-core.txt
uv pip install -e .
```

All examples below also work with legacy script names (for example `LR_TDDFTB.py ...`) if preferred.

## 1) Ground + Excited States (Single Molecule)

Goal: run a standard TD-DFTB excitation calculation and write a spectrum file.

```bash
uv run dftbaby lrtddftb benzene.xyz --nstates=10 --spectrum_file=benzene.spec
```

Useful outputs:

- console table with excitation energies and oscillator strengths
- `benzene.spec` for plotting/analysis

Optional visualization exports:

```bash
uv run dftbaby dftb2 benzene.xyz --molden_file=benzene.molden
```

## 2) Excited-State MD (Surface Hopping)

Goal: run non-adiabatic dynamics using the shipped fluorene example.

```bash
cd examples/NAMD
uv run dftbaby surface-hopping
```

Key outputs:

- `dynamics.xyz`: nuclear trajectory
- `energy_*.dat`: adiabatic state energies vs time
- `state.dat`: active electronic state history
- `coeff_*.dat`: electronic populations

## 3) Excited-State Geometry Optimization and Emission Workflow

Goal: optimize `S0`, then optimize `S1`, then estimate vertical emission.

```bash
# S0 optimization
uv run dftbaby geometry-opt molecule.xyz --state=0

# S1 optimization
uv run dftbaby geometry-opt optimized.xyz --state=1

# Excitations at S1 geometry
uv run dftbaby lrtddftb optimized.xyz --nstates=6
```

This follows the classic ground/excited minimum workflow from the legacy docs.

## 4) Relaxed Scan (Internal Rotation Example)

```bash
cd examples/RELAXED_SCAN
uv run dftbaby geometry-opt phenylbenzene.xyz
```

Expected outputs:

- `phenylbenzene_scan.dat`
- `phenylbenzene_scan.xyz`

## 5) Nudged Elastic Band (NEB)

```bash
cd examples/NEB
uv run dftbaby optimize-neb water_flip.xyz 0 --verbose=0
```

Expected outputs:

- `neb_NAME_##.xyz` (image geometries)
- `path_energies_NAME_##.dat` (energy profile)

## 6) Optional Advanced Tutorials

### 6a) Metadynamics

Requires:

- `pip install ".[metadynamics]"`
- `examples/META/{dynamics.in,dftbaby.cfg,meta-config.py}`

Run:

```bash
cd examples/META
uv run dftbaby surface-hopping
uv run dftbaby reconstruct.py
```

### 6b) QM/MM Crystal Optimization

Requires force-field extension build for best stability/performance.

```bash
cd DFTB/ForceField/src && make clean && make
cd ../../../examples/QMMM
uv run dftbaby optimize pyrene_crystal.xyz 0 --verbose=0
```

### 6c) Multiple-Scattering / PAD (`electroSka`)

Requires advanced extras and multiple-scattering extension build.

```bash
pip install ".[advanced]"
cd DFTB/MultipleScattering/src && make clean && make
cd ../../../examples/SKA
uv run dftbaby electroSka.py water.json
```

