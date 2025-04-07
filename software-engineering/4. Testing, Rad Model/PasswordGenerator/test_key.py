import unittest
from secure_key import PasswordGenerator
import string

class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        gen = PasswordGenerator()
        password = gen.get()
        expected_length = gen.num_upper + gen.num_lower + gen.num_digits + gen.num_symbols
        self.assertEqual(len(password), expected_length)

    def test_character_inclusion(self):
        gen = PasswordGenerator(num_upper=2, num_lower=2, num_digits=1, num_symbols=1)
        password = gen.get()

        upper_count = sum(1 for c in password if c in string.ascii_uppercase)
        lower_count = sum(1 for c in password if c in string.ascii_lowercase)
        digit_count = sum(1 for c in password if c in string.digits)
        symbol_count = sum(1 for c in password if c in string.punctuation)

        self.assertEqual(upper_count, 2)
        self.assertEqual(lower_count, 2)
        self.assertEqual(digit_count, 1)
        self.assertEqual(symbol_count, 1)

    def test_invalid_value_raises_error(self):
        with self.assertRaises(ValueError):
            PasswordGenerator(num_upper=0)