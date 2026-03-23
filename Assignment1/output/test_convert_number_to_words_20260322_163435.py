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
        """TC001: 测试 NumberingSystem.max_value 方法，使用 'short' 计数系统。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc002(self):
        """TC002: 测试 NumberingSystem.max_value 方法，使用 'long' 计数系统。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc003(self):
        """TC003: 测试 NumberingSystem.max_value 方法，使用 'indian' 计数系统。"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc004(self):
        """TC004: 测试 NumberingSystem.max_value 方法，使用无效的计数系统（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc005(self):
        """TC005: 测试 convert_small_number 函数，输入为 0。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 函数，输入为个位数（例如 5）。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 函数，输入为 10。"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc008(self):
        """TC008: 测试 convert_small_number 函数，输入为十几的数字（例如 15）。"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc009(self):
        """TC009: 测试 convert_small_number 函数，输入为整十数（例如 20）。"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc010(self):
        """TC010: 测试 convert_small_number 函数，输入为两位数（例如 25）。"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc011(self):
        """TC011: 测试 convert_small_number 函数，输入为最大的两位数（99）。"""
        result = convert_small_number(99)
        assert result == 'ninety-nine'

    def test_tc012(self):
        """TC012: 测试 convert_small_number 函数，输入为负数（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc013(self):
        """TC013: 测试 convert_small_number 函数，输入为大于等于 100 的数字（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc014(self):
        """TC014: 测试 convert_number 函数，输入为 0。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc015(self):
        """TC015: 测试 convert_number 函数，输入为 1。"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc016(self):
        """TC016: 测试 convert_number 函数，输入为 99。"""
        result = convert_number(99, 'short')
        assert result == 'ninety-nine'

    def test_tc017(self):
        """TC017: 测试 convert_number 函数，输入为 100。"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc018(self):
        """TC018: 测试 convert_number 函数，输入为 123。"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'

    def test_tc019(self):
        """TC019: 测试 convert_number 函数，输入为 1000。"""
        result = convert_number(1000, 'short')
        assert result == 'one thousand'

    def test_tc020(self):
        """TC020: 测试 convert_number 函数，输入为 123456 (包含递归调用)。"""
        result = convert_number(123456, 'short')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six'

    def test_tc021(self):
        """TC021: 测试 convert_number 函数，输入为 -1 (负数)。"""
        result = convert_number(-1, 'short')
        assert result == 'negative one'

    def test_tc022(self):
        """TC022: 测试 convert_number 函数，输入为 -100 (负数)。"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc023(self):
        """TC023: 测试 convert_number 函数，输入为 'short' 系统的最大支持值。"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc024(self):
        """TC024: 测试 convert_number 函数，输入值超过 'short' 系统的最大支持值（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc025(self):
        """TC025: 测试 convert_number 函数，输入为 'long' 系统的最大支持值。"""
        result = convert_number(999999999999999999999, 'long')
        assert result == 'nine hundred ninety-nine billiard nine hundred ninety-nine milliard nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc026(self):
        """TC026: 测试 convert_number 函数，输入值超过 'long' 系统的最大支持值（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc027(self):
        """TC027: 测试 convert_number 函数，输入为 'indian' 系统的最大支持值。"""
        result = convert_number(9999999999999999999, 'indian')
        assert result == 'nine crore crore ninety-nine lakh crore ninety-nine crore ninety-nine lakh ninety-nine thousand nine hundred ninety-nine'

    def test_tc028(self):
        """TC028: 测试 convert_number 函数，输入值超过 'indian' 系统的最大支持值（应抛出 ValueError）。"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc029(self):
        """TC029: 测试 convert_number 函数，使用 'short' 系统转换大数字（doctest 示例）。"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc030(self):
        """TC030: 测试 convert_number 函数，使用 'long' 系统转换大数字（doctest 示例）。"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc031(self):
        """TC031: 测试 convert_number 函数，使用 'indian' 系统转换大数字（doctest 示例）。"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc032(self):
        """TC032: 测试 convert_number 函数，输入为正好一百万 ('short')。"""
        result = convert_number(1000000, 'short')
        assert result == 'one million'

    def test_tc033(self):
        """TC033: 测试 convert_number 函数，输入为正好十亿 ('short')。"""
        result = convert_number(1000000000, 'short')
        assert result == 'one billion'

    def test_tc034(self):
        """TC034: 测试 convert_number 函数，输入为正好一万亿 ('short')。"""
        result = convert_number(1000000000000, 'short')
        assert result == 'one trillion'

    def test_tc035(self):
        """TC035: 测试 convert_number 函数，输入为正好一千万亿 ('short')。"""
        result = convert_number(1000000000000000, 'short')
        assert result == 'one quadrillion'

    def test_tc036(self):
        """TC036: 测试 convert_number 函数，输入为正好一千兆 ('long')。"""
        result = convert_number(1000000000000000, 'long')
        assert result == 'one billiard'

    def test_tc037(self):
        """TC037: 测试 convert_number 函数，输入为正好十亿 ('long')。"""
        result = convert_number(1000000000, 'long')
        assert result == 'one milliard'

    def test_tc038(self):
        """TC038: 测试 convert_number 函数，输入为正好一千万 ('indian')。"""
        result = convert_number(10000000, 'indian')
        assert result == 'one crore'

    def test_tc039(self):
        """TC039: 测试 convert_number 函数，输入为正好十万 ('indian')。"""
        result = convert_number(100000, 'indian')
        assert result == 'one lakh'

    def test_tc040(self):
        """TC040: 测试 convert_number 函数，输入为正好一万亿 ('indian')。"""
        result = convert_number(1000000000000, 'indian')
        assert result == 'one lakh crore'

    def test_tc041(self):
        """TC041: 测试 convert_number 函数，输入为正好一千万亿 ('indian')。"""
        result = convert_number(100000000000000, 'indian')
        assert result == 'one crore crore'

    def test_tc042(self):
        """TC042: 测试 convert_number 函数，输入数字中间包含零组（例如 1,000,005）。"""
        result = convert_number(1000005, 'short')
        assert result == 'one million five'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 方法，传入一个无效的数字系统名称，以覆盖默认的 case 分支并触发 ValueError。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid_system')

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 函数，传入一个无效的编号系统名称，以覆盖默认的 `case _` 分支并抛出 ValueError。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('nonexistent')
