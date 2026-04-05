# Example Catalog

DFTBaby ships multiple example folders under `examples/`.  
This table maps each folder to purpose, command, and additional requirements.

| Folder | Goal | Typical Run Command | Extra Requirements |
|---|---|---|---|
| `examples/NAMD` | Non-adiabatic excited-state MD | `uv run dftbaby surface-hopping` | core profile |
| `examples/META` | Metadynamics free-energy surface | `uv run dftbaby surface-hopping` then `uv run dftbaby reconstruct.py` | `.[metadynamics]` |
| `examples/NEB` | Minimum-energy path (water flip) | `uv run dftbaby optimize-neb water_flip.xyz 0 --verbose=0` | core profile |
| `examples/RELAXED_SCAN` | Relaxed torsion scan | `uv run dftbaby geometry-opt phenylbenzene.xyz` | core profile |
| `examples/QMMM` | QM/MM crystal optimization | `uv run dftbaby optimize pyrene_crystal.xyz 0 --verbose=0` | ForceField extension build |
| `examples/CPKS` | CPKS charge gradients | `./charge_gradients.py water.xyz` | core profile |
| `examples/ORB_LOC` | Localized orbitals workflow | `uv run dftbaby dftb2 ethene_dimer.xyz --localize_orbitals=PM` | core profile |
| `examples/EXCITON` | Frenkel-exciton transition-charge workflow | visualization scripts + external QC steps | external tools (Gaussian/Multiwfn/Poisson/VMD) |
| `examples/SKA` | Multiple-scattering PAD workflows | `uv run dftbaby electroSka.py water.json` | `.[advanced]` + MultipleScattering build |
| `examples/CHELPG` | CHELPG charge fitting workflow | see folder README | external tools |

## Notes on Optional Modules

- If a command needs optional dependencies, the CLI now returns a targeted install hint.
- Build native extensions only for the feature you actually run.
- For most molecular excited-state workflows (`DFTB2`, `LR_TDDFTB`, `SurfaceHopping`), the core profile is sufficient.

