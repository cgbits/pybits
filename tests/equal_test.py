import unittest

from typing import Any, Dict

from pybits.equal import (
    dict_is_equal,
    list_is_equal,
)


class TestEqualModule(unittest.TestCase):
    def test_dict_is_equal_true(self):
        superset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        result = dict_is_equal(subset, superset)

        self.assertTrue(result)

    def test_dict_is_equal_false(self):
        superset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "foo", "type": "asdf", "children": []}],
        }

        subset: Dict[str, Any] = {
            "name": "some_name",
            "type": "asdf",
            "children": [{"name": "bar", "type": "asdf", "children": []}],
        }

        result = dict_is_equal(subset, superset)

        self.assertFalse(result)

    def test_list_is_equal_strings_true(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["foo", "bar", "foobar"]

        result = list_is_equal(subset, superset)

        self.assertTrue(result)

    def test_let_is_equal_strings_false(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["foo", "bar", "barfoo"]

        result = list_is_equal(subset, superset)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
