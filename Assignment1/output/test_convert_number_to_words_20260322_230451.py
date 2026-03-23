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
        """TC001: 测试 convert_small_number 函数，输入 0，覆盖正常情况。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc002(self):
        """TC002: 测试 convert_small_number 函数，输入 5，覆盖正常情况。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc003(self):
        """TC003: 测试 convert_small_number 函数，输入 10，覆盖正常情况。"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 函数，输入 15，覆盖正常情况。"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc005(self):
        """TC005: 测试 convert_small_number 函数，输入 20，覆盖正常情况。"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 函数，输入 25，覆盖正常情况。"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 函数，输入 -1，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc008(self):
        """TC008: 测试 convert_small_number 函数，输入 123，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc009(self):
        """TC009: 测试 convert_number 函数，输入 0，覆盖正常情况。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc010(self):
        """TC010: 测试 convert_number 函数，输入 1，覆盖正常情况。"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc011(self):
        """TC011: 测试 convert_number 函数，输入 100，覆盖正常情况。"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc012(self):
        """TC012: 测试 convert_number 函数，输入 -100，覆盖正常情况。"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc013(self):
        """TC013: 测试 convert_number 函数，输入 123456789012345，覆盖正常情况。"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc014(self):
        """TC014: 测试 convert_number 函数，输入 123456789012345，使用 long 系统，覆盖正常情况。"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc015(self):
        """TC015: 测试 convert_number 函数，输入 123456789012345，使用 indian 系统，覆盖正常情况。"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc016(self):
        """TC016: 测试 convert_number 函数，输入 1000000000000000000，使用 short 系统，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc017(self):
        """TC017: 测试 convert_number 函数，输入 1000000000000000000000，使用 long 系统，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc018(self):
        """TC018: 测试 convert_number 函数，输入 10000000000000000000，使用 indian 系统，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc019(self):
        """TC019: 测试 max_value 函数，输入 'short'，覆盖正常情况。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc020(self):
        """TC020: 测试 max_value 函数，输入 'long'，覆盖正常情况。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc021(self):
        """TC021: 测试 max_value 函数，输入 'indian'，覆盖正常情况。"""
        result = NumberingSystem.max_value('indian')
        assert result == 99999999999999999999

    def test_tc022(self):
        """TC022: 测试 max_value 函数，输入无效的系统，覆盖异常情况。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')
