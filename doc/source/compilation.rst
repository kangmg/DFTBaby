==================
Compilation Guide
==================

DFTBaby includes Fortran extensions for performance-critical calculations. This guide explains how to compile them.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

DFTBaby has three main Fortran extension modules:

1. **Core Extensions** (``DFTB/extensions/``) - Essential for most calculations
2. **Force Field** (``DFTB/ForceField/src/``) - Required for QM/MM simulations
3. **Multiple Scattering** (``DFTB/MultipleScattering/src/``) - Advanced electronic structure methods

Prerequisites
=============

Required Tools
--------------

- **Python 3.12+** with NumPy 2.0+
- **Fortran compiler**: ``gfortran`` (recommended) or Intel ``ifort``
- **f2py**: Included with NumPy
- **BLAS/LAPACK**: Linear algebra libraries
- **make**: Build automation tool

Install on Ubuntu/Debian
-------------------------

::

    sudo apt-get update
    sudo apt-get install gfortran libblas-dev liblapack-dev make

Install on macOS
----------------

::

    brew install gcc make openblas lapack

Install on Fedora/RHEL
----------------------

::

    sudo dnf install gcc-gfortran blas-devel lapack-devel make

Install in Conda Environment (Recommended for Python 3.12)
-----------------------------------------------------------

**IMPORTANT**: If you're using conda with Python 3.12 and NumPy 2.0+, use conda-forge
packages to avoid meson/BLAS linking issues.

::

    # Create conda environment
    conda create -n dftbaby python=3.12 -y
    conda activate dftbaby

    # Install all dependencies
    conda install -c conda-forge numpy scipy openblas liblapack gfortran make

    # Verify installation
    python3 -c "import numpy; print(f'NumPy {numpy.__version__}')"
    gfortran --version

**For conda users experiencing BLAS linking errors**, see the detailed troubleshooting guide:
**➜ :doc:`compilation_fixes`** (Error 7: Meson backend BLAS linking)

Verify Installation
-------------------

Check that required tools are available::

    # Check gfortran
    gfortran --version

    # Check f2py
    python3 -c "import numpy.f2py; print(numpy.f2py.__version__)"

    # Check make
    make --version

Core Extensions (Essential)
============================

These extensions are **required** for most DFTBaby calculations.

Location
--------

``DFTB/extensions/``

Modules Compiled
----------------

- ``thomson.so`` - Thomson charge distribution
- ``tddftb.so`` - TD-DFTB calculations
- ``mulliken.so`` - Mulliken population analysis
- ``slako.so`` - Slater-Koster transformations
- ``grad.so`` - Analytical gradients
- ``cosmo.so`` - COSMO solvation model

Compilation Steps
-----------------

**Method 1: Simple compilation (GNU gfortran)**

For **system Python** or **conda with working BLAS**::

    cd DFTB/extensions/
    make clean
    make

This compiles all extensions with default settings (GNU compilers, OpenMP parallelization).

**Method 1b: Conda environment (if regular Makefile fails)**

If you're using conda and get ``cannot find -lblas`` errors, use the conda-specific Makefile::

    cd DFTB/extensions/

    # Use Makefile.conda which lets meson auto-detect libraries
    make -f Makefile.conda clean
    make -f Makefile.conda

    # Or create a symlink to use regular make commands
    mv Makefile Makefile.system
    ln -s Makefile.conda Makefile
    make clean && make

**Why use Makefile.conda?**

- NumPy 2.0+ uses meson/ninja build backend (not distutils)
- Meson handles library linking differently - explicit ``-lblas -lgomp`` may fail
- ``Makefile.conda`` removes explicit library flags and lets meson auto-detect
- Works with conda-installed BLAS/LAPACK packages

**Method 2: Intel compilers (for HPC clusters)**

If you have Intel compilers and MKL::

    cd DFTB/extensions/

    # Load Intel modules (on HPC systems)
    module load compiler/intel/icc
    source $(dirname $(which icc))/compilervars.sh intel64
    source $(dirname $(which icc))/../mkl/bin/mklvars.sh intel64

    # Edit Makefile: change SYS=GNU to SYS=INTEL
    sed -i 's/SYS=GNU/SYS=INTEL/' Makefile

    # Compile
    make clean
    make

**Method 3: Manual f2py (if make fails)**

::

    cd DFTB/extensions/

    # Compile each module individually
    python3 -m numpy.f2py -c thomson.f90 -m thomson --fcompiler=gfortran --opt="-O3"
    python3 -m numpy.f2py -c tddftb.f90 -m tddftb --fcompiler=gfortran --opt="-O3"
    python3 -m numpy.f2py -c mulliken.f90 -m mulliken --fcompiler=gfortran --opt="-O3"
    python3 -m numpy.f2py -c slako.f90 -m slako --fcompiler=gfortran --opt="-O3"
    python3 -m numpy.f2py -c grad.f90 -m grad --fcompiler=gfortran --opt="-O3"
    python3 -m numpy.f2py -c cosmo.f90 -m cosmo --fcompiler=gfortran --opt="-O3"

Verification
------------

Test that modules can be imported::

    cd DFTB/extensions/
    python3 << 'EOF'
    import thomson
    import tddftb
    import mulliken
    import slako
    import grad
    import cosmo
    print("✓ All core extensions compiled successfully!")
    EOF

Performance Settings
--------------------

For optimal performance with OpenMP parallelization::

    # Set number of threads (adjust based on your CPU)
    export OMP_NUM_THREADS=4

    # Increase stack size (prevents segfaults in parallel code)
    export OMP_STACKSIZE=1g
    ulimit -s unlimited

Add these lines to your ``~/.bashrc`` to make them permanent.

Force Field Extensions (QM/MM)
===============================

These extensions are **required only for QM/MM simulations** with periodic systems.

Location
--------

``DFTB/ForceField/src/``

Module Compiled
---------------

- ``ff.so`` - UFF/DREIDING force fields with periodic boundary conditions

Compilation Steps
-----------------

::

    cd DFTB/ForceField/src/
    make clean
    make

This compiles the C-based force field module.

Verification
------------

::

    cd DFTB/ForceField/
    python3 << 'EOF'
    import ff
    print("✓ Force field extension compiled successfully!")
    EOF

Troubleshooting
---------------

**Issue**: ``lapack`` not found

::

    # Install LAPACK development files
    sudo apt-get install liblapack-dev

**Issue**: ``setup.py`` errors

Check that ``setup.py`` exists in ``DFTB/ForceField/src/``::

    ls -la DFTB/ForceField/src/setup.py

Multiple Scattering Extensions (Advanced)
==========================================

These extensions are **optional** and used for advanced electronic structure calculations.

Location
--------

``DFTB/MultipleScattering/src/``

Modules Compiled
----------------

- ``Wigner3j.so`` - Wigner 3j symbols
- ``coul90.so`` - Coulomb and spherical Bessel functions
- ``mod_bessel.so`` - Modified spherical Bessel functions
- ``sphharm.so`` - Spherical harmonics
- ``cms.so`` - Continuum multiple scattering
- ``ms.so`` - Bound orbital multiple scattering
- ``photo.so`` - Photoionization cross sections
- ``numerov.so`` - Numerov solver for radial Schrödinger equation

Compilation Steps
-----------------

::

    cd DFTB/MultipleScattering/src/
    make clean
    make

This compiles all multiple scattering modules. Compilation may take several minutes.

Verification
------------

::

    cd DFTB/MultipleScattering/
    python3 << 'EOF'
    import Wigner3j
    import coul90
    import mod_bessel
    import sphharm
    import cms
    import ms
    import photo
    import numerov
    print("✓ All multiple scattering extensions compiled successfully!")
    EOF

Complete Compilation Script
============================

To compile everything at once::

    #!/bin/bash
    # compile_all.sh - Compile all DFTBaby Fortran extensions

    set -e  # Exit on error

    echo "Compiling DFTBaby Fortran Extensions"
    echo "===================================="

    # Set performance options
    export OMP_NUM_THREADS=4
    export OMP_STACKSIZE=1g

    # 1. Core Extensions (Required)
    echo ""
    echo "[1/3] Compiling core extensions..."
    cd DFTB/extensions/
    make clean
    make
    cd ../..
    echo "✓ Core extensions compiled"

    # 2. Force Field (for QM/MM)
    echo ""
    echo "[2/3] Compiling force field extensions..."
    cd DFTB/ForceField/src/
    make clean
    make
    cd ../../..
    echo "✓ Force field extensions compiled"

    # 3. Multiple Scattering (optional)
    echo ""
    echo "[3/3] Compiling multiple scattering extensions..."
    cd DFTB/MultipleScattering/src/
    make clean
    make
    cd ../../..
    echo "✓ Multiple scattering extensions compiled"

    echo ""
    echo "===================================="
    echo "All extensions compiled successfully!"
    echo ""
    echo "Performance settings:"
    echo "  OMP_NUM_THREADS=$OMP_NUM_THREADS"
    echo "  OMP_STACKSIZE=$OMP_STACKSIZE"
    echo ""
    echo "To use parallelization, run:"
    echo "  export OMP_NUM_THREADS=4"
    echo "  export OMP_STACKSIZE=1g"
    echo "  ulimit -s unlimited"

Save this as ``compile_all.sh`` and run::

    chmod +x compile_all.sh
    ./compile_all.sh

Common Issues and Solutions
============================

Compilation Errors
------------------

**Error**: ``f2py: command not found``

**Solution**: Install NumPy with f2py::

    pip3 install --upgrade numpy

**Error**: ``gfortran: command not found``

**Solution**: Install gfortran compiler::

    sudo apt-get install gfortran

**Error**: ``cannot find -lblas`` or ``cannot find -llapack``

**Solution**: Install BLAS and LAPACK::

    sudo apt-get install libblas-dev liblapack-dev

**Error**: ``Segmentation fault`` when importing modules

**Solution**: Increase stack size::

    export OMP_STACKSIZE=1g
    ulimit -s unlimited

**Error**: Module version mismatch

**Solution**: Recompile with the same Python version::

    make clean
    make

Import Errors
-------------

**Error**: ``ImportError: cannot import name 'thomson'``

**Solution**: Ensure you're in the correct directory or extensions are in Python path::

    # Check if .so files exist
    ls -la DFTB/extensions/*.so

    # Test from DFTB parent directory
    cd /path/to/DFTBaby
    python3 -c "from DFTB.extensions import thomson"

**Error**: ``ImportError: undefined symbol: __kmpc_fork_call``

**Solution**: Link with OpenMP library::

    # Recompile with explicit OpenMP flag
    cd DFTB/extensions/
    make clean
    F2PY_OPTIONS="--f90flags='-fopenmp' -lgomp" make

Performance Issues
------------------

**Slow calculations despite compilation**

1. Check OpenMP is enabled::

       # Should show your thread count
       echo $OMP_NUM_THREADS

2. Verify parallel regions in code::

       nm DFTB/extensions/tddftb.so | grep -i omp

3. Profile with different thread counts::

       for i in 1 2 4 8; do
           export OMP_NUM_THREADS=$i
           echo "Threads: $i"
           time python3 your_calculation.py
       done

Platform-Specific Notes
=======================

Linux (Intel MKL)
-----------------

For maximum performance on Intel CPUs with MKL::

    # Load Intel MKL
    source /opt/intel/mkl/bin/mklvars.sh intel64

    # Compile with Intel compilers
    cd DFTB/extensions/
    sed -i 's/SYS=GNU/SYS=INTEL/' Makefile
    make clean
    make

    # Set MKL threads
    export MKL_NUM_THREADS=4

macOS (Apple Silicon)
---------------------

For M1/M2/M3 Macs::

    # Install Homebrew GCC (not Apple's gcc)
    brew install gcc

    # Use Homebrew's gfortran
    cd DFTB/extensions/
    make clean
    FC=gfortran-13 make  # Version may vary

Windows (WSL)
-------------

Use Windows Subsystem for Linux (WSL2)::

    # In WSL Ubuntu
    sudo apt-get update
    sudo apt-get install gfortran libblas-dev liblapack-dev

    # Then follow Linux instructions
    cd DFTB/extensions/
    make

HPC Clusters
------------

On SLURM-based clusters::

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=8
    #SBATCH --time=00:30:00

    # Load modules
    module load python/3.12
    module load gcc/11.3.0
    module load openblas

    # Compile
    cd $SLURM_SUBMIT_DIR/DFTB/extensions/
    make clean
    make

    # Set threads
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

Testing Compilation
===================

Quick Test Suite
----------------

::

    #!/usr/bin/env python3
    """Test all compiled extensions"""

    import sys

    def test_core_extensions():
        """Test core extensions"""
        print("Testing core extensions...")
        try:
            from DFTB.extensions import thomson, tddftb, mulliken, slako, grad, cosmo
            print("  ✓ All core extensions loaded")
            return True
        except ImportError as e:
            print(f"  ✗ Core extension import failed: {e}")
            return False

    def test_forcefield():
        """Test force field extension"""
        print("Testing force field extension...")
        try:
            from DFTB.ForceField import ff
            print("  ✓ Force field extension loaded")
            return True
        except ImportError as e:
            print(f"  ✗ Force field import failed: {e}")
            return False

    def test_multiple_scattering():
        """Test multiple scattering extensions"""
        print("Testing multiple scattering extensions...")
        try:
            from DFTB.MultipleScattering import (
                Wigner3j, coul90, mod_bessel, sphharm,
                cms, ms, photo, numerov
            )
            print("  ✓ All multiple scattering extensions loaded")
            return True
        except ImportError as e:
            print(f"  ✗ Multiple scattering import failed: {e}")
            return False

    if __name__ == "__main__":
        print("DFTBaby Fortran Extensions Test")
        print("=" * 40)

        results = []
        results.append(test_core_extensions())
        results.append(test_forcefield())
        results.append(test_multiple_scattering())

        print("=" * 40)
        if all(results):
            print("SUCCESS: All extensions working!")
            sys.exit(0)
        else:
            print("FAILURE: Some extensions failed")
            sys.exit(1)

Save as ``test_extensions.py`` and run::

    python3 test_extensions.py

Performance Benchmarking
------------------------

Simple benchmark for parallelization::

    #!/usr/bin/env python3
    """Benchmark OpenMP performance"""

    import time
    import numpy as np
    from DFTB.extensions import tddftb

    def benchmark(threads):
        """Run benchmark with specified thread count"""
        import os
        os.environ['OMP_NUM_THREADS'] = str(threads)

        # Create test data
        n = 1000
        A = np.random.rand(n, n)
        B = np.random.rand(n, n)

        # Time matrix operation
        start = time.time()
        C = np.dot(A, B)
        elapsed = time.time() - start

        return elapsed

    print("OpenMP Performance Benchmark")
    print("Threads | Time (s) | Speedup")
    print("-" * 35)

    baseline = None
    for threads in [1, 2, 4, 8]:
        t = benchmark(threads)
        if baseline is None:
            baseline = t
        speedup = baseline / t
        print(f"   {threads:2d}   | {t:7.3f}  | {speedup:6.2f}x")

NumPy 2.0 Migration Issues
==========================

**IMPORTANT**: If you experience compilation errors, especially after upgrading from NumPy 1.x to 2.0+,
see the comprehensive troubleshooting guide:

**➜ :doc:`compilation_fixes`**

This includes:

- NumPy 2.0 breaking changes (removed ``-fexternal-blas``, ``numpy.distutils``)
- Fixed Makefile changes
- Common error messages and solutions
- Verified working configurations
- Step-by-step migration checklist

Further Information
===================

- Makefile details: Check comments in each ``Makefile``
- f2py documentation: https://numpy.org/doc/stable/f2py/
- OpenMP tuning: https://www.openmp.org/
- Compiler options: ``gfortran --help`` or ``ifort --help``

For compilation issues, check:

1. Python version: ``python3 --version``
2. NumPy version: ``python3 -c "import numpy; print(numpy.__version__)``
3. f2py availability: ``python3 -m numpy.f2py --help``
4. Compiler version: ``gfortran --version``
5. Library paths: ``ldconfig -p | grep -E "(blas|lapack)"``
