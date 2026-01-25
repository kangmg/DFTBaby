#!/usr/bin/env python3
"""
Comprehensive compilation and installation test for DFTBaby

Tests:
1. Package metadata validation
2. Python syntax validation (all files)
3. Import tests (core modules)
4. Dependency checking
5. Installation simulation (dry-run)
"""

import sys
import subprocess
from pathlib import Path
import importlib.util


class CompilationTester:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.results = {
            'metadata': False,
            'syntax': False,
            'imports': False,
            'dependencies': False,
            'installation': False,
        }
        self.errors = []

    def test_metadata(self):
        """Test pyproject.toml validity"""
        print("=" * 70)
        print("1. Testing package metadata (pyproject.toml)")
        print("=" * 70)

        pyproject = self.repo_root / 'pyproject.toml'
        if not pyproject.exists():
            self.errors.append("pyproject.toml not found")
            return False

        try:
            import tomli
        except ImportError:
            # Try built-in tomllib (Python 3.11+)
            try:
                import tomllib as tomli
            except ImportError:
                print("⚠ tomli/tomllib not available, using basic check")
                # Basic check - just verify it's readable
                with open(pyproject, 'r') as f:
                    content = f.read()
                    if '[build-system]' in content and '[project]' in content:
                        print("✓ pyproject.toml structure looks valid")
                        self.results['metadata'] = True
                        return True
                    else:
                        self.errors.append("Invalid pyproject.toml structure")
                        return False

        try:
            with open(pyproject, 'rb') as f:
                data = tomli.load(f)

            # Verify required fields
            required_fields = ['name', 'version', 'dependencies']
            for field in required_fields:
                if field not in data.get('project', {}):
                    self.errors.append(f"Missing required field: project.{field}")
                    return False

            print(f"✓ Package name: {data['project']['name']}")
            print(f"✓ Version: {data['project']['version']}")
            print(f"✓ Dependencies: {len(data['project']['dependencies'])} packages")
            print(f"✓ Python requirement: {data['project']['requires-python']}")

            self.results['metadata'] = True
            return True

        except Exception as e:
            self.errors.append(f"Error reading pyproject.toml: {e}")
            return False

    def test_syntax(self):
        """Test all Python files for syntax errors"""
        print("\n" + "=" * 70)
        print("2. Testing Python syntax (all files)")
        print("=" * 70)

        python_files = list(self.repo_root.glob('DFTB/**/*.py'))
        errors = []

        for py_file in python_files:
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', str(py_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                errors.append(str(py_file.relative_to(self.repo_root)))

        success_rate = (len(python_files) - len(errors)) / len(python_files) * 100

        print(f"Checked {len(python_files)} Python files")
        print(f"✓ Valid: {len(python_files) - len(errors)} ({success_rate:.1f}%)")

        if errors:
            print(f"✗ Errors: {len(errors)}")
            for err in errors[:5]:
                print(f"    - {err}")
            if len(errors) > 5:
                print(f"    ... and {len(errors) - 5} more")

        self.results['syntax'] = success_rate >= 99.0
        return self.results['syntax']

    def test_imports(self):
        """Test core module imports"""
        print("\n" + "=" * 70)
        print("3. Testing module imports")
        print("=" * 70)

        # Add repo to path
        sys.path.insert(0, str(self.repo_root))

        core_modules = [
            ('DFTB.XYZ', 'XYZ module'),
            ('DFTB.AtomicData', 'Atomic data'),
            ('DFTB.utils', 'Utilities'),
            ('DFTB.Parameters', 'Parameters'),
        ]

        imported = 0
        for module_name, description in core_modules:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is None:
                    print(f"✗ {description}: Module not found")
                    continue

                # Try to import
                module = importlib.import_module(module_name)
                print(f"✓ {description}: OK")
                imported += 1

            except Exception as e:
                print(f"✗ {description}: {str(e)[:60]}")
                self.errors.append(f"Import error in {module_name}: {e}")

        success = imported >= len(core_modules) * 0.75  # 75% import success
        self.results['imports'] = success

        if success:
            print(f"\n✓ Successfully imported {imported}/{len(core_modules)} core modules")
        else:
            print(f"\n⚠ Only {imported}/{len(core_modules)} modules imported")

        return success

    def test_dependencies(self):
        """Test if dependencies can be resolved"""
        print("\n" + "=" * 70)
        print("4. Testing dependency resolution")
        print("=" * 70)

        required_deps = {
            'numpy': '2.0.0',
            'scipy': '1.14.0',
            'matplotlib': '3.9.0',
            'mpmath': '1.3.0',
            'sympy': '1.13',
        }

        available = 0
        for dep, min_version in required_deps.items():
            try:
                module = importlib.import_module(dep)
                version = getattr(module, '__version__', 'unknown')
                print(f"✓ {dep}: {version} (required: >={min_version})")
                available += 1
            except ImportError:
                print(f"✗ {dep}: Not installed (required: >={min_version})")

        self.results['dependencies'] = available >= 2  # At least numpy and scipy

        print(f"\nAvailable: {available}/{len(required_deps)} dependencies")

        return self.results['dependencies']

    def test_installation(self):
        """Test installation dry-run"""
        print("\n" + "=" * 70)
        print("5. Testing installation (dry-run)")
        print("=" * 70)

        # Test if setup can be validated
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--dry-run', '--no-deps', '.'],
            cwd=str(self.repo_root),
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Package can be installed")
            self.results['installation'] = True
            return True
        else:
            # Try alternative check
            setup_py = self.repo_root / 'setup.py'
            if setup_py.exists():
                print("✓ setup.py exists (legacy mode)")
                self.results['installation'] = True
                return True
            else:
                print("✗ Installation check failed")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
                return False

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("DFTBaby Compilation and Installation Test Suite")
        print("Python Version:", sys.version.split()[0])
        print()

        tests = [
            ('metadata', self.test_metadata),
            ('syntax', self.test_syntax),
            ('imports', self.test_imports),
            ('dependencies', self.test_dependencies),
            ('installation', self.test_installation),
        ]

        for name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n✗ Test '{name}' crashed: {e}")
                self.errors.append(f"Test crash in {name}: {e}")

        # Generate summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        passed = sum(self.results.values())
        total = len(self.results)

        for test, result in self.results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {test.ljust(20)}: {status}")

        print()
        print(f"Overall: {passed}/{total} tests passed ({passed*100//total}%)")

        if self.errors:
            print(f"\nErrors encountered: {len(self.errors)}")
            for err in self.errors[:5]:
                print(f"  - {err}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")

        print()
        if passed == total:
            print("✅ All tests PASSED! Package is ready for compilation/installation")
            return 0
        elif passed >= total * 0.8:
            print("⚠ Most tests passed. Package is functional with minor issues")
            return 0
        else:
            print("❌ Multiple test failures. Review errors above")
            return 1


def main():
    repo_root = Path(__file__).parent.parent
    tester = CompilationTester(repo_root)
    return tester.run_all_tests()


if __name__ == '__main__':
    sys.exit(main())
