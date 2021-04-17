from pybits.exceptions import (
    ComparisonError,
    ComparisonErrorInfo,
    ComparisonBaseError,
)
import unittest

from pybits import dictbits


class TestDictbitsModule(unittest.TestCase):
    def test_assert_is_subset_exception(self):
        with self.assertRaises(ComparisonErrorInfo):
            superset = {
                "name": "some_name",
                "type": "asdf",
                "children": [{"name": "foo", "type": "asdf", "children": []}],
            }

            subset = {
                "name": "some_name",
                "children": [{"name": "bar", "children": []}],
            }

            dictbits.assert_is_subset(subset, superset)

    def test_assert_is_subset_exception_depth(self):
        superset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset = {
            "name": "some_name",
            "children": [{"name": "bar", "children": []}],
        }

        result = -1

        result_excpected = 2

        try:
            dictbits.assert_is_subset(subset, superset)
        except ComparisonBaseError as e:
            result = e.depth

        self.assertEqual(result, result_excpected)

    def test_is_subset_true(self):
        superset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset = {
            "name": "some_name",
            "children": [{"name": "foo", "children": []}],
        }

        result = dictbits.is_subset(subset, superset)

        self.assertTrue(result)

    def test_is_subset_false(self):
        superset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset = {
            "name": "some_name",
            "children": [{"name": "bar", "children": []}],
        }

        result = dictbits.is_subset(subset, superset)

        self.assertFalse(result)

    def test_is_equal_true(self):
        superset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        result = dictbits.is_equal(subset, superset)

        self.assertTrue(result)

    def test_is_equal_false(self):
        superset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "bar", "type": "asdf", "children": []}],
        }

        result = dictbits.is_equal(subset, superset)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
