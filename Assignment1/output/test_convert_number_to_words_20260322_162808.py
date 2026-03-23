"""自动生成的白盒测试用例 - convert_number_to_words"""
import pytest
import sys
import os

# 将 targets 目录加入 path，以便导入被测模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import convert_small_number, convert_number, NumberingSystem, NumberWords


class TestConvertNumberToWords:
    """白盒测试类 - 由 LLM 自动生成"""

    def test_tc001(self):
        """TC001: Test convert_small_number with negative input"""
        result = convert_small_number(-1)
        assert result == 'This function only accepts non-negative integers'

    def test_tc002(self):
        """TC002: Test convert_small_number with number >= 100"""
        result = convert_small_number(100)
        assert result == 'This function only converts numbers less than 100'

    def test_tc003(self):
        """TC003: Test convert_small_number with zero"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc004(self):
        """TC004: Test convert_small_number with single digit (1-9)"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc005(self):
        """TC005: Test convert_small_number with ten"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc006(self):
        """TC006: Test convert_small_number with teen number (11-19)"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc007(self):
        """TC007: Test convert_small_number with tens number and zero ones (20,30,...,90)"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc008(self):
        """TC008: Test convert_small_number with tens number and non-zero ones (21-99)"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc009(self):
        """TC009: Test NumberingSystem.max_value with 'short' system"""
        result = NumberingSystem.max_value('short')
        assert result == '999999999999999999'

    def test_tc010(self):
        """TC010: Test NumberingSystem.max_value with 'long' system"""
        result = NumberingSystem.max_value('long')
        assert result == '999999999999999999999'

    def test_tc011(self):
        """TC011: Test NumberingSystem.max_value with 'indian' system"""
        result = NumberingSystem.max_value('indian')
        assert result == '9999999999999999999'

    def test_tc012(self):
        """TC012: Test NumberingSystem.max_value with invalid system"""
        result = NumberingSystem.max_value('invalid')
        assert result == 'Invalid numbering system'

    def test_tc013(self):
        """TC013: Test convert_number with zero"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc014(self):
        """TC014: Test convert_number with positive single digit"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc015(self):
        """TC015: Test convert_number with negative number"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc016(self):
        """TC016: Test convert_number with number 123 to cover recursion and tens"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'

    def test_tc017(self):
        """TC017: Test convert_number with large number in short system"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc018(self):
        """TC018: Test convert_number with large number in long system"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc019(self):
        """TC019: Test convert_number with number in indian system"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc020(self):
        """TC020: Test convert_number with max value for short system"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc021(self):
        """TC021: Test convert_number with number exceeding max value for short system"""
        result = convert_number(1000000000000000000, 'short')
        assert result == 'Input number is too large'

    def test_tc022(self):
        """TC022: Test convert_number with number exceeding max value for long system"""
        result = convert_number(1000000000000000000000, 'long')
        assert result == 'Input number is too large'

    def test_tc023(self):
        """TC023: Test convert_number with number exceeding max value for indian system"""
        result = convert_number(10000000000000000000, 'indian')
        assert result == 'Input number is too large'

    def test_tc024(self):
        """TC024: Test convert_number with number where digit_group >= 100 requiring recursion"""
        result = convert_number(200000000000000000, 'short')
        assert result == 'two hundred quadrillion'

    def test_tc025(self):
        """TC025: Test convert_number with number where some digit_group == 0 in loop"""
        result = convert_number(1000, 'short')
        assert result == 'one thousand'

    def test_tc_sup_001(self):
        """TC_SUP_001: 通过直接运行脚本覆盖 __main__ 块中的代码行（201, 203, 205）和分支（L200 → L201）。"""
        result = convert_small_number(True)
        assert result == "convert_number(123456789) = 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'"

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 方法传入无效的枚举名时抛出 ValueError。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('INVALID')

    def test_tc_sup_002(self):
        """TC_SUP_002: 执行脚本主块，覆盖 import doctest、doctest.testmod() 和打印语句。"""
        result = convert_small_number()
        assert result == "convert_number(123456789) = 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'"
