import unittest

from typing import Dict, List, Any

from pybits.subset import (
    dict_assert_is_subset,
    dict_is_subset,
    list_is_subset,
)
from pybits.exceptions import (
    ComparisonBaseError,
    ComparisonErrorInfo,
)


class TestSubsetModule(unittest.TestCase):
    def test_dict_assert_is_subset_exception(self):
        with self.assertRaises(ComparisonErrorInfo):
            superset: Dict[str, Any] = {
                "name": "some_name",
                "type": "asdf",
                "children": [{"name": "foo", "type": "asdf", "children": []}],
            }

            subset: Dict[str, Any] = {
                "name": "some_name",
                "children": [{"name": "bar", "children": []}],
            }

            dict_assert_is_subset(subset, superset)

    def test_dict_assert_is_subset_exception_depth(self):
        superset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset: Dict[str, Any] = {
            "name": "some_name",
            "children": [{"name": "bar", "children": []}],
        }

        result = -1

        result_excpected = 2

        try:
            dict_assert_is_subset(subset, superset)
        except ComparisonBaseError as e:
            result = e.depth

        self.assertEqual(result, result_excpected)

    def test_dict_is_subset_true(self):
        superset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset: Dict[str, Any] = {
            "name": "some_name",
            "children": [{"name": "foo", "children": []}],
        }

        result = dict_is_subset(subset, superset)

        self.assertTrue(result)

    def test_dict_is_subset_false(self):
        superset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset: Dict[str, Any] = {
            "name": "some_name",
            "children": [{"name": "bar", "children": []}],
        }

        result = dict_is_subset(subset, superset)

        self.assertFalse(result)

    def test_list_is_subset_strings_true(self):
        superset: List[str] = ["foo", "bar", "foobar"]

        subset: List[str] = ["foobar"]

        result = list_is_subset(subset, superset)

        self.assertTrue(result)

    def test_list_is_subset_strings_false(self):
        superset: List[str] = ["foo", "bar", "foobar"]

        subset: List[str] = ["barfoo"]

        result = list_is_subset(subset, superset)

        self.assertFalse(result)

    def test_list_is_subset_lists_true(self):
        superset: List[List[str]] = [["foo"], ["bar"], ["foobar", "barfoo"]]

        subset: List[List[str]] = [["foobar"]]

        result = list_is_subset(subset, superset)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
