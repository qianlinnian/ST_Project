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
        """TC001: 测试 convert_small_number 函数：负数输入，覆盖 L121 分支 True"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc002(self):
        """TC002: 测试 convert_small_number 函数：大于等于100的输入，覆盖 L121 分支 False，L123 分支 True"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc003(self):
        """TC003: 测试 convert_small_number 函数：输入0，覆盖 L121 分支 False，L123 分支 False，L126 分支 True，复合条件 L127 中第一个子条件为 False"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 函数：输入5（个位数），覆盖 L121 分支 False，L123 分支 False，L126 分支 True，复合条件 L127 中第一个子条件为 True"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc005(self):
        """TC005: 测试 convert_small_number 函数：输入10（十位数，且tens==1），覆盖 L121 分支 False，L123 分支 False，L126 分支 False，L128 分支 True"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 函数：输入15（十几），覆盖 L121 分支 False，L123 分支 False，L126 分支 False，L128 分支 True"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 函数：输入20（几十，且个位为0），覆盖 L121 分支 False，L123 分支 False，L126 分支 False，L128 分支 False"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc008(self):
        """TC008: 测试 convert_small_number 函数：输入25（几十几），覆盖 L121 分支 False，L123 分支 False，L126 分支 False，L128 分支 False"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc009(self):
        """TC009: 测试 convert_number 函数：负数输入，覆盖 L179 分支 True"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc010(self):
        """TC010: 测试 convert_number 函数：输入0，覆盖 L179 分支 False，L183 分支 False，for循环体不执行（digit_group <= 0），复合条件 L195 中 num > 0 为 False，not word_groups 为 True"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc011(self):
        """TC011: 测试 convert_number 函数：输入1，覆盖 L179 分支 False，L183 分支 False，for循环体不执行（digit_group <= 0），复合条件 L195 中 num > 0 为 True，not word_groups 为 False"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc012(self):
        """TC012: 测试 convert_number 函数：输入100（short系统），覆盖 L179 分支 False，L183 分支 False，for循环执行（digit_group > 0），且 digit_group < 100 调用 convert_small_number，复合条件 L195 中 num > 0 为 False，not word_groups 为 False"""
        result = convert_small_number(100, 'short')
        assert result == 'one hundred'

    def test_tc013(self):
        """TC013: 测试 convert_number 函数：输入123456789012345（short系统），覆盖 L179 分支 False，L183 分支 False，for循环多次执行（digit_group > 0），且 digit_group >= 100 递归调用 convert_number"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc014(self):
        """TC014: 测试 convert_number 函数：输入123456789012345（long系统），覆盖 L179 分支 False，L183 分支 False，for循环多次执行（digit_group > 0），且 digit_group >= 100 递归调用 convert_number"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc015(self):
        """TC015: 测试 convert_number 函数：输入123456789012345（indian系统），覆盖 L179 分支 False，L183 分支 False，for循环多次执行（digit_group > 0），且 digit_group >= 100 递归调用 convert_number"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc016(self):
        """TC016: 测试 convert_number 函数：输入超过short系统最大值，覆盖 L179 分支 False，L183 分支 True"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc017(self):
        """TC017: 测试 convert_number 函数：输入超过long系统最大值，覆盖 L179 分支 False，L183 分支 True"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc018(self):
        """TC018: 测试 convert_number 函数：输入超过indian系统最大值，覆盖 L179 分支 False，L183 分支 True"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')
