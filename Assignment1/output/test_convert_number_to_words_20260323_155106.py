import pytest
import sys
import os

# Adjust the path to import the target module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import NumberingSystem, convert_small_number, convert_number


class TestNumberToWords:
    # Test cases for NumberingSystem.max_value
    @pytest.mark.parametrize(
        "test_id, description, system, expected_output",
        [
            (
                "TC_MAX_VALUE_001",
                "测试 NumberingSystem.max_value 函数，输入 'short' 系统。",
                "short",
                999999999999999999,
            ),
            (
                "TC_MAX_VALUE_002",
                "测试 NumberingSystem.max_value 函数，输入 'long' 系统。",
                "long",
                999999999999999999999,
            ),
            (
                "TC_MAX_VALUE_003",
                "测试 NumberingSystem.max_value 函数，输入 'indian' 系统。",
                "indian",
                9999999999999999999,
            ),
        ],
    )
    def test_max_value_valid_systems(self, test_id, description, system, expected_output):
        """
        Tests NumberingSystem.max_value with valid numbering systems.
        """
        assert NumberingSystem.max_value(system) == expected_output

    def test_TC_MAX_VALUE_004_invalid_system(self):
        """
        TC_MAX_VALUE_004: 测试 NumberingSystem.max_value 函数，输入无效系统，期望抛出 ValueError。
        """
        with pytest.raises(ValueError, match="Invalid numbering system"):
            NumberingSystem.max_value("invalid")

    # Test cases for convert_small_number
    def test_TC_SMALL_001_negative_input(self):
        """
        TC_SMALL_001: 测试 convert_small_number 函数，输入负数，期望抛出 ValueError。
        """
        with pytest.raises(ValueError, match="This function only accepts non-negative integers"):
            convert_small_number(-1)

    def test_TC_SMALL_002_large_input(self):
        """
        TC_SMALL_002: 测试 convert_small_number 函数，输入大于等于 100 的数，期望抛出 ValueError。
        """
        with pytest.raises(ValueError, match="This function only converts numbers less than 100"):
            convert_small_number(100)

    @pytest.mark.parametrize(
        "test_id, description, num, expected_output",
        [
            ("TC_SMALL_003", "测试 convert_small_number 函数，输入 0。", 0, "zero"),
            ("TC_SMALL_004", "测试 convert_small_number 函数，输入个位数（例如 5）。", 5, "five"),
            ("TC_SMALL_005", "测试 convert_small_number 函数，输入 10-19 之间的数（例如 10）。", 10, "ten"),
            ("TC_SMALL_006", "测试 convert_small_number 函数，输入 10-19 之间的数（例如 15）。", 15, "fifteen"),
            ("TC_SMALL_007", "测试 convert_small_number 函数，输入 20-99 之间且个位为 0 的数（例如 20）。", 20, "twenty"),
            ("TC_SMALL_008", "测试 convert_small_number 函数，输入 20-99 之间且个位不为 0 的数（例如 25）。", 25, "twenty-five"),
        ],
    )
    def test_convert_small_number_valid_inputs(self, test_id, description, num, expected_output):
        """
        Tests convert_small_number with various valid inputs.
        """
        assert convert_small_number(num) == expected_output

    # Test cases for convert_number
    @pytest.mark.parametrize(
        "test_id, description, num, system, expected_output",
        [
            ("TC_CONVERT_001", "测试 convert_number 函数，输入 0。", 0, "short", "zero"),
            ("TC_CONVERT_002", "测试 convert_number 函数，输入个位数正数（例如 1）。", 1, "short", "one"),
            ("TC_CONVERT_003", "测试 convert_number 函数，输入个位数负数（例如 -1）。", -1, "short", "negative one"),
            ("TC_CONVERT_004", "测试 convert_number 函数，输入两位数（例如 99）。", 99, "short", "ninety-nine"),
            ("TC_CONVERT_005", "测试 convert_number 函数，输入使用单位词且无余数的数（例如 100）。", 100, "short", "one hundred"),
            ("TC_CONVERT_006", "测试 convert_number 函数，输入使用单位词且有余数的数（例如 123）。", 123, "short", "one hundred twenty-three"),
            ("TC_CONVERT_007", "测试 convert_number 函数，输入需要递归调用处理数字组的数（例如 123456）。", 123456, "short", "one hundred twenty-three thousand four hundred fifty-six"),
            (
                "TC_CONVERT_008",
                "测试 convert_number 函数，输入 'short' 系统的最大支持值。",
                999999999999999999,
                "short",
                "nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine",
            ),
            (
                "TC_CONVERT_010",
                "测试 convert_number 函数，输入 'long' 系统的最大支持值。",
                999999999999999999999,
                "long",
                "nine hundred ninety-nine thousand nine hundred ninety-nine milliard nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine",
            ),
            (
                "TC_CONVERT_012",
                "测试 convert_number 函数，输入 'indian' 系统的最大支持值。",
                9999999999999999999,
                "indian",
                "nine hundred ninety-nine crore crore ninety-nine lakh crore ninety-nine crore ninety-nine lakh ninety-nine thousand nine hundred ninety-nine",
            ),
            (
                "TC_CONVERT_014",
                "测试 convert_number 函数，输入一个大数，使用 'short' 系统。",
                123456789012345,
                "short",
                "one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five",
            ),
            (
                "TC_CONVERT_015",
                "测试 convert_number 函数，输入一个大数，使用 'long' 系统。",
                123456789012345,
                "long",
                "one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five",
            ),
            (
                "TC_CONVERT_016",
                "测试 convert_number 函数，输入一个大数，使用 'indian' 系统。",
                123456789012345,
                "indian",
                "one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five",
            ),
        ],
    )
    def test_convert_number_valid_inputs(self, test_id, description, num, system, expected_output):
        """
        Tests convert_number with various valid inputs across different systems.
        """
        assert convert_number(num, system) == expected_output

    @pytest.mark.parametrize(
        "test_id, description, num, system, expected_error_message",
        [
            (
                "TC_CONVERT_009",
                "测试 convert_number 函数，输入超过 'short' 系统最大值的数，期望抛出 ValueError。",
                1000000000000000000,
                "short",
                "Input number is too large",
            ),
            (
                "TC_CONVERT_011",
                "测试 convert_number 函数，输入超过 'long' 系统最大值的数，期望抛出 ValueError。",
                1000000000000000000000,
                "long",
                "Input number is too large",
            ),
            (
                "TC_CONVERT_013",
                "测试 convert_number 函数，输入超过 'indian' 系统最大值的数，期望抛出 ValueError。",
                10000000000000000000,
                "indian",
                "Input number is too large",
            ),
        ],
    )
    def test_convert_number_too_large_input(self, test_id, description, num, system, expected_error_message):
        """
        Tests convert_number with inputs exceeding the maximum supported value for the given system.
        """
        with pytest.raises(ValueError, match=expected_error_message):
            convert_number(num, system)