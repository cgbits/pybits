import unittest

from pybits import listbits


class TestListbitsModule(unittest.TestCase):
    def test_is_subset_strings_true(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["foobar"]

        result = listbits.is_subset(subset, superset)

        self.assertTrue(result)

    def test_is_subset_strings_false(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["barfoo"]

        result = listbits.is_subset(subset, superset)

        self.assertFalse(result)

    def test_is_subset_lists_true(self):
        superset = [["foo"], ["bar"], ["foobar", "barfoo"]]

        subset = [["foobar"]]

        result = listbits.is_subset(subset, superset)

        self.assertTrue(result)

    def test_is_equal_strings_true(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["foo", "bar", "foobar"]

        result = listbits.is_equal(subset, superset)

        self.assertTrue(result)

    def test_is_equal_strings_false(self):
        superset = ["foo", "bar", "foobar"]

        subset = ["foo", "bar", "barfoo"]

        result = listbits.is_equal(subset, superset)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
