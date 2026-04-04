"""
The files <atom name>.py are generated automatically. They contain
orbital energies and radial wavefunctions of non-relativistic
DFT-LDA pseudo atoms WITH a confinement potential.
"""

from importlib import import_module

from DFTB.AtomicData import atom_names

# Keep legacy index-based access pseudo_atoms_list[Z-1], but only populate
# entries for modules that actually exist in this repository.
pseudo_atoms_list = [None] * len(atom_names)
for Z, name in enumerate(atom_names, start=1):
    module_name = "%s.%s" % (__name__, name)
    try:
        pseudo_atoms_list[Z - 1] = import_module(module_name)
    except ModuleNotFoundError as exc:
        # Ignore only truly missing pseudo-atom modules for unsupported Z.
        # If a dependency inside an existing module is missing, surface it.
        if exc.name == module_name:
            continue
        raise
