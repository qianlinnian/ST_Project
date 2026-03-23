import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import convert_number, NumberingSystem


class TestConvertNumberToWords:
    def test_convert_zero(self):
        assert convert_number(0) == "zero"

    def test_convert_positive_number(self):
        assert convert_number(5) == "five"

    def test_convert_ten(self):
        assert convert_number(10) == "ten"

    def test_convert_negative_number(self):
        with pytest.raises(ValueError):
            convert_number(-5)

    def test_convert_over_100(self):
        with pytest.raises(ValueError):
            convert_number(100)

    def test_convert_short_system(self):
        assert convert_number(123456789012345, "short") == (
            "one hundred twenty-three trillion four hundred fifty-six billion "
            "seven hundred eighty-nine million twelve thousand three hundred forty-five"
        )

    def test_convert_long_system(self):
        assert convert_number(123456789012345, "long") == (
            "one hundred twenty-three thousand four hundred fifty-six milliard "
            "seven hundred eighty-nine million twelve thousand three hundred forty-five"
        )

    def test_convert_indian_system(self):
        assert convert_number(123456789012345, "indian") == (
            "one crore crore twenty-three lakh crore forty-five thousand "
            "six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five"
        )

    def test_convert_exceeding_short_max(self):
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, "short")

    def test_convert_exceeding_long_max(self):
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, "long")

    def test_convert_exceeding_indian_max(self):
        with pytest.raises(ValueError):
            convert_number(100000000000000000000, "indian")

    def test_max_value_short(self):
        assert NumberingSystem.max_value("short") == 999999999999999999

    def test_max_value_long(self):
        assert NumberingSystem.max_value("long") == 999999999999999999999

    def test_max_value_indian(self):
        assert NumberingSystem.max_value("indian") == 99999999999999999999

    def test_invalid_numbering_system(self):
        with pytest.raises(ValueError):
            NumberingSystem.max_value("invalid")