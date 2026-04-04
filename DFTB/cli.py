"""
Console entry-point dispatcher.

Most legacy DFTBaby scripts are implemented as module-level ``if __name__ ==
"__main__"`` blocks rather than exported ``main()`` callables. This dispatcher
keeps packaging entry points stable by routing each installed script name to its
original module.
"""
import os
import runpy
import sys

SCRIPT_TO_MODULE = {
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


def dispatch():
    script_name = os.path.basename(sys.argv[0])
    module_name = SCRIPT_TO_MODULE.get(script_name)
    if module_name is None:
        known = ", ".join(sorted(SCRIPT_TO_MODULE))
        raise SystemExit(
            "Unknown DFTBaby console script '%s'. Known scripts: %s"
            % (script_name, known)
        )
    runpy.run_module(module_name, run_name="__main__")
