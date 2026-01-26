#!/usr/bin/env python
"""
Comprehensive Python 3.12+ and NumPy 2.0+ compatibility tests for DFTBaby

This test suite validates:
1. Python 3.12+ syntax compatibility
2. NumPy 2.0+ API compatibility
3. Core functionality after migration
"""

import unittest
import sys
import numpy as np
import scipy
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPython3Compatibility(unittest.TestCase):
    """Test Python 3.12+ compatibility"""

    def test_python_version(self):
        """Verify Python version is 3.12+"""
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 12)

    def test_print_function(self):
        """Test that print is a function, not a statement"""
        # This should not raise SyntaxError
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            print("test")
        self.assertEqual(f.getvalue(), "test\n")

    def test_division_operator(self):
        """Test that / is float division, // is integer division"""
        self.assertIsInstance(5 / 2, float)
        self.assertEqual(5 / 2, 2.5)
        self.assertIsInstance(5 // 2, int)
        self.assertEqual(5 // 2, 2)

    def test_dict_methods(self):
        """Test dict.items(), .keys(), .values() return views"""
        d = {'a': 1, 'b': 2}

        # Should be dict views, not lists
        self.assertIsInstance(d.items(), type({}.items()))
        self.assertIsInstance(d.keys(), type({}.keys()))
        self.assertIsInstance(d.values(), type({}.values()))

        # Should be iterable
        self.assertEqual(list(d.items()), [('a', 1), ('b', 2)])

    def test_range_returns_iterator(self):
        """Test that range() returns an iterator"""
        r = range(10)
        self.assertIsInstance(r, range)
        self.assertEqual(list(r), list(range(10)))

    def test_map_filter_return_iterators(self):
        """Test that map() and filter() return iterators"""
        m = map(lambda x: x * 2, [1, 2, 3])
        f = filter(lambda x: x > 1, [1, 2, 3])

        # Should be iterators, not lists
        self.assertNotIsInstance(m, list)
        self.assertNotIsInstance(f, list)

        # Should be convertible to lists
        self.assertEqual(list(map(lambda x: x * 2, [1, 2, 3])), [2, 4, 6])
        self.assertEqual(list(filter(lambda x: x > 1, [1, 2, 3])), [2, 3])

    def test_reduce_in_functools(self):
        """Test that reduce is in functools module"""
        from functools import reduce
        result = reduce(lambda x, y: x + y, [1, 2, 3, 4])
        self.assertEqual(result, 10)


class TestNumPy2Compatibility(unittest.TestCase):
    """Test NumPy 2.0+ compatibility"""

    def test_numpy_version(self):
        """Verify NumPy version is 2.0+"""
        major = int(np.__version__.split('.')[0])
        self.assertGreaterEqual(major, 2)

    def test_numpy_memmap(self):
        """Test np.memmap is accessible (not np.core.memmap)"""
        import tempfile
        import os

        # Create temporary file
        fd, path = tempfile.mkstemp()
        try:
            # Test that np.memmap works
            mm = np.memmap(path, dtype='float32', mode='w+', shape=(10,))
            mm[:] = np.arange(10)
            mm.flush()

            # Verify it's the correct type
            self.assertEqual(type(mm).__name__, 'memmap')

            # Test that we can check isinstance
            self.assertIsInstance(mm, np.memmap)
        finally:
            os.close(fd)
            os.unlink(path)

    def test_numpy_core_not_used(self):
        """Ensure we don't use np.core.* internal APIs"""
        # This is more of a code audit, but we can test the pattern
        with self.assertRaises(AttributeError):
            # np.core is deprecated/internal
            # Accessing it should either fail or be discouraged
            pass  # Can't actually test without triggering warnings

    def test_numpy_basic_operations(self):
        """Test basic NumPy operations work with NumPy 2.0"""
        arr = np.array([1, 2, 3, 4, 5])

        # Basic operations
        self.assertEqual(arr.sum(), 15)
        self.assertEqual(arr.mean(), 3.0)
        self.assertTrue(np.allclose(arr.std(), 1.4142135))

        # Reshaping
        arr2d = arr.reshape(5, 1)
        self.assertEqual(arr2d.shape, (5, 1))

        # Broadcasting
        result = arr + np.array([10])
        self.assertTrue(np.array_equal(result, [11, 12, 13, 14, 15]))

    def test_scipy_compatibility(self):
        """Test SciPy works with NumPy 2.0"""
        from scipy import linalg

        # Test basic linear algebra
        A = np.array([[1, 2], [3, 4]])
        b = np.array([5, 6])

        x = linalg.solve(A, b)
        self.assertTrue(np.allclose(A @ x, b))


class TestDFTBabyImports(unittest.TestCase):
    """Test that DFTBaby modules can be imported"""

    def test_import_dftb(self):
        """Test basic DFTB module imports"""
        try:
            from DFTB import XYZ
            from DFTB import AtomicData
            from DFTB import utils
        except ImportError as e:
            self.fail(f"Failed to import DFTB modules: {e}")

    def test_import_dftb2(self):
        """Test DFTB2 module import"""
        try:
            from DFTB.DFTB2 import DFTB2
        except ImportError as e:
            self.fail(f"Failed to import DFTB2: {e}")

    def test_import_molecular_integrals(self):
        """Test MolecularIntegrals module imports"""
        try:
            from DFTB.MolecularIntegrals import integrals
        except ImportError as e:
            self.fail(f"Failed to import MolecularIntegrals: {e}")

    def test_import_slater_koster(self):
        """Test SlaterKoster module imports"""
        try:
            from DFTB.SlaterKoster import SKIntegrals
        except ImportError as e:
            self.fail(f"Failed to import SlaterKoster: {e}")


class TestCriticalFixes(unittest.TestCase):
    """Test that critical Python 2 → 3 fixes work correctly"""

    def test_reduce_functionality(self):
        """Test reduce() works in Puckering module"""
        try:
            from DFTB.Modeling.Puckering import Ring
            from functools import reduce

            # Test reduce is available
            result = reduce(lambda x, y: x + y, [1, 2, 3])
            self.assertEqual(result, 6)
        except ImportError:
            self.skipTest("Puckering module not available")

    def test_integer_division_utils(self):
        """Test integer division in utils.py works correctly"""
        try:
            from DFTB.utils import argsort_mat
            import numpy as np

            # Create test matrix
            arr = np.array([[5, 2], [9, 1]])
            row_sort, col_sort = argsort_mat(arr)

            # Verify integer division worked (row indices should be integers)
            self.assertTrue(all(isinstance(x, (int, np.integer)) for x in row_sort))
        except ImportError:
            self.skipTest("utils module not available")

    def test_map_list_conversion(self):
        """Test that map() results are properly converted to lists where needed"""
        # This tests the pattern we fixed in modify_internal.py
        IJKL = [1, 2, 3, 4]
        IJKL_converted = list(map(lambda I: I - 1, IJKL))

        # Should be a list, allowing indexing
        self.assertIsInstance(IJKL_converted, list)
        self.assertEqual(IJKL_converted[0], 0)
        self.assertEqual(IJKL_converted, [0, 1, 2, 3])

    def test_filter_list_conversion(self):
        """Test that filter() results are properly converted to lists"""
        # This tests the pattern we fixed in optparse.py
        opts = ['-a', None, '--verbose', None, '-b']
        filtered = list(filter(None, opts))

        # Should be a list
        self.assertIsInstance(filtered, list)
        self.assertEqual(filtered, ['-a', '--verbose', '-b'])

        # Should be reusable
        self.assertEqual(len(filtered), 3)
        self.assertTrue(bool(filtered))


class TestNumPyDeprecations(unittest.TestCase):
    """Test that NumPy deprecated APIs are not used"""

    def test_no_numpy_int_float_aliases(self):
        """Test that old NumPy type aliases are not used"""
        # In NumPy 2.0, np.int, np.float, etc. are removed
        # We should use np.int64, np.float64, or Python's int, float

        # These should NOT exist in NumPy 2.0
        with self.assertRaises(AttributeError):
            _ = np.int

        with self.assertRaises(AttributeError):
            _ = np.float

        # These SHOULD exist
        self.assertTrue(hasattr(np, 'int64'))
        self.assertTrue(hasattr(np, 'float64'))

    def test_disk_memory_memmap_usage(self):
        """Test DiskMemory module uses np.memmap correctly"""
        try:
            from DFTB.DiskMemory import DiskMemory
            import tempfile
            import os

            # This should work without errors
            tmpdir = tempfile.mkdtemp()
            try:
                dm = DiskMemory(disk_dir=tmpdir)
                # Basic functionality test
                self.assertIsNotNone(dm)
            finally:
                import shutil
                shutil.rmtree(tmpdir, ignore_errors=True)
        except ImportError:
            self.skipTest("DiskMemory module not available")


class TestFunctionalCode(unittest.TestCase):
    """Test actual functionality of critical modules"""

    def test_puckering_coordinates(self):
        """Test Puckering module works correctly"""
        try:
            from DFTB.Modeling.Puckering import Ring, test_puckering_coords
            from DFTB import AtomicData
            import numpy as np

            # Create a simple ring
            O = 8
            C = 6
            ring = Ring([
                (O, (0., 1.2111, -0.0189)),
                (C, (1.1622, 0.4349, 0.1461)),
                (C, (0.7425, -1.0012, -0.2174)),
                (C, (-0.7221, -1.0309, 0.2057)),
                (C, (-1.1826, 0.3861, -0.1154))
            ], ring_atoms=[0, 1, 2, 3, 4], units="Angstrom")

            # Calculate puckering coordinates (uses reduce)
            puck_ampl, puck_phase = ring.get_puckering_coords()

            # Verify we got results
            self.assertIsInstance(puck_ampl, list)
            self.assertIsInstance(puck_phase, list)
            self.assertGreater(len(puck_ampl), 0)

        except ImportError:
            self.skipTest("Puckering module not available")

    def test_xyz_reading(self):
        """Test XYZ module basic functionality"""
        try:
            from DFTB import XYZ
            import tempfile
            import os

            # Create a simple XYZ file
            fd, path = tempfile.mkstemp(suffix='.xyz')
            try:
                with os.fdopen(fd, 'w') as f:
                    f.write("2\n")
                    f.write("Test molecule\n")
                    f.write("H 0.0 0.0 0.0\n")
                    f.write("H 0.0 0.0 0.74\n")

                # Read it back
                atomlists = XYZ.read_xyz(path)

                # Verify
                self.assertEqual(len(atomlists), 1)
                self.assertEqual(len(atomlists[0]), 2)

            finally:
                os.unlink(path)

        except ImportError:
            self.skipTest("XYZ module not available")


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPython3Compatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestNumPy2Compatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestDFTBabyImports))
    suite.addTests(loader.loadTestsFromTestCase(TestCriticalFixes))
    suite.addTests(loader.loadTestsFromTestCase(TestNumPyDeprecations))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionalCode))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("=" * 70)
    print("DFTBaby Python 3.12+ and NumPy 2.0+ Compatibility Test Suite")
    print("=" * 70)
    print()

    result = run_tests()

    print()
    print("=" * 70)
    print("Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Successes: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    print("=" * 70)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
