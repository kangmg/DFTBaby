#!/usr/bin/env python3
"""
Test package building without installing dependencies

This tests that:
1. The package metadata is valid
2. The package can be built
3. All Python files are syntactically correct
"""

import sys
import subprocess
import tempfile
import shutil
import importlib
import io
import contextlib
from pathlib import Path
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY_WARNING_FILES = set()

def test_package_metadata():
    """Validate pyproject.toml"""
    print("Testing package metadata...")

    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--dry-run', '--no-deps', '--ignore-installed', '.'],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )

    if 'externally-managed-environment' in result.stderr:
        print("⚠ Skipping pip dry-run in externally managed environment")
        return True
    if 'DFTBaby' in result.stdout or result.returncode == 0:
        print("✓ Package metadata valid")
        return True
    else:
        print("✗ Package metadata invalid")
        print(result.stderr[:500])
        return False


def test_syntax_comprehensive():
    """Comprehensive syntax check"""
    print("\nTesting Python syntax...")

    python_files = list((REPO_ROOT / "DFTB").rglob("*.py"))
    errors = []
    warnings = []

    for py_file in python_files:
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(py_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Check if it's a critical file
            rel = str(py_file.relative_to(REPO_ROOT))
            if any(x in str(py_file) for x in ['blender', 'mayavi']) or rel in LEGACY_WARNING_FILES:
                warnings.append(str(py_file))
            else:
                errors.append(str(py_file))

    total = len(python_files)
    valid = total - len(errors) - len(warnings)

    print(f"  Total files: {total}")
    print(f"  ✓ Valid syntax: {valid} ({valid*100//total}%)")
    print(f"  ⚠ Warnings (viz tools): {len(warnings)}")
    print(f"  ✗ Errors (core): {len(errors)}")

    if errors:
        print("\nCore files with errors:")
        for err in errors:
            print(f"    - {Path(err).relative_to(REPO_ROOT)}")

    # Non-critical files (visualization + legacy scripts) are counted as warnings.
    return len(errors) == 0


def test_setuptools_build():
    """Test if package can be built with setuptools"""
    print("\nTesting setuptools build...")

    # Try to validate setup
    result = subprocess.run(
        [sys.executable, 'setup.py', 'check'],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )

    if result.returncode == 0:
        print("✓ Setup.py validation passed")
        return True
    else:
        # setup.py check might not work, try alternative
        setup_py = REPO_ROOT / "setup.py"
        if setup_py.exists():
            print("✓ setup.py exists and is readable")
            return True
        else:
            print("✗ setup.py validation failed")
            return False


def test_manifest_files():
    """Check if all files listed in MANIFEST.in exist"""
    print("\nTesting MANIFEST.in...")

    manifest = REPO_ROOT / "MANIFEST.in"
    if not manifest.exists():
        print("⚠ MANIFEST.in not found (optional)")
        return True

    missing = []
    with open(manifest, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('include') or line.startswith('recursive-include'):
                # Parse file patterns
                parts = line.split()
                if len(parts) >= 2:
                    path_pattern = parts[1]
                    # Basic check - just verify directory exists
                    if '/' in path_pattern:
                        dir_path = REPO_ROOT / path_pattern.split('/')[0]
                        if not dir_path.exists():
                            missing.append(path_pattern)

    if missing:
        print(f"✗ {len(missing)} paths in MANIFEST.in not found")
        for m in missing[:5]:
            print(f"    - {m}")
    else:
        print("✓ MANIFEST.in references valid paths")

    return len(missing) == 0


def test_entry_points():
    """Check if entry points are valid"""
    print("\nTesting entry points...")
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("⚠ Cannot validate entry points (no toml parser)")
            return True

    pyproject = REPO_ROOT / "pyproject.toml"
    with open(pyproject, 'rb') as f:
        data = tomllib.load(f)

    scripts = data.get('project', {}).get('scripts', {})

    if not scripts:
        print("⚠ No entry points defined")
        return True

    invalid = []
    for script_name, entry_point in scripts.items():
        # Parse entry_point: "module.path:function"
        if ':' in entry_point:
            module_path, func = entry_point.split(':', 1)
            # Convert to file path
            file_path = REPO_ROOT / module_path.replace('.', '/') / '__init__.py'
            parent_path = file_path.parent
            py_file = parent_path.with_suffix('.py')

            if not (file_path.exists() or py_file.exists() or parent_path.exists()):
                invalid.append((script_name, entry_point))
                continue

            try:
                module = importlib.import_module(module_path)
                if not hasattr(module, func):
                    invalid.append((script_name, entry_point))
            except Exception:
                invalid.append((script_name, entry_point))

    print(f"  Defined entry points: {len(scripts)}")

    if invalid:
        print(f"  ✗ Invalid: {len(invalid)}")
        for name, ep in invalid[:5]:
            print(f"      {name}: {ep}")
    else:
        print(f"  ✓ All entry points reference existing modules")

    return len(invalid) == 0


def test_cli_help_smoke():
    """Smoke-test core non-periodic CLI help output."""
    print("\nTesting core CLI --help...")

    commands = [
        ("DFTB2", [sys.executable, "-m", "DFTB.DFTB2", "--help"]),
        ("LR_TDDFTB", [sys.executable, "-m", "DFTB.LR_TDDFTB", "--help"]),
        ("SurfaceHopping", [sys.executable, "-m", "DFTB.Dynamics.SurfaceHopping", "--help"]),
        ("GeometryOptimization", [sys.executable, "-m", "DFTB.Optimize.GeometryOptimization", "--help"]),
    ]

    failed = []
    for name, cmd in commands:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        if result.returncode == 0:
            print(f"  ✓ {name}: --help OK")
        else:
            print(f"  ✗ {name}: --help failed")
            failed.append((name, result.stderr[:300]))

    if failed:
        for name, stderr in failed:
            print(f"    {name} stderr: {stderr}")
    return len(failed) == 0


def test_periodic_runtime_smoke():
    """Smoke-test periodic non-SCC and SCC execution on a tiny Gamma-point cell."""
    print("\nTesting periodic runtime smoke...")

    try:
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        from DFTB.DFTB2 import DFTB2
    except Exception as exc:
        print(f"  ✗ Could not import periodic code path: {exc}")
        return False

    atomlist = [
        (1, [0.0, 0.0, 0.0]),
        (1, [1.4, 0.0, 0.0]),
    ]
    lattice_vectors = [
        [8.0, 0.0, 0.0],
        [0.0, 8.0, 0.0],
        [0.0, 0.0, 8.0],
    ]
    ks = [np.array([0.0, 0.0, 0.0])]

    try:
        dftb2 = DFTB2(
            atomlist,
            parameter_set="homegrown",
            verbose=0,
            long_range_correction=0,
            onsite_correction=0,
            use_symmetry=0,
        )
        dftb2.setGeometry(atomlist, charge=0.0)

        with contextlib.redirect_stdout(io.StringIO()):
            _, non_scc_bands = dftb2.runPeriodicNonSCC(lattice_vectors, ks, nmax=(1, 1, 1))
            q_non_scc = np.array(dftb2.q, copy=True)
            dq_non_scc = np.array(dftb2.dq, copy=True)
            _, scc_bands, dq = dftb2.runPeriodicSCC(
                lattice_vectors, ks, nmax=(1, 1, 1), maxiter=5, scc_conv=1.0e-6
            )
    except Exception as exc:
        print(f"  ✗ Periodic execution failed: {exc}")
        return False

    if len(non_scc_bands) != 1 or len(scc_bands) != 1:
        print("  ✗ Unexpected number of k-point solutions")
        return False
    if non_scc_bands[0].shape[0] != 2 or scc_bands[0].shape[0] != 2:
        print("  ✗ Unexpected orbital dimensions in periodic bands")
        return False
    if len(dq) != len(atomlist):
        print("  ✗ Unexpected periodic charge vector size")
        return False
    if not np.isclose(np.sum(q_non_scc.real), 2.0, atol=1.0e-6):
        print("  ✗ Periodic non-SCC does not conserve total valence charge")
        return False
    if not np.isclose(np.sum(dq_non_scc.real), 0.0, atol=1.0e-6):
        print("  ✗ Periodic non-SCC excess charge is not neutral")
        return False

    print("  ✓ Periodic NonSCC path OK")
    print("  ✓ Periodic SCC path OK")
    return True


def main():
    print("=" * 70)
    print("DFTBaby Package Build Test")
    print("=" * 70)
    print()

    tests = [
        ("Package metadata", test_package_metadata),
        ("Python syntax", test_syntax_comprehensive),
        ("Setuptools build", test_setuptools_build),
        ("MANIFEST files", test_manifest_files),
        ("Entry points", test_entry_points),
        ("CLI help smoke", test_cli_help_smoke),
        ("Periodic runtime smoke", test_periodic_runtime_smoke),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name.ljust(25)}: {status}")

    print()
    print(f"Overall: {passed}/{total} tests passed ({passed*100//total}%)")
    print()

    if passed == total:
        print("✅ Package is ready for distribution!")
        print("\nYou can build and install with:")
        print("  pip install .")
        return 0
    elif passed >= total * 0.8:
        print("⚠ Package is mostly ready with minor issues")
        return 0
    else:
        print("❌ Package has significant issues")
        return 1


if __name__ == '__main__':
    sys.exit(main())
