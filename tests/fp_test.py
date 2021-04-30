import unittest

from pybits import fp


class TestFpModule(unittest.TestCase):
    def test_curry(self):
        def test_function(a: str, b: str, c: str) -> str:
            return a + b + c

        curried_test_function = fp.curry(test_function)

        call_1 = curried_test_function("Hello")

        self.assertTrue(callable(call_1))

        call_2 = call_1(" from the")

        self.assertTrue(callable(call_2))

        result = call_2(" other side")
        result_expected = "Hello from the other side"

        self.assertEqual(result, result_expected)


if __name__ == "__main__":
    unittest.main()
