import unittest
import re
import json
import ast
from  import apiResponse


class ReplaceArgumentTest(unittest.TestCase):

    def test_no_replacements_in_string(self):
        target_str = "Hello, World!"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, World!")

    def test_replacement_in_string(self):
        target_str = "Hello, {{name}}!"
        arguments = {"name": "Alice"}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, Alice!")

    def test_multiple_replacements_in_string(self):
        target_str = "Hello, {{user}} and {{name}}!"
        arguments = {"user": "Bob", "name": "Alice"}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, Bob and Alice!")

    def test_replacements_in_dict(self):
        target_str = '{"name": "{{name}}", "age": {{age}}}'
        arguments = {"name": "Alice", "age": 30}
        result = _replace_argument(target_str, arguments)
        expected_result = '{"name": "Alice", "age": 30}'
        self.assertEqual(result, expected_result)

    def test_replacements_in_list(self):
        target_str = "[1, 2, {{number}}, 4]"
        arguments = {"number": 3}
        result = _replace_argument(target_str, arguments)
        expected_result = "[1, 2, 3, 4]"
        self.assertEqual(result, expected_result)

    def test_no_replacements_in_list(self):
        target_str = "[1, 2, 3, 4]"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "[1, 2, 3, 4]")

    def test_invalid_argument(self):
        target_str = "Hello, {{name}}!"
        arguments = {"name": "Alice", "age": "not_a_number"}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, Alice!")

    def test_int_type(self):
        target_str = "42"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, 42)

    def test_bool_type(self):
        target_str = "True"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, True)

    def test_float_type(self):
        target_str = "3.14"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, 3.14)

    def test_nonexistent_argument(self):
        target_str = "Hello, {{unknown}}!"
        arguments = {}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, {{unknown}}!")

    def test_invalid_argument_type(self):
        target_str = "Hello, {{name}}!"
        arguments = {"name": ["Alice", "Bob"]}
        result = _replace_argument(target_str, arguments)
        self.assertEqual(result, "Hello, [Alice, Bob]!")

    def test_nested_dict(self):
        target_str = '{"user": "{{name}}", "address": {"city": "{{city}}"}}'
        arguments = {"name": "Alice", "city": "New York"}
        result = _replace_argument(target_str, arguments)
        expected_result = '{"user": "Alice", "address": {"city": "New York"}}'
        self.assertEqual(result, expected_result)

    def test_nested_list(self):
        target_str = "[1, 2, {{list}}, 4]"
        arguments = {"list": [3, 5, 7]}
        result = _replace_argument(target_str, arguments)
        expected_result = "[1, 2, [3, 5, 7], 4]"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
