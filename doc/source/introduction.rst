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
 - Mayavi (for graphical visualization)

**For DFTB Parametrization Only:**

 - Gaussian 09/16, Psi4, or PySCF (for calculating reference forces/energies)

.. note::
   Most users do **not** need Gaussian/Psi4/PySCF. Pre-parametrized repulsive
   potentials are already included for common elements (H, C, N, O, S, Ag, etc.).
   Quantum chemistry programs are only required when creating new DFTB parameters
   for unsupported elements or developing custom parametrizations.

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

