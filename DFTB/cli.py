"""
Console entry-point dispatcher.

DFTBaby historically exposed many ``*.py`` script names as command-line tools.
This module now supports both legacy script names and modern command-style
invocation via ``dftbaby <command>`` / ``dftbaby-<command>``.
"""

from __future__ import annotations

import os
import runpy
import sys
from typing import Dict, List

SCRIPT_TO_MODULE: Dict[str, str] = {
    "DFTB2.py": "DFTB.DFTB2",
    "LR_TDDFTB.py": "DFTB.LR_TDDFTB",
    "optimize.py": "DFTB.optimize",
    "optimize_neb.py": "DFTB.optimize_neb",
    "optimize_meci.py": "DFTB.optimize_meci",
    "scan.py": "DFTB.scan",
    "split_xyz.py": "DFTB.Modeling.split_xyz",
    "show_molcoords.py": "DFTB.Modeling.show_molcoords",
    "modify_internal.py": "DFTB.Modeling.modify_internal",
    "cut_sphere.py": "DFTB.Modeling.cut_sphere",
    "convert_xyz.py": "DFTB.Modeling.convert_xyz",
    "nanotube_builder.py": "DFTB.Modeling.nanotube_builder",
    "filter_fragments.py": "DFTB.Modeling.filter_fragments",
    "check_initial_distribution.py": "DFTB.Dynamics.check_initial_distribution",
    "random_velocities.py": "DFTB.Dynamics.random_velocities",
    "initial_conditions.py": "DFTB.Dynamics.initial_conditions",
    "absorption_spectrum.py": "DFTB.Analyse.absorption_spectrum",
    "ph_correlation.py": "DFTB.Analyse.ph_correlation",
    "SurfaceHopping.py": "DFTB.Dynamics.SurfaceHopping",
    "populations.py": "DFTB.Dynamics.Analyse.populations",
    "trajViewer2.py": "DFTB.Dynamics.Analyse.Viewer.trajViewer2",
    "reconstruct.py": "DFTB.MetaDynamics.reconstruct",
    "GeometryOptimization.py": "DFTB.Optimize.GeometryOptimization",
    "assign_atom_types.py": "DFTB.ForceField.assign_atom_types",
    "copy_atom_types.py": "DFTB.ForceField.copy_atom_types",
    "ff_optimize.py": "DFTB.ForceField.ff_optimize",
    "fit_electric_charges.py": "DFTB.ForceField.fit_electric_charges",
    "fit_magnetic_dipoles.py": "DFTB.ForceField.fit_magnetic_dipoles",
    "electrostatic_potential.py": "DFTB.Poisson.electrostatic_potential",
    "vector_potential.py": "DFTB.Poisson.vector_potential",
    "electroSka.py": "DFTB.MultipleScattering.electroSka",
}

# command aliases installed as separate entry points
SCRIPT_ALIASES: Dict[str, str] = {
    "dftbaby-dftb2": "DFTB2.py",
    "dftbaby-lrtddftb": "LR_TDDFTB.py",
    "dftbaby-surface-hopping": "SurfaceHopping.py",
    "dftbaby-geometry-opt": "GeometryOptimization.py",
    "dftbaby-optimize": "optimize.py",
    "dftbaby-initial-conditions": "initial_conditions.py",
    "dftbaby-populations": "populations.py",
    "dftbaby-scan": "scan.py",
}

# subcommands for `dftbaby <command>`
SUBCOMMAND_TO_SCRIPT: Dict[str, str] = {
    "dftb2": "DFTB2.py",
    "lrtddftb": "LR_TDDFTB.py",
    "surface-hopping": "SurfaceHopping.py",
    "geometry-opt": "GeometryOptimization.py",
    "optimize": "optimize.py",
    "optimize-neb": "optimize_neb.py",
    "optimize-meci": "optimize_meci.py",
    "scan": "scan.py",
    "initial-conditions": "initial_conditions.py",
    "populations": "populations.py",
}

OPTIONAL_COMMAND_HINTS: Dict[str, str] = {
    "trajViewer2.py": "This command requires optional GUI dependencies (`pip install .[gui]`).",
    "nanotube_builder.py": "This command requires compiled Thomson extension (`cd DFTB/extensions && make`).",
    "reconstruct.py": "This command requires metadynamics dependencies (`pip install .[metadynamics]`).",
    "electroSka.py": (
        "This command requires advanced optional deps (`pip install .[advanced]`) "
        "and compiled multiple-scattering extensions."
    ),
}


def _resolve_script_name(raw_name: str) -> str:
    return SCRIPT_ALIASES.get(raw_name, raw_name)


def _run_script(legacy_script: str, argv_tail: List[str]) -> None:
    module_name = SCRIPT_TO_MODULE.get(legacy_script)
    if module_name is None:
        known = ", ".join(sorted(SCRIPT_TO_MODULE))
        raise SystemExit(
            "Unknown DFTBaby console script '%s'. Known scripts: %s"
            % (legacy_script, known)
        )

    old_argv = sys.argv[:]
    try:
        sys.argv = [legacy_script] + list(argv_tail)
        runpy.run_module(module_name, run_name="__main__")
    except (ImportError, ModuleNotFoundError) as exc:
        hint = OPTIONAL_COMMAND_HINTS.get(legacy_script)
        if hint is not None:
            raise SystemExit(
                "Cannot run '%s': %s\nOriginal import error: %s"
                % (legacy_script, hint, exc)
            ) from exc
        raise
    finally:
        sys.argv = old_argv


def _print_help() -> None:
    print("Usage: dftbaby <command> [args]")
    print("")
    print("Common commands:")
    print("  dftb2               Ground-state SCC-DFTB")
    print("  lrtddftb            Excited states / spectrum")
    print("  geometry-opt        Geometry optimization")
    print("  surface-hopping     Non-adiabatic dynamics")
    print("  initial-conditions  Wigner initial conditions")
    print("  populations         Trajectory population analysis")
    print("  scan                Coordinate scan")
    print("")
    print("Use `dftbaby list` to show all registered command mappings.")


def _print_mapping() -> None:
    print("DFTBaby command mappings:")
    for command, script in sorted(SUBCOMMAND_TO_SCRIPT.items()):
        print("  %-18s -> %s" % (command, script))


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in {"-h", "--help", "help"}:
        _print_help()
        return

    command = args[0]
    if command in {"list", "--list"}:
        _print_mapping()
        return

    # convenience: allow passing a legacy script name directly to `dftbaby`
    legacy_script = SUBCOMMAND_TO_SCRIPT.get(command, command)
    _run_script(legacy_script, args[1:])


def dispatch() -> None:
    script_name = os.path.basename(sys.argv[0])
    legacy_script = _resolve_script_name(script_name)
    _run_script(legacy_script, sys.argv[1:])


if __name__ == "__main__":
    main()
