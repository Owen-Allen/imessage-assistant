import unittest
import argparse
from context import ArgParseWrapper

class TestArgParseWrapper(unittest.TestCase):

    def test_format_phone_number_without_prefix(self):
        self.assertEqual(ArgParseWrapper.format_phone_number('1234567890'), '+11234567890')

    def test_format_phone_number_with_prefix(self):
        self.assertEqual(ArgParseWrapper.format_phone_number('+11234567890'), '+11234567890')

    def test_validate_phone_number_valid(self):
        self.assertEqual(ArgParseWrapper.validate_phone_number('+11234567890'), '+11234567890')

    def test_validate_phone_number_invalid(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            ArgParseWrapper.validate_phone_number('+123')

    def test_format_and_validate_phone_number(self):
        self.assertEqual(ArgParseWrapper.format_and_validate_phone_number('1234567890'), '+11234567890')

    def test_format_and_validate_phone_number_invalid(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            ArgParseWrapper.format_and_validate_phone_number('+123')

if __name__ == '__main__':
    unittest.main()