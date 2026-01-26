===========
Usage Guide
===========

This guide provides comprehensive instructions for using DFTBaby for various computational chemistry tasks.

.. contents:: Table of Contents
   :local:
   :depth: 2

Getting Started
===============

Basic Workflow
--------------

A typical DFTBaby calculation workflow consists of:

1. **Prepare geometry**: Create an XYZ file with your molecular structure
2. **Configure parameters**: Set up ``dftbaby.cfg`` for calculation options
3. **Run calculation**: Execute the appropriate program
4. **Analyze results**: Visualize and interpret output files

Molecular Structure Format
---------------------------

DFTBaby uses standard XYZ format for molecular geometries::

    3
    Water molecule
    O   0.0000   0.0000   0.1173
    H   0.0000   0.7572  -0.4692
    H   0.0000  -0.7572  -0.4692

Coordinates can be in Angstroms (default) or Bohr (specify with ``units="bohr"`` in keywords).

Command-Line Programs
=====================

DFTBaby provides 30+ command-line programs. Here are the most important ones:

Ground State Calculations
--------------------------

DFTB2.py
~~~~~~~~

Performs ground state DFTB calculations and computes molecular orbitals::

    DFTB2.py molecule.xyz

**Key options:**

- ``--charge=N``: Set total charge (default: 0)
- ``--multiplicity=N``: Set spin multiplicity (default: 1)
- ``--nstates=N``: Number of excited states for configuration interaction
- ``--save_orbitals=file.npz``: Save molecular orbitals

**Example - Charged system**::

    DFTB2.py cation.xyz --charge=+1 --multiplicity=2

**Output files:**

- Ground state energy
- Molecular orbital energies
- Mulliken charges
- Dipole moment

Excited State Calculations
---------------------------

LR_TDDFTB.py
~~~~~~~~~~~~

Linear-response TD-DFTB for excited states and their gradients::

    LR_TDDFTB.py molecule.xyz --nstates=10

**Key options:**

- ``--nstates=N``: Number of excited states (default: 5)
- ``--lr_correction=1``: Enable long-range correction
- ``--graphical=1``: Interactive visualization with Mayavi
- ``--gradient_state=N``: Compute gradient for state N
- ``--save_charges=file.dat``: Save transition charges

**Example - Absorption spectrum**::

    LR_TDDFTB.py molecule.xyz --nstates=20 --lr_correction=1

**Output:**

- Excitation energies (eV)
- Oscillator strengths
- Transition dipole moments
- Configuration analysis

**Visualization**::

    LR_TDDFTB.py molecule.xyz --nstates=10 --graphical=1

This opens an interactive 3D viewer showing:

- Molecular orbitals
- Transition densities
- Difference densities
- HOMO/LUMO orbitals

Geometry Optimization
---------------------

GeometryOptimization.py
~~~~~~~~~~~~~~~~~~~~~~~

Optimize molecular geometry on ground or excited states::

    # Ground state optimization
    GeometryOptimization.py molecule.xyz

    # Excited state optimization (S1)
    GeometryOptimization.py molecule.xyz --state=1

**Key options:**

- ``--state=N``: Optimize excited state N (0=ground, 1=S1, 2=S2, ...)
- ``--constraints=file.txt``: Apply geometric constraints
- ``--max_iter=N``: Maximum optimization steps
- ``--conv_threshold=X``: Convergence threshold (default: 1e-3)

**Example - Constrained optimization**::

    # Create constraints file
    echo "bond 0 1 1.5" > constraints.txt
    GeometryOptimization.py molecule.xyz --constraints=constraints.txt

**Constraint types:**

- ``bond i j R``: Fix distance between atoms i and j to R Å
- ``angle i j k A``: Fix angle i-j-k to A degrees
- ``dihedral i j k l D``: Fix dihedral angle to D degrees

Non-adiabatic Molecular Dynamics
---------------------------------

SurfaceHopping.py
~~~~~~~~~~~~~~~~~

Trajectory surface hopping for non-adiabatic dynamics::

    SurfaceHopping.py

**Requirements:**

1. **dynamics.in** - Initial geometry (Bohr) and velocities (a.u.).
   Format: atomic positions first, then velocities::

       3
       o   0.0000   0.0000   0.2217
       h   0.0000   1.4315  -0.8868
       h   0.0000  -1.4315  -0.8868
       0.0001  -0.0002   0.0000
       0.0000   0.0010  -0.0005
       0.0000  -0.0010  -0.0005

2. **dftbaby.cfg** - Configuration file (see Configuration section)

**Output files:**

- ``dynamics.xyz``: Trajectory of nuclear positions
- ``energy_0.dat, energy_1.dat, ...``: Energies of electronic states vs. time
- ``state.dat``: Active electronic state vs. time
- ``coeff_0.dat, coeff_1.dat, ...``: Quantum populations for each state

**Example workflow**::

    # 1. Prepare initial conditions (Wigner distribution)
    python3 -c "from DFTB.Dynamics import prepare_initial_conditions; \
                prepare_initial_conditions.wigner_sampling('molecule.xyz', \
                'dynamics.in', nsamples=1)"

    # 2. Run surface hopping
    SurfaceHopping.py

    # 3. Analyze trajectory
    python3 -c "from DFTB.Analyse import analyze_trajectory; \
                analyze_trajectory.plot_energies('energy_*.dat')"

QM/MM Calculations
------------------

For large systems, combine TD-DFTB (QM) with force fields (MM)::

    # Requires: dftbaby.cfg with QM/MM settings
    LR_TDDFTB.py crystal.xyz --qmmm=1

**Configuration in dftbaby.cfg**::

    [QMMM]
    qm_atoms = 0-50          # Atom indices for QM region
    mm_forcefield = UFF      # Force field (UFF or DREIDING)
    periodic_box = 50.0 50.0 50.0  # Box dimensions (Å)

See ``examples/QMMM/`` for complete examples.

Python API
==========

For more control, use DFTBaby as a Python library.

Basic Example - Ground State
-----------------------------

::

    from DFTB import XYZ
    from DFTB.DFTB2 import DFTB2

    # Load molecular geometry
    atomlist = XYZ.read_xyz("molecule.xyz")[0]

    # Create DFTB calculator
    calc = DFTB2(atomlist)

    # Run calculation
    calc.getEnergy()

    # Access results
    print(f"Total energy: {calc.dftb_energy} Hartree")
    print(f"HOMO energy: {calc.orbital_energies[calc.Nelec//2-1]} Hartree")
    print(f"LUMO energy: {calc.orbital_energies[calc.Nelec//2]} Hartree")

Excited State Calculations
---------------------------

::

    from DFTB.LR_TDDFTB import LR_TDDFTB

    # Initialize TD-DFTB
    tddftb = LR_TDDFTB(atomlist)

    # Set number of excited states
    tddftb.setNstates(10)

    # Enable long-range correction
    tddftb.setLongRangeCorrection(True)

    # Run calculation
    tddftb.getEnergies()

    # Access results
    for i, (energy, osc_strength) in enumerate(
        zip(tddftb.excitation_energies, tddftb.oscillator_strengths)):
        print(f"S{i+1}: {energy:.3f} eV, f={osc_strength:.4f}")

Geometry Optimization
---------------------

::

    from DFTB.Optimize import optimize_geometry

    # Optimize ground state
    optimized_geometry = optimize_geometry(
        atomlist,
        state=0,           # 0=ground, 1=S1, etc.
        max_iter=100,
        conv_threshold=1e-3
    )

    # Save optimized structure
    XYZ.write_xyz("optimized.xyz", [optimized_geometry])

Force Calculations
------------------

::

    # Get forces on all atoms
    forces = calc.getForces()

    # Forces is a list of (Z, force_vector) tuples
    for i, (Z, force) in enumerate(forces):
        fx, fy, fz = force
        print(f"Atom {i}: Force = ({fx:.6f}, {fy:.6f}, {fz:.6f}) Ha/Bohr")

Molecular Orbitals Analysis
----------------------------

::

    # Get orbital coefficients
    orbitals = calc.orbitals

    # Get orbital energies
    energies = calc.orbital_energies

    # Find HOMO and LUMO
    homo_idx = calc.Nelec // 2 - 1
    lumo_idx = calc.Nelec // 2

    print(f"HOMO energy: {energies[homo_idx]:.4f} Ha")
    print(f"LUMO energy: {energies[lumo_idx]:.4f} Ha")
    print(f"HOMO-LUMO gap: {(energies[lumo_idx]-energies[homo_idx])*27.211:.2f} eV")

Configuration File
==================

The ``dftbaby.cfg`` file controls calculation parameters.

Basic Template
--------------

::

    # DFTB Parameters
    [DFTB]
    charge = 0                  # Total charge
    multiplicity = 1            # Spin multiplicity
    long_range_correction = 1   # Enable LC-DFTB
    gamma_approximation = 0     # Use full gamma matrix

    # TD-DFTB Parameters
    [TD-DFTB]
    nstates = 10                # Number of excited states
    iter_conv = 1e-6            # Convergence threshold
    singlet_triplet = singlet   # singlet or triplet

    # Dynamics Parameters
    [DYNAMICS]
    nstep = 10000               # Number of MD steps
    tstep = 0.1                 # Time step (fs)
    temperature = 300.0         # Temperature (K)

    # QM/MM Parameters (optional)
    [QMMM]
    qm_atoms = 0-50
    mm_forcefield = UFF
    periodic_box = 50.0 50.0 50.0

See ``examples/*/dftbaby.cfg`` for complete examples.

Advanced Features
=================

Cube File Generation
--------------------

Generate cube files for visualization in VMD, Avogadro, etc.::

    from DFTB.Analyse import Cube

    # Generate HOMO cube file
    Cube.write_orbital_cube("homo.cube", calc, orbital_index=homo_idx)

    # Generate transition density cube
    Cube.write_transition_density("transition_S1.cube", tddftb, state=1)

Wigner Sampling
---------------

Generate initial conditions from Wigner distribution::

    from DFTB.Dynamics import WignerSampling

    # Sample 100 initial conditions
    sampler = WignerSampling("molecule.xyz")
    sampler.sample(nsamples=100, temperature=300.0)
    sampler.write("initial_conditions_*.in")

Metadynamics
------------

Explore free energy surfaces with metadynamics::

    # See examples/META/ for complete setup
    python3 DFTB/MetaDynamics/meta.py

Natural Transition Orbitals
----------------------------

Analyze excited states using NTOs::

    # Compute NTOs for state 1 (S1)
    ntos = tddftb.compute_NTOs(state=1)

    # Get participation ratio
    participation = tddftb.nto_participation_ratio(state=1)
    print(f"NTO participation ratio: {participation:.2f}")

Examples by Application
=======================

Absorption Spectrum
-------------------

::

    # 1. Optimize ground state geometry
    GeometryOptimization.py molecule.xyz

    # 2. Calculate excited states
    LR_TDDFTB.py optimized.xyz --nstates=50 --lr_correction=1

    # 3. Plot spectrum
    python3 -c "from DFTB.Analyse import spectrum; \
                spectrum.plot_absorption('lr_tddftb_output.dat')"

Emission Spectrum
-----------------

::

    # 1. Optimize excited state (S1)
    GeometryOptimization.py molecule.xyz --state=1

    # 2. Calculate vertical emission
    LR_TDDFTB.py s1_optimized.xyz --nstates=10

    # Emission energy is E(S1) at S1 geometry

Photodynamics Simulation
-------------------------

::

    # 1. Optimize ground state
    GeometryOptimization.py molecule.xyz

    # 2. Prepare initial conditions at S1
    python3 -c "from DFTB.Dynamics import prepare_initial; \
                prepare_initial.excited_state_sampling('optimized.xyz', \
                state=1, nsamples=50)"

    # 3. Run trajectories
    for i in {1..50}; do
        mkdir traj_$i
        cd traj_$i
        cp ../dynamics_$i.in dynamics.in
        cp ../dftbaby.cfg .
        SurfaceHopping.py
        cd ..
    done

    # 4. Analyze ensemble
    python3 -c "from DFTB.Analyse import ensemble_analysis; \
                ensemble_analysis.plot_populations('traj_*/state.dat')"

Crystal Calculations
--------------------

For periodic systems or molecular crystals::

    # Use QM/MM with periodic boundary conditions
    LR_TDDFTB.py crystal.xyz --qmmm=1

    # In dftbaby.cfg:
    # [QMMM]
    # periodic_box = 30.0 30.0 30.0
    # qm_atoms = 0-100

See ``examples/QMMM/`` for molecular crystal example.

Troubleshooting
===============

Common Issues
-------------

**SCF Not Converging**

- Try different initial guess
- Reduce mixing parameter
- Enable level shifting
- Check geometry for unreasonable bond lengths

**Memory Errors**

- Reduce basis set size (use minimal basis)
- Reduce number of excited states
- Use disk-based storage for large matrices
- Split calculation into smaller fragments

**Forces Not Available**

- Ensure analytical gradients are implemented for your method
- Check that gradient calculation is enabled
- Verify excited state gradients are supported

**Trajectory Instabilities**

- Reduce time step (try 0.1 fs → 0.05 fs)
- Increase number of substeps for electronic propagation
- Check energy conservation
- Verify initial conditions are reasonable

Performance Tips
----------------

1. **Use optimized BLAS/LAPACK**: Link with Intel MKL for best performance
2. **Set thread count**::

       export OMP_NUM_THREADS=4
       export MKL_NUM_THREADS=4

3. **Pre-compute parameters**: Generate Slater-Koster files once, reuse
4. **Use appropriate basis**: Minimal basis is sufficient for most TD-DFTB
5. **Disk caching**: Enable for large molecules to reduce memory

Getting Help
============

- **Documentation**: https://kangmg.github.io/DFTBaby/
- **Issues**: https://github.com/kangmg/DFTBaby/issues
- **Examples**: See ``examples/`` directory in repository

References
==========

If you use DFTBaby, please cite:

- Original DFTBaby: Humeniuk, A. (2015)
- Python 3.12+ migration: This repository

See ``README.md`` for complete citation information.
