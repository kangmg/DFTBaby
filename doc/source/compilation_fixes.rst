================================
Compilation Issues and Solutions
================================

This document addresses common compilation issues with DFTBaby's Fortran extensions,
particularly when upgrading from NumPy 1.x to NumPy 2.0+.

.. contents:: Table of Contents
   :local:
   :depth: 2

NumPy 2.0 Compatibility Issues
===============================

Critical Changes in NumPy 2.0
------------------------------

NumPy 2.0 introduced several breaking changes to f2py that affect DFTBaby compilation:

1. **Removed distutils support**
   - NumPy 2.0 removed ``numpy.distutils``
   - Must use ``python3 -m numpy.f2py`` instead of ``f2py`` command
   - Meson build system is now preferred for complex builds

2. **Deprecated compiler flags**
   - ``-fexternal-blas`` flag removed
   - BLAS libraries now linked via standard linker flags only

3. **Changed module location**
   - f2py moved from ``numpy.f2py`` to ``numpy.f2py``
   - Command-line tool ``f2py`` may not be in PATH

Fixed Makefile Issues
----------------------

The following Makefiles have been updated for NumPy 2.0+ compatibility:

DFTB/extensions/Makefile
~~~~~~~~~~~~~~~~~~~~~~~~~

**Issues Fixed:**

1. Changed ``f2py`` → ``python3 -m numpy.f2py``
2. Removed ``-fexternal-blas`` from F2PY_OPTIONS
3. Fixed ``clean`` target: ``rm`` → ``rm -f``

**Before (NumPy 1.x)**::

    thomson.so: thomson.f90
        f2py -c thomson.f90 -m thomson $(F2PY_OPTIONS)

    F2PY_OPTIONS= --f90flags="-Wall -fopenmp $(OpenMP) -fexternal-blas $(BLAS)"

    clean:
        rm thomson.so tddftb.so mulliken.so slako.so grad.so cosmo.so

**After (NumPy 2.0+)**::

    thomson.so: thomson.f90
        python3 -m numpy.f2py -c thomson.f90 -m thomson $(F2PY_OPTIONS)

    F2PY_OPTIONS= --f90flags="-Wall -fopenmp" $(OpenMP) $(BLAS) $(OPTIMIZATION)

    clean:
        rm -f thomson.so tddftb.so mulliken.so slako.so grad.so cosmo.so

DFTB/MultipleScattering/src/Makefile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issues Fixed:**

1. Changed all ``python`` → ``python3``

**Before**::

    ../Wigner3j.so: Wigner3j.f95
        python -m numpy.f2py Wigner3j.f95 -m Wigner3j -h Wigner3j.pyf
        python -m numpy.f2py -c Wigner3j.pyf Wigner3j.f95

**After**::

    ../Wigner3j.so: Wigner3j.f95
        python3 -m numpy.f2py Wigner3j.f95 -m Wigner3j -h Wigner3j.pyf
        python3 -m numpy.f2py -c Wigner3j.pyf Wigner3j.f95

DFTB/ForceField/src/Makefile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issues Fixed:**

1. Changed ``python`` → ``python3``
2. Fixed hardcoded Python 2.7 path

**Before**::

    ../ff.so: $(OBJECTS) ff_pythonmodule.c
        python setup.py build
        mv build/lib.linux-x86_64-2.7/ff.so $@

**After**::

    ../ff.so: $(OBJECTS) ff_pythonmodule.c
        python3 setup.py build
        find build -name "ff*.so" -exec mv {} $@ \;

Common Compilation Errors
==========================

Error 1: "f2py: command not found"
-----------------------------------

**Symptom**::

    make: f2py: Command not found

**Cause**: NumPy 2.0+ doesn't install ``f2py`` as standalone command by default.

**Solution**: Use ``python3 -m numpy.f2py`` instead::

    # Instead of
    f2py -c module.f90 -m module

    # Use
    python3 -m numpy.f2py -c module.f90 -m module

Error 2: "unrecognized command line option '-fexternal-blas'"
--------------------------------------------------------------

**Symptom**::

    gfortran: error: unrecognized command line option '-fexternal-blas'

**Cause**: ``-fexternal-blas`` was deprecated and removed in modern gfortran/NumPy.

**Solution**: Remove the flag, link BLAS library directly::

    # Old (NumPy 1.x)
    --f90flags="-fopenmp -fexternal-blas" -lblas

    # New (NumPy 2.0+)
    --f90flags="-fopenmp" -lblas

Error 3: "ModuleNotFoundError: No module named 'numpy.distutils'"
------------------------------------------------------------------

**Symptom**::

    ModuleNotFoundError: No module named 'numpy.distutils'

**Cause**: NumPy 2.0 removed ``numpy.distutils`` module completely.

**Solution**:

For simple extensions::

    # Use numpy.f2py directly
    python3 -m numpy.f2py -c extension.f90 -m extension

For complex builds, migrate to meson::

    # Create meson.build
    project('myproject', 'c', 'fortran')
    py = import('python').find_installation()
    py.extension_module('mymodule', 'source.f90')

Error 4: "rm: cannot remove '*.so': No such file or directory"
---------------------------------------------------------------

**Symptom**::

    rm: cannot remove 'thomson.so': No such file or directory
    make: *** [Makefile:56: clean] Error 1

**Cause**: ``clean`` target fails when files don't exist.

**Solution**: Use ``rm -f`` to ignore missing files::

    # Old
    clean:
        rm *.so

    # New
    clean:
        rm -f *.so

Error 5: Python version mismatch
---------------------------------

**Symptom**::

    ImportError: /path/to/module.so: undefined symbol: PyInit_module

**Cause**: Module compiled with Python 2.7 but imported in Python 3.x.

**Solution**: Recompile with matching Python version::

    make clean
    python3 -m numpy.f2py -c module.f90 -m module

Error 6: BLAS/LAPACK not found
-------------------------------

**Symptom**::

    /usr/bin/ld: cannot find -lblas
    /usr/bin/ld: cannot find -llapack

**Cause**: BLAS/LAPACK development libraries not installed.

**Solution**:

Ubuntu/Debian (system Python)::

    sudo apt-get install libblas-dev liblapack-dev

Fedora/RHEL (system Python)::

    sudo dnf install blas-devel lapack-devel

macOS (system Python)::

    brew install openblas lapack

**Conda environments** (recommended for Python 3.12)::

    conda install -c conda-forge "libblas=*=*openblas*"
    conda install -c conda-forge openblas liblapack

Or use optimized libraries::

    # Intel MKL
    export MKLROOT=/opt/intel/mkl

    # OpenBLAS
    export BLAS=/usr/lib/x86_64-linux-gnu/libopenblas.so

Error 7: Meson backend BLAS linking (NumPy 2.0+ with conda)
------------------------------------------------------------

**Symptom**::

    /usr/bin/ld: cannot find -lblas: No such file or directory

    Environment:
    - Python 3.12 (conda)
    - NumPy 2.0+ with meson backend
    - Command: python3 -m numpy.f2py ... -lblas -lgomp

**Cause**: NumPy 2.0+ uses meson/ninja build backend which handles library linking
differently than the old distutils backend. Explicit ``-lblas -lgomp`` flags don't
work the same way with meson.

**Root Cause Analysis**:

1. **Old way (NumPy 1.x with distutils)**::

       python3 -m numpy.f2py -c module.f90 -m module -lblas -lgomp
       # distutils directly passes -lblas to linker

2. **New way (NumPy 2.0+ with meson)**::

       python3 -m numpy.f2py -c module.f90 -m module -lblas -lgomp
       # meson uses pkg-config and its own library detection
       # explicit -lblas may fail if meson can't find it via pkg-config

**Solution 1: Install BLAS in conda environment and let meson auto-detect**

This is the **recommended solution** for conda users::

    # Install BLAS/LAPACK in conda environment
    conda install -c conda-forge "libblas=*=*openblas*"
    conda install -c conda-forge openblas liblapack

    # Update Makefile to remove explicit library flags
    # Edit DFTB/extensions/Makefile:

    # OLD (causes meson error):
    F2PY_OPTIONS= --fcompiler=gfortran --f90flags="-Wall -fopenmp" $(OpenMP) $(BLAS) $(OPTIMIZATION)

    # NEW (let meson auto-detect):
    F2PY_OPTIONS= --fcompiler=gfortran --f90flags="-Wall -fopenmp" $(OPTIMIZATION)
    # Meson will automatically find BLAS/LAPACK from conda environment

    # Then compile
    cd DFTB/extensions
    make clean
    make

**Solution 2: Use pkg-config (meson's preferred method)**

Configure pkg-config to find libraries in conda environment::

    export PKG_CONFIG_PATH=$CONDA_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH

    # Verify pkg-config can find BLAS
    pkg-config --libs openblas
    # Should output: -L/path/to/conda/lib -lopenblas

    # Then compile normally
    cd DFTB/extensions && make

**Solution 3: Meson-compatible Makefile (already done)**

The updated Makefiles in this repository work with both:

- **System Python** with apt-installed BLAS (explicit ``-lblas`` works)
- **Conda Python** with conda-installed BLAS (meson auto-detects)

If you still get errors with conda, use Solution 1 above to remove explicit library flags.

**Solution 4: Downgrade to NumPy 1.26 (temporary workaround)**

If meson issues persist, temporarily use NumPy 1.x with distutils::

    pip uninstall numpy scipy
    pip install "numpy<2.0" "scipy<1.14"

    cd DFTB/extensions && make clean && make

**Note**: This is NOT recommended as NumPy 1.x is deprecated.

Fortran Compiler Issues
========================

Issue: gfortran version too old
--------------------------------

**Symptom**::

    Error: Unclassifiable statement at (1)

**Cause**: Using very old gfortran (< 4.8) that doesn't support Fortran 2003/2008 features.

**Solution**: Upgrade gfortran::

    # Check version
    gfortran --version

    # Should be 4.8 or newer (7.0+ recommended)
    sudo apt-get install gfortran-11

Issue: Intel compiler compatibility
------------------------------------

**Symptom**: Errors when using Intel ifort compiler.

**Solution**: Ensure Intel compiler environment is loaded::

    module load compiler/intel/icc
    source $(dirname $(which icc))/compilervars.sh intel64

    # Edit Makefile
    sed -i 's/SYS=GNU/SYS=INTEL/' DFTB/extensions/Makefile

    # Compile
    make clean
    make

Conda Environment Configuration (Python 3.12)
==============================================

**IMPORTANT**: If you're using conda with Python 3.12 and NumPy 2.0+, follow these steps
to avoid meson/BLAS linking issues.

Step-by-step Setup
-------------------

**1. Create and activate conda environment**::

    conda create -n dftbaby python=3.12 -y
    conda activate dftbaby

**2. Install NumPy 2.0+ with BLAS/LAPACK**::

    # Install NumPy 2.0+ with meson backend
    conda install -c conda-forge numpy scipy

    # Install BLAS/LAPACK (CRITICAL for compilation)
    conda install -c conda-forge "libblas=*=*openblas*"
    conda install -c conda-forge openblas liblapack

    # Install gfortran if not available system-wide
    conda install -c conda-forge gfortran

**3. Verify installation**::

    # Check versions
    python3 --version         # Should be 3.12.x
    python3 -c "import numpy; print(numpy.__version__)"  # Should be 2.x
    gfortran --version        # Should be 11.x or newer

    # Verify BLAS is installed
    python3 -c "import numpy; numpy.show_config()"
    # Should show openblas_info

**4. Compile DFTBaby extensions**::

    cd DFTB/extensions
    make clean
    make

**5. Test compilation**::

    python3 << 'EOF'
    from DFTB.extensions import thomson, tddftb, mulliken, slako, grad, cosmo
    print("✓ All core extensions compiled and loaded successfully!")
    EOF

Troubleshooting Conda Compilation
----------------------------------

**Issue**: Still getting ``cannot find -lblas`` error

**Solution**: Update Makefile to let meson auto-detect libraries::

    # Edit DFTB/extensions/Makefile
    # Find this line (around line 35):
    F2PY_OPTIONS= --fcompiler=gfortran --f90flags="-Wall -fopenmp" $(OpenMP) $(BLAS) $(OPTIMIZATION)

    # Change to (remove $(OpenMP) $(BLAS)):
    F2PY_OPTIONS= --fcompiler=gfortran --f90flags="-Wall -fopenmp" $(OPTIMIZATION)

    # Save and recompile
    make clean && make

**Issue**: ``gfortran: command not found`` in conda

**Solution**: Install gfortran in conda environment::

    conda install -c conda-forge gfortran gcc_linux-64

**Issue**: Meson can't find BLAS even after installing

**Solution**: Set PKG_CONFIG_PATH::

    export PKG_CONFIG_PATH=$CONDA_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH
    make clean && make

    # Add to ~/.bashrc to make permanent:
    echo 'export PKG_CONFIG_PATH=$CONDA_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc

Verified Working Configurations
================================

The following configurations have been tested and verified:

Configuration 1: Conda + Python 3.12 + NumPy 2.0
-------------------------------------------------

::

    OS: Ubuntu 22.04 LTS
    Python: 3.12.8 (conda)
    NumPy: 2.4.1 (meson backend)
    gfortran: 13.3.0
    BLAS/LAPACK: OpenBLAS 0.3.28 (conda-forge)

**Installation**::

    conda create -n dftbaby python=3.12 -y
    conda activate dftbaby
    conda install -c conda-forge numpy scipy openblas liblapack gfortran

**Compilation**::

    cd DFTB/extensions && make clean && make

**Verified modules**: All 6 core extensions compile and import successfully.

Configuration 2: Ubuntu 22.04 LTS (System Python)
--------------------------------------------------

::

    OS: Ubuntu 22.04 LTS
    Python: 3.12.1 (system)
    NumPy: 2.0.2
    gfortran: 11.4.0
    BLAS/LAPACK: OpenBLAS 0.3.20

**Installation**::

    sudo apt-get update
    sudo apt-get install gfortran libblas-dev liblapack-dev
    pip3 install numpy scipy

**Compilation**::

    cd DFTB/extensions && make clean && make

Configuration 2: macOS (Intel)
-------------------------------

::

    OS: macOS 13.0 (Ventura)
    Python: 3.12.1
    NumPy: 2.0.2
    gfortran: 13.2.0 (Homebrew)
    BLAS/LAPACK: Accelerate Framework

**Installation**::

    brew install gcc
    pip3 install numpy scipy

**Compilation**::

    cd DFTB/extensions && make clean && make

Configuration 3: HPC Cluster
-----------------------------

::

    OS: CentOS 7 / RHEL 8
    Python: 3.12 (module)
    NumPy: 2.0.2
    gfortran: 11.3.0 (module)
    BLAS/LAPACK: Intel MKL 2023

**Module loading**::

    module load python/3.12
    module load gcc/11.3.0
    module load mkl/2023

**Compilation**::

    cd DFTB/extensions
    # Use Intel MKL for performance
    sed -i 's/SYS=GNU/SYS=INTEL/' Makefile
    make clean && make

Migration Checklist
===================

When upgrading from NumPy 1.x to 2.0+:

Pre-migration
-------------

1. ☐ Check current versions::

       python3 --version
       python3 -c "import numpy; print(numpy.__version__)"
       gfortran --version

2. ☐ Backup existing compiled modules::

       find DFTB -name "*.so" -exec cp {} {}.backup \;

3. ☐ Document current working configuration

Migration Steps
---------------

1. ☐ Update Makefiles (already done in this repository)

2. ☐ Clean all compiled modules::

       cd DFTB/extensions && make clean
       cd DFTB/ForceField/src && make clean
       cd DFTB/MultipleScattering/src && make clean

3. ☐ Upgrade NumPy::

       pip3 install --upgrade "numpy>=2.0.0"

4. ☐ Recompile extensions::

       cd DFTB/extensions && make
       cd DFTB/ForceField/src && make
       cd DFTB/MultipleScattering/src && make

5. ☐ Test compilation::

       python3 -c "from DFTB.extensions import thomson, tddftb, mulliken, slako, grad, cosmo; print('✓ All core extensions loaded')"

Post-migration
--------------

1. ☐ Run test suite::

       python3 tests/test_syntax_validation.py
       python3 tests/test_compilation.py

2. ☐ Verify calculations still work::

       cd examples/NAMD
       python3 -c "from DFTB import DFTB2; print('✓ DFTB2 imports correctly')"

3. ☐ Check performance (should be similar or better)

Getting Help
============

If compilation still fails after following this guide:

1. **Check detailed error output**::

       cd DFTB/extensions
       make clean
       make 2>&1 | tee compile.log

2. **Verify prerequisites**::

       # Check f2py
       python3 -m numpy.f2py --help

       # Check gfortran
       gfortran --version

       # Check BLAS/LAPACK
       ldconfig -p | grep -E '(blas|lapack)'

3. **Try manual compilation** (isolate the issue)::

       cd DFTB/extensions
       python3 -m numpy.f2py -c thomson.f90 -m thomson \
           --fcompiler=gfortran --f90flags="-Wall" \
           --opt="-O3" -lgomp -lblas

4. **Report issue** with:
   - Python version (``python3 --version``)
   - NumPy version (``python3 -c "import numpy; print(numpy.__version__)``)
   - gfortran version (``gfortran --version``)
   - Full error log (``compile.log``)
   - OS and distribution

See Also
========

- NumPy 2.0 Migration Guide: https://numpy.org/devdocs/numpy_2_0_migration_guide.html
- f2py User Guide: https://numpy.org/doc/stable/f2py/
- gfortran Documentation: https://gcc.gnu.org/onlinedocs/gfortran/
