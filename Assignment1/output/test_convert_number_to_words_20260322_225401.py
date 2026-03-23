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
        """TC001: 测试 convert_small_number 函数，输入为 0，覆盖正常情况。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc002(self):
        """TC002: 测试 convert_small_number 函数，输入为 5，覆盖正常情况。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc003(self):
        """TC003: 测试 convert_small_number 函数，输入为 10，覆盖十的情况。"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 函数，输入为 -1，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc005(self):
        """TC005: 测试 convert_small_number 函数，输入为 123，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc006(self):
        """TC006: 测试 convert_number 函数，输入为 0，覆盖正常情况。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc007(self):
        """TC007: 测试 convert_number 函数，输入为 1，覆盖正常情况。"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc008(self):
        """TC008: 测试 convert_number 函数，输入为 -100，覆盖负数情况。"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc009(self):
        """TC009: 测试 convert_number 函数，输入为 100，覆盖整百情况。"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc010(self):
        """TC010: 测试 convert_number 函数，输入为 123456789012345，覆盖正常情况。"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc011(self):
        """TC011: 测试 convert_number 函数，输入为 10**18，覆盖异常情况。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc012(self):
        """TC012: 测试 max_value 函数，输入为 'short'，覆盖正常情况。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc013(self):
        """TC013: 测试 max_value 函数，输入为 'long'，覆盖正常情况。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc014(self):
        """TC014: 测试 max_value 函数，输入为 'indian'，覆盖正常情况。"""
        result = NumberingSystem.max_value('indian')
        assert result == 99999999999999999999

    def test_tc015(self):
        """TC015: 测试 max_value 函数，输入为无效的系统，覆盖异常情况。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')
