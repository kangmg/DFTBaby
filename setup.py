#!/usr/bin/env python
"""
DFTBaby setup script

Note: This setup.py is maintained for backward compatibility.
For modern installations, please use:
    pip install .

This will use pyproject.toml for configuration.

For Fortran extensions, they need to be built separately:
    cd DFTB/extensions/ && make
    cd DFTB/ForceField/src/ && make
    cd DFTB/MultipleScattering/src/ && make
    cd DFTB/Poisson/src/ && make

Or use the provided build script (to be created).
"""

import warnings
warnings.warn(
    "Direct setup.py usage is deprecated. Please use 'pip install .' instead.",
    DeprecationWarning,
    stacklevel=2
)

import setuptools
from setuptools import setup

# Fortran extensions are now built separately using f2py and Makefiles
# See DFTB/extensions/Makefile, DFTB/ForceField/src/Makefile, etc.
# numpy.distutils has been removed in numpy 2.0                   

# Package discovery is now handled by pyproject.toml
# Extension modules need to be built separately (see Makefiles)

if __name__ == "__main__":
    # For backward compatibility, call setuptools.setup()
    # But configuration is now in pyproject.toml
    setup()
