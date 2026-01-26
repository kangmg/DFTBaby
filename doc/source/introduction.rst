============
Introduction
============

DFTBaby is a software package for tight-binding DFT calculations on ground and excited states of molecules and for non-adiabatic molecular dynamics simulations.

Prerequisites
=============

**Required:**

 - Python 3.12 or newer
 - NumPy 2.0.0 or newer
 - SciPy 1.14.0 or newer
 - Matplotlib 3.9.0 or newer
 - mpmath 1.3.0 or newer
 - sympy 1.13 or newer
 - BLAS and LAPACK libraries
 - f2py (included with NumPy)

**Optional:**

 - libxc 3.0.0 (for pseudoorbital calculations)
 - Gaussian 09 or newer (for calculating repulsive potentials)
 - Mayavi (for graphical visualization)

Installation
============

Install via pip::

    git clone https://github.com/kangmg/DFTBaby.git
    cd DFTBaby
    pip install .

For development mode::

    pip install -e .

Migration from Python 2
=======================

This package has been migrated from Python 2.7 to Python 3.12+ with NumPy 2.0+ compatibility.
See ``PYTHON3_MIGRATION.md`` for detailed migration information.

Links
=====

 - **Documentation**: https://kangmg.github.io/DFTBaby/
 - **Repository**: https://github.com/kangmg/DFTBaby
 - **Original Website**: http://dftbaby.chemie.uni-wuerzburg.de/

