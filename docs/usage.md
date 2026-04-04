# Run By Goal

All options can be passed on the command line or through `dftbaby.cfg` in the working directory (legacy behavior preserved).

Primary supported path is non-periodic molecular dynamics/photochemistry. Periodic workflows are available but currently a secondary path.

## Main Programs (Legacy Compatible)

- `DFTB2.py`: ground-state SCC-DFTB
- `LR_TDDFTB.py`: excited states, spectra, gradients
- `GeometryOptimization.py`: recommended geometry optimization interface
- `optimize.py`: legacy optimization interface kept for compatibility
- `initial_conditions.py`: Wigner initial-condition sampling from Hessian
- `SurfaceHopping.py`: non-adiabatic molecular dynamics

Modern command-style aliases are also available:

- `dftbaby dftb2 ...` (or `dftbaby-dftb2 ...`)
- `dftbaby lrtddftb ...` (or `dftbaby-lrtddftb ...`)
- `dftbaby surface-hopping ...` (or `dftbaby-surface-hopping ...`)

## 1) Ground-State Single Point (Original Style)

```bash
DFTB2.py benzene.xyz
dftbaby dftb2 benzene.xyz
```

Export Molden orbitals:

```bash
DFTB2.py benzene.xyz --molden_file=benzene.molden --verbose=0
```

## 2) Excited States and Spectrum

```bash
LR_TDDFTB.py benzene.xyz --nstates=6 --diag_conv=1.0e-8
LR_TDDFTB.py benzene.xyz --nstates=6 --spectrum_file=benzene.spec
dftbaby lrtddftb benzene.xyz --nstates=6 --spectrum_file=benzene.spec
```

Legacy graphical mode:

```bash
LR_TDDFTB.py benzene.xyz --nstates=6 --graphical=1
```

For plotting install `.[plot]`. For robust workflows, prefer external viewers from exported cube/molden files.

## 3) Geometry Optimization (Updated + Legacy)

Recommended interface:

```bash
GeometryOptimization.py molecule.xyz --state=0
GeometryOptimization.py molecule.xyz --state=1 --calc_hessian=1
dftbaby geometry-opt molecule.xyz --state=1
```

Legacy equivalent:

```bash
optimize.py molecule.xyz 0 H
optimize.py molecule.xyz 1
```

## 4) Non-Adiabatic Dynamics (Legacy Fluorene Flow, Updated)

1. Optimize S0 and inspect vertical excitations.

```bash
optimize.py F1_C2v.xyz 0 --verbose=0
LR_TDDFTB.py F1_S0.xyz --nstates=6 --spectrum_file=F1_S0.spec --verbose=1
```

2. Compute Hessian and sample Wigner initial conditions.

```bash
optimize.py F1_S0.xyz 0 H
initial_conditions.py F1_S0.xyz hessian.dat --Nsample=10 --outdir=.
```

3. For each trajectory folder (`TRAJ_0`, `TRAJ_1`, ...), place:

- `dynamics.in` (positions and velocities)
- `dftbaby.cfg` with `[DFTBaby]` and `[SurfaceHopping]`

4. Run dynamics.

```bash
cd TRAJ_0
SurfaceHopping.py
dftbaby surface-hopping
```

5. Aggregate populations after running many trajectories.

```bash
populations.py TRAJ_*/state.dat
```

Typical trajectory outputs include `dynamics.xyz`, `state.dat`, `energy_*.dat`, `coeff_*.dat`, and non-adiabatic coupling tables.

### External Visualization (Recommended)

- `--molden_file=...` for MO and charge inspection in molden-capable tools.
- cube exports for orbitals/densities can be viewed with tools like VMD, PyMOL, or OVITO.
- `--graphical=1` is legacy and requires optional `.[gui]` dependencies.

## 5) Periodic Calculations (Secondary Path)

Periodic SCC/NonSCC execution paths are smoke-tested, but the main hardening target remains molecular systems. If you need periodic runs:

- start from `requirements-core.txt`
- run short sanity jobs first (small cells, low state count)
- add optional modules only when your workflow needs them

## Minimal `dftbaby.cfg` (Current Keys)

```ini
[DFTBaby]
scf_conf = 1e-14
long_range_correction = 0

[SurfaceHopping]
charge = 0
initial_state = 0
nstates = 2
nstep = 1000
nuclear_step = 0.1
dyn_mode = "E"
```

## Important Changes vs Old Wiki

- Install flow changed from `setup.py install` to `pip install -e .` plus profile requirements.
- Build strategy changed from "compile everything" to "compile only feature-relevant extensions".
- The old `scf_conv` spelling in examples is now `scf_conf` in current config/templates.

## Method Limitations to Keep in Mind

- The minimal valence basis and monopole approximation can miss Rydberg physics and may produce spurious low-lying dark states in some systems.
- S0/S1 conical intersection topology is not fully reliable at the TD-DFTB(B) level.
- Workflow is centered on closed-shell singlet excited-state dynamics.
