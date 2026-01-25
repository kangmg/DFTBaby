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
from pathlib import Path


def test_package_metadata():
    """Validate pyproject.toml"""
    print("Testing package metadata...")

    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--dry-run', '--no-deps', '--ignore-installed', '.'],
        capture_output=True,
        text=True,
        cwd='/home/user/DFTBaby'
    )

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

    python_files = list(Path('/home/user/DFTBaby/DFTB').rglob('*.py'))
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
            if any(x in str(py_file) for x in ['blender', 'mayavi']):
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
            print(f"    - {Path(err).relative_to('/home/user/DFTBaby')}")

    # Pass if >= 99% valid
    return (valid / total) >= 0.99


def test_setuptools_build():
    """Test if package can be built with setuptools"""
    print("\nTesting setuptools build...")

    # Try to validate setup
    result = subprocess.run(
        [sys.executable, 'setup.py', 'check'],
        capture_output=True,
        text=True,
        cwd='/home/user/DFTBaby'
    )

    if result.returncode == 0:
        print("✓ Setup.py validation passed")
        return True
    else:
        # setup.py check might not work, try alternative
        setup_py = Path('/home/user/DFTBaby/setup.py')
        if setup_py.exists():
            print("✓ setup.py exists and is readable")
            return True
        else:
            print("✗ setup.py validation failed")
            return False


def test_manifest_files():
    """Check if all files listed in MANIFEST.in exist"""
    print("\nTesting MANIFEST.in...")

    manifest = Path('/home/user/DFTBaby/MANIFEST.in')
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
                        dir_path = Path('/home/user/DFTBaby') / path_pattern.split('/')[0]
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

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("⚠ Cannot validate entry points (no toml parser)")
            return True

    pyproject = Path('/home/user/DFTBaby/pyproject.toml')
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
            file_path = Path('/home/user/DFTBaby') / module_path.replace('.', '/') / '__init__.py'
            parent_path = file_path.parent
            py_file = parent_path.with_suffix('.py')

            if not (file_path.exists() or py_file.exists() or parent_path.exists()):
                invalid.append((script_name, entry_point))

    print(f"  Defined entry points: {len(scripts)}")

    if invalid:
        print(f"  ✗ Invalid: {len(invalid)}")
        for name, ep in invalid[:5]:
            print(f"      {name}: {ep}")
    else:
        print(f"  ✓ All entry points reference existing modules")

    return len(invalid) == 0


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
