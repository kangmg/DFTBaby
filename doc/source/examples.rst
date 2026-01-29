==================
Practical Examples
==================

This page provides ready-to-use examples with configuration files and commands.

.. contents:: Table of Contents
   :local:
   :depth: 2

Configuration File Format
=========================

DFTBaby uses **INI format** for configuration files (``dftbaby.cfg``):

- Sections: ``[SectionName]``
- Settings: ``key = value``
- Comments: ``# comment text``
- Boolean: ``0`` (False) or ``1`` (True)

Example 1: Basic Excited State Calculation
===========================================

**Goal**: Calculate the first 10 excited states of a molecule with absorption spectrum.

File Structure
--------------

::

    my_calculation/
    ├── molecule.xyz
    └── dftbaby.cfg

molecule.xyz
------------

::

    10
    Naphthalene
    C   0.000000   0.000000   0.000000
    C   1.397000   0.000000   0.000000
    C   2.093000   1.207000   0.000000
    C   1.397000   2.414000   0.000000
    C   0.000000   2.414000   0.000000
    C  -0.696000   1.207000   0.000000
    H  -0.544000  -0.940000   0.000000
    H   1.941000  -0.940000   0.000000
    H  -0.544000   3.354000   0.000000
    H   1.941000   3.354000   0.000000

dftbaby.cfg
-----------

::

    [DFTBaby]
    # Ground state settings
    charge = 0
    multiplicity = 1
    scf_conv = 1e-8

    # Long-range correction for better CT states
    long_range_correction = 1

    # Number of excited states
    nstates = 10

    # Convergence for TD-DFTB
    iter_conv = 1e-6

Run Command
-----------

::

    LR_TDDFTB.py molecule.xyz

Expected Output
---------------

::

    Excited State Energies:
    S1:  3.245 eV   f=0.0234   (HOMO->LUMO)
    S2:  3.876 eV   f=0.1567   (HOMO->LUMO+1)
    S3:  4.123 eV   f=0.0012   (HOMO-1->LUMO)
    ...

Visualization
-------------

Add ``--graphical=1`` for interactive 3D visualization::

    LR_TDDFTB.py molecule.xyz --graphical=1

Example 2: Absorption Spectrum Calculation
===========================================

**Goal**: Calculate absorption spectrum with many states and long-range correction.

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    multiplicity = 1
    scf_conv = 1e-10

    # Essential for accurate spectrum
    long_range_correction = 1

    # Calculate many states for broad spectrum
    nstates = 50

    # Tight convergence for accurate energies
    iter_conv = 1e-8

    # Active space (optional, for large molecules)
    # nr_active_occ = 50
    # nr_active_virt = 50

Run Command
-----------

::

    LR_TDDFTB.py molecule.xyz > spectrum_output.txt

Post-processing
---------------

Extract data and plot::

    grep "eV" spectrum_output.txt > energies.dat

    # Plot with Python
    python3 << 'EOF'
    import matplotlib.pyplot as plt
    import numpy as np

    # Read energies and oscillator strengths
    data = np.loadtxt('energies.dat', usecols=(1,3))
    energies = data[:,0]
    osc_strengths = data[:,1]

    # Create spectrum with Gaussian broadening
    x = np.linspace(2.0, 8.0, 1000)
    y = np.zeros_like(x)
    sigma = 0.2  # eV

    for E, f in zip(energies, osc_strengths):
        y += f * np.exp(-(x-E)**2/(2*sigma**2))

    plt.plot(x, y)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Absorption (arb. units)')
    plt.title('Absorption Spectrum')
    plt.savefig('spectrum.png', dpi=300)
    plt.show()
    EOF

Example 3: Ground State Geometry Optimization
==============================================

**Goal**: Optimize molecular geometry to the nearest local minimum.

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-10

    [GeometryOptimization]
    # Optimize ground state
    state = 0

    # Coordinate system: 'cartesian' or 'internal'
    coord_system = cartesian

    # Convergence criteria
    grad_tol = 1.0e-5
    func_tol = 1.0e-8

    # Maximum steps
    max_steps = 500

    # Optimization method: 'BFGS', 'CG', 'Newton', 'Steepest Descent'
    method = BFGS

    # Calculate vibrational frequencies after optimization
    calc_hessian = 1

Run Command
-----------

::

    GeometryOptimization.py molecule.xyz

Output Files
------------

- ``optimized.xyz``: Optimized geometry
- ``optimization.xyz``: Full optimization trajectory
- ``hessian.dat``: Hessian matrix (if calc_hessian=1)
- ``vib.molden``: Vibrational modes (view with Molden)

Example 4: Excited State Geometry Optimization
===============================================

**Goal**: Find the optimized geometry of the first excited state (S1).

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-10
    long_range_correction = 1
    nstates = 5

    [GeometryOptimization]
    # Optimize S1 (first excited state)
    state = 1

    coord_system = cartesian
    grad_tol = 1.0e-4
    func_tol = 1.0e-7
    max_steps = 300
    method = BFGS

    # Don't calculate Hessian for excited states (expensive)
    calc_hessian = 0

Run Command
-----------

::

    GeometryOptimization.py molecule.xyz

Use Case: Emission Spectrum
----------------------------

1. Optimize ground state (S0)::

       # Set state=0 in dftbaby.cfg
       GeometryOptimization.py molecule.xyz
       cp optimized.xyz s0_geometry.xyz

2. Optimize excited state (S1)::

       # Set state=1 in dftbaby.cfg
       GeometryOptimization.py s0_geometry.xyz
       cp optimized.xyz s1_geometry.xyz

3. Calculate vertical emission::

       LR_TDDFTB.py s1_geometry.xyz

4. The emission energy is S1→S0 at S1 geometry.

Example 5: Surface Hopping Dynamics
====================================

**Goal**: Simulate non-adiabatic dynamics with trajectory surface hopping.

File Structure
--------------

::

    dynamics/
    ├── molecule.xyz
    ├── dftbaby.cfg
    └── dynamics.in

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-10
    long_range_correction = 1

    # IMPORTANT: Disable DIIS for dynamics
    density_mixer = None

    [SurfaceHopping]
    # Start in S1 (first excited state)
    initial_state = 1

    # Calculate 3 excited states
    nstates = 3

    # Simulation time
    nstep = 5000
    nuclear_step = 0.1     # 0.1 fs time step

    # Run at constant energy (NVE)
    dyn_mode = "E"

    # Force hop to ground state at conical intersection
    switch_to_groundstate = 1

    # Decoherence correction (recommended)
    decoherence_correction = 1

    # Scalar coupling threshold
    scalar_coupling_threshold = 0.01

    # Output settings
    output_step = 10       # Save every 10th step

    # Time series (optional)
    time_series = ['particle-hole charges current', 'Lambda2 current']

dynamics.in
-----------

Initial conditions with positions (Bohr) and velocities (a.u.).

**Format**: First the number of atoms and comment line, then atomic positions,
followed by velocities in the same order::

    10
    c   0.0000   0.0000   0.0000
    c   2.6400   0.0000   0.0000
    c   3.9500   2.2800   0.0000
    c   2.6400   4.5600   0.0000
    c   0.0000   4.5600   0.0000
    c  -1.3100   2.2800   0.0000
    h  -1.0300  -1.7700   0.0000
    h   3.6700  -1.7700   0.0000
    h  -1.0300   6.3400   0.0000
    h   3.6700   6.3400   0.0000
    0.0001  -0.0002   0.0003
   -0.0001   0.0004  -0.0001
    0.0002  -0.0001   0.0002
   -0.0003   0.0001  -0.0001
    0.0001   0.0003   0.0002
   -0.0002  -0.0002   0.0001
    0.0005   0.0001  -0.0003
   -0.0004   0.0002   0.0004
    0.0003  -0.0004   0.0001
   -0.0001   0.0003  -0.0002

Run Command
-----------

::

    cd dynamics/
    SurfaceHopping.py

Output Files
------------

- ``dynamics.xyz``: Nuclear trajectory
- ``energy_0.dat, energy_1.dat, ...``: Energy of each electronic state vs. time
- ``state.dat``: Active state vs. time (for hopping analysis)
- ``coeff_0.dat, coeff_1.dat, ...``: Quantum populations for each state
- ``particle_hole_charges.xyz``: Charge distribution (if requested)

Analysis
--------

Plot state populations::

    python3 << 'EOF'
    import matplotlib.pyplot as plt
    import numpy as np

    # Read active state vs. time
    data = np.loadtxt('state.dat')
    time_fs = data[:, 0]
    state = data[:, 1]

    plt.figure(figsize=(10,6))
    plt.plot(time_fs, state, linewidth=0.5)
    plt.xlabel('Time (fs)')
    plt.ylabel('Electronic State')
    plt.title('Surface Hopping Trajectory')
    plt.yticks([0,1,2,3], ['S0', 'S1', 'S2', 'S3'])
    plt.grid(True, alpha=0.3)
    plt.savefig('hopping.png', dpi=300)
    plt.show()
    EOF

Example 6: Ground State Equilibration
======================================

**Goal**: Equilibrate geometry at finite temperature before excited state dynamics.

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-8

    [SurfaceHopping]
    # Stay on ground state
    initial_state = 0
    nstates = 0           # Don't calculate excited states

    # Equilibration time
    nstep = 10000
    nuclear_step = 0.5    # Larger step for faster equilibration

    # Constant temperature (Berendsen thermostat)
    dyn_mode = "T"
    temp = 300.0
    timecoupling = 1.0

    output_step = 50

Run Command
-----------

::

    SurfaceHopping.py

Then extract equilibrated geometry::

    tail -11 dynamics.xyz | head -10 > equilibrated.xyz

Example 7: QM/MM Calculation for Molecular Crystals
====================================================

**Goal**: Calculate excited states in a periodic molecular crystal using QM/MM.

File Structure
--------------

::

    crystal/
    ├── crystal.xyz
    ├── crystal.ff
    └── dftbaby.cfg

crystal.ff
----------

Force field definition with periodic box::

    # Lattice vectors (Angstrom)
    50.0  0.0  0.0
    0.0  50.0  0.0
    0.0   0.0  50.0

    # Atom types and positions
    C  0.0  0.0  0.0
    C  1.4  0.0  0.0
    H  2.0  0.9  0.0
    ...

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-10
    long_range_correction = 1

    # QM region (Python list syntax)
    qmmm_partitioning = "[0,1,2,3,4,5,6,7,8,9]"

    # Force field file
    periodic_force_field = crystal.ff

    # Excited states
    nstates = 10

    # Active space (important for large QM regions)
    nr_active_occ = 50
    nr_active_virt = 50

Run Command
-----------

For excited states::

    LR_TDDFTB.py crystal.xyz

For geometry optimization::

    optimize.py crystal.xyz 0

(The QM/MM setup is read automatically from ``dftbaby.cfg``)

Example 8: Constrained Geometry Optimization
=============================================

**Goal**: Optimize geometry while fixing certain bond lengths or angles.

constraints.txt
---------------

::

    # Fix C-C bond between atoms 0 and 1 to 1.54 Angstrom
    bond 0 1 1.54

    # Fix angle C-C-C (atoms 0,1,2) to 120 degrees
    angle 0 1 2 120.0

    # Fix dihedral angle (atoms 0,1,2,3) to 180 degrees
    dihedral 0 1 2 3 180.0

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0
    scf_conv = 1e-10

    [GeometryOptimization]
    state = 0
    coord_system = cartesian
    grad_tol = 1.0e-5
    max_steps = 500
    method = BFGS

Run Command
-----------

::

    GeometryOptimization.py molecule.xyz --constraints=constraints.txt

Example 9: Charged Species Calculation
=======================================

**Goal**: Calculate excited states of a cation or anion.

dftbaby.cfg (Cation)
--------------------

::

    [DFTBaby]
    # Total charge +1
    charge = 1

    # Doublet (one unpaired electron)
    multiplicity = 2

    scf_conv = 1e-10
    long_range_correction = 1
    nstates = 10

Run Command
-----------

::

    LR_TDDFTB.py cation.xyz

dftbaby.cfg (Anion)
-------------------

::

    [DFTBaby]
    # Total charge -1
    charge = -1

    # Doublet
    multiplicity = 2

    scf_conv = 1e-10
    long_range_correction = 1
    nstates = 10

Example 10: High-Accuracy Calculation
======================================

**Goal**: Maximize accuracy for publication-quality results.

dftbaby.cfg
-----------

::

    [DFTBaby]
    charge = 0

    # Very tight SCF convergence
    scf_conv = 1e-14

    # Disable DIIS for better convergence
    density_mixer = None

    # Long-range correction
    long_range_correction = 1

    # Dispersion correction (if needed)
    dispersion_correction = 1

    # Excited states
    nstates = 20

    # Very tight TD-DFTB convergence
    iter_conv = 1e-10

    # Increase maximum iterations if needed
    max_iter = 200

Run Command
-----------

::

    LR_TDDFTB.py molecule.xyz > high_accuracy.log

Quick Reference: Common Settings
=================================

DFTBaby Section
---------------

+---------------------------+-------------------+----------------------------------------+
| Parameter                 | Default           | Description                            |
+===========================+===================+========================================+
| ``charge``                | 0                 | Total molecular charge                 |
+---------------------------+-------------------+----------------------------------------+
| ``multiplicity``          | 1                 | Spin multiplicity (2S+1)               |
+---------------------------+-------------------+----------------------------------------+
| ``scf_conv``              | 1e-6              | SCF convergence threshold              |
+---------------------------+-------------------+----------------------------------------+
| ``long_range_correction`` | 0                 | Enable LC-DFTB (0 or 1)                |
+---------------------------+-------------------+----------------------------------------+
| ``dispersion_correction`` | 0                 | Enable Grimme's D3 (0 or 1)            |
+---------------------------+-------------------+----------------------------------------+
| ``nstates``               | 5                 | Number of excited states               |
+---------------------------+-------------------+----------------------------------------+
| ``iter_conv``             | 1e-6              | TD-DFTB convergence                    |
+---------------------------+-------------------+----------------------------------------+
| ``density_mixer``         | "DIIS"            | Mixing algorithm (None, DIIS, Pulay)   |
+---------------------------+-------------------+----------------------------------------+

SurfaceHopping Section
----------------------

+---------------------------+-------------------+----------------------------------------+
| Parameter                 | Default           | Description                            |
+===========================+===================+========================================+
| ``initial_state``         | 0                 | Starting electronic state              |
+---------------------------+-------------------+----------------------------------------+
| ``nstates``               | 2                 | Number of excited states               |
+---------------------------+-------------------+----------------------------------------+
| ``nstep``                 | 1000              | Number of MD steps                     |
+---------------------------+-------------------+----------------------------------------+
| ``nuclear_step``          | 0.1               | Time step (fs)                         |
+---------------------------+-------------------+----------------------------------------+
| ``dyn_mode``              | "E"               | "E" (NVE), "T" (NVT), "M" (meta)       |
+---------------------------+-------------------+----------------------------------------+
| ``temp``                  | 300.0             | Temperature (K) for NVT                |
+---------------------------+-------------------+----------------------------------------+
| ``decoherence_correction``| 0                 | Enable decoherence (0 or 1)            |
+---------------------------+-------------------+----------------------------------------+
| ``output_step``           | 1                 | Output frequency                       |
+---------------------------+-------------------+----------------------------------------+

GeometryOptimization Section
-----------------------------

+---------------------------+-------------------+----------------------------------------+
| Parameter                 | Default           | Description                            |
+===========================+===================+========================================+
| ``state``                 | 0                 | Electronic state to optimize           |
+---------------------------+-------------------+----------------------------------------+
| ``coord_system``          | "cartesian"       | "cartesian" or "internal"              |
+---------------------------+-------------------+----------------------------------------+
| ``grad_tol``              | 1e-5              | Gradient convergence                   |
+---------------------------+-------------------+----------------------------------------+
| ``func_tol``              | 1e-8              | Energy convergence                     |
+---------------------------+-------------------+----------------------------------------+
| ``max_steps``             | 100000            | Maximum optimization steps             |
+---------------------------+-------------------+----------------------------------------+
| ``method``                | "CG"              | BFGS, CG, Newton, Steepest Descent     |
+---------------------------+-------------------+----------------------------------------+
| ``calc_hessian``          | 0                 | Calculate frequencies (0 or 1)         |
+---------------------------+-------------------+----------------------------------------+

Tips and Best Practices
========================

1. **Start Simple**

   - Begin with default settings
   - Add options only when needed
   - Test with small molecules first

2. **Convergence Issues**

   - Increase ``scf_conv`` and ``iter_conv``
   - Try ``density_mixer = None``
   - Check geometry for problems

3. **Long Simulations**

   - Increase ``output_step`` to reduce file size
   - Use smaller ``nstates`` if high states not needed
   - Enable ``decoherence_correction`` for surface hopping

4. **Accuracy vs. Speed**

   - Default settings: good balance
   - High accuracy: tighter convergence, more states
   - Fast screening: looser convergence, fewer states

5. **Memory Management**

   - Use ``nr_active_occ`` and ``nr_active_virt`` for large molecules
   - Reduce ``nstates`` if memory issues occur
   - Consider QM/MM for very large systems

Complete Workflow Example
==========================

Here's a complete workflow for studying photodynamics:

Step 1: Ground State Optimization
----------------------------------

Create ``dftbaby.cfg``::

    [DFTBaby]
    charge = 0
    long_range_correction = 1

    [GeometryOptimization]
    state = 0
    method = BFGS
    calc_hessian = 1

Run::

    GeometryOptimization.py molecule.xyz
    cp optimized.xyz s0_min.xyz

Step 2: Vertical Excitation
----------------------------

Update ``dftbaby.cfg``::

    [DFTBaby]
    charge = 0
    long_range_correction = 1
    nstates = 20

Run::

    LR_TDDFTB.py s0_min.xyz > absorption.log

Step 3: S1 Optimization
------------------------

Update ``dftbaby.cfg``::

    [GeometryOptimization]
    state = 1

Run::

    GeometryOptimization.py s0_min.xyz
    cp optimized.xyz s1_min.xyz

Step 4: Emission Energy
------------------------

Run::

    LR_TDDFTB.py s1_min.xyz > emission.log

Step 5: Non-adiabatic Dynamics
-------------------------------

Generate initial conditions::

    # Create multiple Wigner samples
    python3 << 'EOF'
    from DFTB.Dynamics import WignerSampling
    ws = WignerSampling('s1_min.xyz')
    ws.sample(nsamples=50)
    EOF

Update ``dftbaby.cfg``::

    [SurfaceHopping]
    initial_state = 1
    nstates = 3
    nstep = 10000
    nuclear_step = 0.1
    dyn_mode = "E"
    decoherence_correction = 1

Run trajectories::

    for i in {1..50}; do
        mkdir traj_$i
        cd traj_$i
        cp ../dynamics_$i.in dynamics.in
        cp ../dftbaby.cfg .
        SurfaceHopping.py &
        cd ..
    done
    wait

Analyze results::

    python3 << 'EOF'
    import numpy as np
    import matplotlib.pyplot as plt
    from glob import glob

    # Calculate population decay
    trajectories = glob('traj_*/state.dat')
    # Analysis code here...
    EOF

Additional Resources
====================

- Full example files: ``examples/`` directory in repository
- Command-line help: ``program.py --help``
- Python API: ``usage_guide.rst``
- Troubleshooting: ``usage_guide.rst`` troubleshooting section
