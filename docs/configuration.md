# Configuration Guide

DFTBaby reads options from command line and/or `dftbaby.cfg` in the working directory.

## Resolution Order

- command-line flags override config-file values
- if no flag is provided, `dftbaby.cfg` values are used
- if neither is set, built-in defaults are used

To inspect full option sets:

```bash
dftbaby dftb2 --help
dftbaby lrtddftb --help
dftbaby surface-hopping --help
dftbaby geometry-opt --help
```

## Core Sections

### `[DFTBaby]`

Common keys:

- `scf_conf`: SCF convergence threshold
- `density_mixer`: set to `None` if you need strict legacy dynamics behavior
- `long_range_correction`: `0/1`
- `charge`: total molecular charge

### `[SurfaceHopping]`

Common keys:

- `nstep`: number of nuclear time steps
- `nuclear_step`: fs time step
- `dyn_mode`: `"E"` (constant energy), `"T"` (thermostatted), `"M"` (metadynamics)
- `initial_state`: integer state index or `"brightest"`
- `nstates`: number of excited states included in propagation
- `output_step`: write interval for trajectory files

### `[GeometryOptimization]`

Common keys:

- `state`: `0` ground state, `1` for `S1`, etc.
- `calc_hessian`: `0/1`
- `coord_system`: `cartesian` or `internal`
- `grad_tol`, `func_tol`, `max_steps`
- `method`: `CG`, `BFGS`, `Newton`, `Steepest Descent`

## Minimal Templates

### A) Excited-State Single Point + Spectrum

```ini
[DFTBaby]
charge = 0
scf_conf = 1e-14
long_range_correction = 1
```

Run:

```bash
dftbaby lrtddftb molecule.xyz --nstates=10 --spectrum_file=molecule.spec
```

### B) Surface Hopping Trajectory

```ini
[DFTBaby]
scf_conf = 1e-14
density_mixer = None
long_range_correction = 0

[SurfaceHopping]
charge = 0
initial_state = 1
nstates = 3
nstep = 5000
nuclear_step = 0.1
dyn_mode = "E"
output_step = 10
```

### C) Geometry Optimization

```ini
[DFTBaby]
scf_conf = 1e-14
long_range_correction = 0

[GeometryOptimization]
state = 0
calc_hessian = 0
coord_system = cartesian
grad_tol = 1.0e-5
func_tol = 1.0e-8
max_steps = 500
method = CG
```

## Legacy Key Compatibility

- Old examples may show `scf_conv`; current template uses `scf_conf`.
- Legacy script names remain valid (`DFTB2.py`, `LR_TDDFTB.py`, `SurfaceHopping.py`, ...).
- Command-style aliases are recommended for new workflows (`dftbaby ...`).

## Related Inputs

- `dynamics.in`: required by `SurfaceHopping` workflows
- `meta-config.py`: additionally required when `dyn_mode = "M"`
- force-field files (`*.ff`): required by QM/MM periodic-force-field workflows

