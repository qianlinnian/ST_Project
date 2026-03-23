import sys
import os
import pytest

# 添加目标模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import *


class TestNumberToWords:
    """测试数字转单词功能"""

    # 测试 NumberingSystem.max_value
    def test_tc001_max_value_short(self):
        """测试 NumberingSystem.max_value 对于 short 系统"""
        result = NumberingSystem.max_value("short")
        expected = 999999999999999999
        assert result == expected

    def test_tc002_max_value_long(self):
        """测试 NumberingSystem.max_value 对于 long 系统"""
        result = NumberingSystem.max_value("long")
        expected = 999999999999999999999
        assert result == expected

    def test_tc003_max_value_indian(self):
        """测试 NumberingSystem.max_value 对于 indian 系统"""
        result = NumberingSystem.max_value("indian")
        expected = 9999999999999999999
        assert result == expected

    # 测试 convert_small_number
    def test_tc004_convert_small_number_negative(self):
        """测试 convert_small_number 对于负数"""
        with pytest.raises(ValueError) as exc_info:
            convert_small_number(-1)
        assert "This function only accepts non-negative integers" in str(exc_info.value)

    def test_tc005_convert_small_number_large(self):
        """测试 convert_small_number 对于大于等于100的数"""
        with pytest.raises(ValueError) as exc_info:
            convert_small_number(123)
        assert "This function only converts numbers less than 100" in str(exc_info.value)

    def test_tc006_convert_small_number_zero(self):
        """测试 convert_small_number 对于数字0"""
        result = convert_small_number(0)
        expected = "zero"
        assert result == expected

    def test_tc007_convert_small_number_single_digit(self):
        """测试 convert_small_number 对于个位数5"""
        result = convert_small_number(5)
        expected = "five"
        assert result == expected

    def test_tc008_convert_small_number_ten(self):
        """测试 convert_small_number 对于数字10"""
        result = convert_small_number(10)
        expected = "ten"
        assert result == expected

    def test_tc009_convert_small_number_teen(self):
        """测试 convert_small_number 对于数字15"""
        result = convert_small_number(15)
        expected = "fifteen"
        assert result == expected

    def test_tc010_convert_small_number_twenty(self):
        """测试 convert_small_number 对于数字20"""
        result = convert_small_number(20)
        expected = "twenty"
        assert result == expected

    def test_tc011_convert_small_number_twenty_five(self):
        """测试 convert_small_number 对于数字25"""
        result = convert_small_number(25)
        expected = "twenty-five"
        assert result == expected

    # 测试 convert_number
    def test_tc012_convert_number_zero_short(self):
        """测试 convert_number 对于数字0，默认short系统"""
        result = convert_number(0)
        expected = "zero"
        assert result == expected

    def test_tc013_convert_number_one_short(self):
        """测试 convert_number 对于数字1，默认short系统"""
        result = convert_number(1)
        expected = "one"
        assert result == expected

    def test_tc014_convert_number_negative_100_short(self):
        """测试 convert_number 对于负数-100，默认short系统"""
        result = convert_number(-100)
        expected = "negative one hundred"
        assert result == expected

    def test_tc015_convert_number_100_short(self):
        """测试 convert_number 对于数字100，默认short系统"""
        result = convert_number(100)
        expected = "one hundred"
        assert result == expected

    def test_tc016_convert_number_1000_short(self):
        """测试 convert_number 对于数字1000，默认short系统"""
        result = convert_number(1000)
        expected = "one thousand"
        assert result == expected

    def test_tc017_convert_number_123456_short(self):
        """测试 convert_number 对于数字123456，默认short系统"""
        result = convert_number(123456)
        expected = "one hundred twenty-three thousand four hundred fifty-six"
        assert result == expected

    def test_tc018_convert_number_large_short(self):
        """测试 convert_number 对于数字123456789012345，默认short系统"""
        result = convert_number(123456789012345)
        expected = (
            "one hundred twenty-three trillion four hundred fifty-six billion "
            "seven hundred eighty-nine million twelve thousand three hundred forty-five"
        )
        assert result == expected

    def test_tc019_convert_number_max_short(self):
        """测试 convert_number 对于short系统最大值999999999999999999"""
        result = convert_number(999999999999999999, "short")
        expected = (
            "nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion "
            "nine hundred ninety-nine billion nine hundred ninety-nine million "
            "nine hundred ninety-nine thousand nine hundred ninety-nine"
        )
        assert result == expected

    def test_tc020_convert_number_exceed_max_short(self):
        """测试 convert_number 对于short系统超最大值1000000000000000000"""
        with pytest.raises(ValueError) as exc_info:
            convert_number(1000000000000000000, "short")
        assert "Input number is too large" in str(exc_info.value)

    def test_tc021_convert_number_long_system(self):
        """测试 convert_number 对于数字123456789012345，long系统"""
        result = convert_number(123456789012345, "long")
        expected = (
            "one hundred twenty-three thousand four hundred fifty-six milliard "
            "seven hundred eighty-nine million twelve thousand three hundred forty-five"
        )
        assert result == expected

    def test_tc022_convert_number_max_long(self):
        """测试 convert_number 对于long系统最大值999999999999999999999"""
        result = convert_number(999999999999999999999, "long")
        expected = (
            "nine hundred ninety-nine thousand nine hundred ninety-nine milliard "
            "nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine"
        )
        assert result == expected

    def test_tc023_convert_number_exceed_max_long(self):
        """测试 convert_number 对于long系统超最大值1000000000000000000000"""
        with pytest.raises(ValueError) as exc_info:
            convert_number(1000000000000000000000, "long")
        assert "Input number is too large" in str(exc_info.value)

    def test_tc024_convert_number_indian_system(self):
        """测试 convert_number 对于数字123456789012345，indian系统"""
        result = convert_number(123456789012345, "indian")
        expected = (
            "one crore crore twenty-three lakh crore forty-five thousand six hundred "
            "seventy-eight crore ninety lakh twelve thousand three hundred forty-five"
        )
        assert result == expected

    def test_tc025_convert_number_max_indian(self):
        """测试 convert_number 对于indian系统最大值9999999999999999999"""
        result = convert_number(9999999999999999999, "indian")
        expected = (
            "nine hundred ninety-nine crore crore ninety-nine lakh crore "
            "ninety-nine thousand nine hundred ninety-nine crore ninety-nine lakh "
            "ninety-nine thousand nine hundred ninety-nine"
        )
        assert result == expected

    def test_tc026_convert_number_exceed_max_indian(self):
        """测试 convert_number 对于indian系统超最大值10000000000000000000"""
        with pytest.raises(ValueError) as exc_info:
            convert_number(10000000000000000000, "indian")
        assert "Input number is too large" in str(exc_info.value)

    def test_tc027_convert_number_invalid_system(self):
        """测试 convert_number 对于无效系统"""
        with pytest.raises(KeyError) as exc_info:
            convert_number(100, "invalid")
        assert "'INVALID'" in str(exc_info.value)