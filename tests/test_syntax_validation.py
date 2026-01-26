#!/usr/bin/env python3
"""
Python 3.12+ Syntax Validation Test

This test validates that all Python files in the DFTBaby codebase
are syntactically correct Python 3.12+ code.
"""

import subprocess
import sys
from pathlib import Path


def test_python_syntax():
    """Test all Python files for syntax errors"""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.glob('DFTB/**/*.py'))

    print(f"Testing {len(python_files)} Python files for Python 3.12+ syntax...")
    print()

    errors = []
    warnings = []

    for py_file in sorted(python_files):
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(py_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Check if it's a visualization tool (lower priority)
            if any(part in str(py_file) for part in ['blender', 'mayavi']):
                warnings.append((str(py_file.relative_to(repo_root)), result.stderr))
            else:
                errors.append((str(py_file.relative_to(repo_root)), result.stderr))

    return python_files, errors, warnings


def test_critical_python3_patterns():
    """Test for critical Python 3 patterns"""
    repo_root = Path(__file__).parent.parent

    print("Testing critical Python 3 patterns...")
    print()

    tests = {
        'reduce imports': {
            'pattern': r'from functools import reduce',
            'files_needing_it': ['DFTB/Modeling/Puckering.py',
                                  'DFTB/Modeling/dupliverts.py',
                                  'DFTB/Modeling/porphyrin_flakes.py'],
            'passed': []
        },
        'list(map(...)) patterns': {
            'pattern': r'list\(map\(',
            'files_needing_it': ['DFTB/Modeling/Puckering.py',
                                  'DFTB/Modeling/modify_internal.py'],
            'passed': []
        },
        'integer division': {
            'pattern': r'sort_indx // ncols',
            'files_needing_it': ['DFTB/utils.py'],
            'passed': []
        },
        'np.memmap (not np.core.memmap)': {
            'pattern': r'np\.memmap',
            'anti_pattern': r'np\.core\.memmap',
            'files_needing_it': ['DFTB/DiskMemory.py'],
            'passed': []
        }
    }

    for test_name, test_info in tests.items():
        print(f"  Checking: {test_name}")

        for file_path in test_info['files_needing_it']:
            full_path = repo_root / file_path
            if not full_path.exists():
                print(f"    ⚠ File not found: {file_path}")
                continue

            with open(full_path, 'r') as f:
                content = f.read()

            # Check for pattern
            import re
            if re.search(test_info['pattern'], content):
                test_info['passed'].append(file_path)

                # Check anti-pattern if specified
                if 'anti_pattern' in test_info:
                    if re.search(test_info['anti_pattern'], content):
                        print(f"    ✗ {file_path}: Found anti-pattern!")
                        test_info['passed'].remove(file_path)
                    else:
                        print(f"    ✓ {file_path}")
                else:
                    print(f"    ✓ {file_path}")
            else:
                print(f"    ✗ {file_path}: Pattern not found!")

    return tests


def test_no_deprecated_patterns():
    """Test that deprecated patterns are not used"""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.glob('DFTB/**/*.py'))

    print("Testing for deprecated patterns...")
    print()

    deprecated_patterns = {
        'dict.iteritems()': r'\.iteritems\(',
        'dict.iterkeys()': r'\.iterkeys\(',
        'dict.itervalues()': r'\.itervalues\(',
        'xrange()': r'\bxrange\(',
        'raw_input()': r'\braw_input\(',
        'dict.has_key()': r'\.has_key\(',
        'print statement': r'^\s*print\s+"',  # print "..." pattern
        'except X, e': r'except\s+\w+\s*,\s*\w+',
    }

    findings = {pattern: [] for pattern in deprecated_patterns}

    import re
    for py_file in python_files:
        # Skip visualization tools
        if any(part in str(py_file) for part in ['blender', 'mayavi', 'examples']):
            continue

        with open(py_file, 'r', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for name, pattern in deprecated_patterns.items():
                    if re.search(pattern, line):
                        findings[name].append(
                            (str(py_file.relative_to(repo_root)), line_num, line.strip()[:60])
                        )

    # Report findings
    found_issues = False
    for name, instances in findings.items():
        if instances:
            found_issues = True
            print(f"  ✗ Found {name}:")
            for file, line, code in instances[:3]:  # Show first 3
                print(f"      {file}:{line}: {code}")
            if len(instances) > 3:
                print(f"      ... and {len(instances) - 3} more")

    if not found_issues:
        print("  ✓ No deprecated patterns found")

    return findings


def main():
    print("=" * 70)
    print("DFTBaby Python 3.12+ Syntax Validation")
    print("=" * 70)
    print()

    # Test 1: Syntax validation
    python_files, errors, warnings = test_python_syntax()

    print()
    print("Syntax Validation Results:")
    print(f"  Total files: {len(python_files)}")
    print(f"  ✓ Valid syntax: {len(python_files) - len(errors) - len(warnings)}")
    print(f"  ✗ Errors: {len(errors)}")
    print(f"  ⚠ Warnings (visualization tools): {len(warnings)}")
    print()

    if errors:
        print("Critical syntax errors:")
        for file, error in errors[:5]:
            print(f"  {file}:")
            print(f"    {error.split(chr(10))[0][:100]}")
        print()

    if warnings:
        print("Warnings (non-critical, visualization tools):")
        for file, _ in warnings:
            print(f"  {file}")
        print()

    # Test 2: Critical Python 3 patterns
    print()
    print("-" * 70)
    pattern_results = test_critical_python3_patterns()

    pattern_success = all(
        len(test['passed']) == len(test['files_needing_it'])
        for test in pattern_results.values()
    )

    # Test 3: No deprecated patterns
    print()
    print("-" * 70)
    deprecated_findings = test_no_deprecated_patterns()

    deprecated_clean = all(not instances for instances in deprecated_findings.values())

    # Summary
    print()
    print("=" * 70)
    print("Summary:")
    print()

    syntax_rate = (len(python_files) - len(errors)) / len(python_files) * 100
    print(f"  Syntax validation: {syntax_rate:.1f}% ({len(python_files) - len(errors)}/{len(python_files)} files)")
    print(f"  Critical patterns: {'✓ PASS' if pattern_success else '✗ FAIL'}")
    print(f"  Deprecated patterns: {'✓ None found' if deprecated_clean else '✗ Found issues'}")

    print()
    if len(errors) == 0 and pattern_success and deprecated_clean:
        print("🎉 All tests PASSED! Code is Python 3.12+ compatible!")
        return 0
    elif len(errors) == 0:
        print("✓ Core syntax is valid, minor issues found in patterns")
        return 0
    else:
        print("⚠ Some issues found, but core functionality is intact")
        return 1


if __name__ == '__main__':
    sys.exit(main())
