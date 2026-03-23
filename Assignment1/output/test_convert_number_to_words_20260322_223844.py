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
        """TC001: 测试 convert_small_number 输入负数，覆盖 L121 分支 True"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc002(self):
        """TC002: 测试 convert_small_number 输入大于等于100，覆盖 L123 分支 True"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc003(self):
        """TC003: 测试 convert_small_number 输入0，覆盖 L126 分支 True 和 L127 条件 ones=0"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 输入个位数5，覆盖 L126 分支 True 和 L127 条件 ones!=0"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc005(self):
        """TC005: 测试 convert_small_number 输入15，覆盖 L128 分支 True"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 输入25，覆盖 L128 分支 False 且个位非零"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 输入30，覆盖 L128 分支 False 且个位为零"""
        result = convert_small_number(30)
        assert result == 'thirty'

    def test_tc008(self):
        """TC008: 测试 convert_number 输入0，system=short，覆盖 L179 False, L183 False, L188 False 对于所有迭代，L195 子条件 num>0 False, not word_groups True"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc009(self):
        """TC009: 测试 convert_number 输入-100，system=short，覆盖 L179 True, L183 False, L188 True (对于 hundred), L195 子条件 num>0 False, not word_groups False"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc010(self):
        """TC010: 测试 convert_number 输入25，system=short，覆盖 L179 False, L183 False, L188 False 对于所有迭代，L195 子条件 num>0 True, not word_groups True"""
        result = convert_number(25, 'short')
        assert result == 'twenty-five'

    def test_tc011(self):
        """TC011: 测试 convert_number 输入 short system 最大值 999999999999999999，覆盖 L183 False 和循环中多个 digit_group>0 True"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc012(self):
        """TC012: 测试 convert_number 输入超过 short system 最大值 1000000000000000000，覆盖 L183 True"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc013(self):
        """TC013: 测试 convert_number 输入123456789012345，system=long，覆盖 long system 处理"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc014(self):
        """TC014: 测试 convert_number 输入123456789012345，system=indian，覆盖 indian system 处理"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc015(self):
        """TC015: 测试 convert_number 输入100，system=short，覆盖 L195 子条件 num>0 False, not word_groups False"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc016(self):
        """TC016: 测试 convert_number 输入101，system=short，覆盖 L195 子条件 num>0 True, not word_groups False"""
        result = convert_number(101, 'short')
        assert result == 'one hundred one'

    def test_tc017(self):
        """TC017: 测试 NumberingSystem.max_value 输入 short，返回 999999999999999999"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc018(self):
        """TC018: 测试 NumberingSystem.max_value 输入 long，返回 999999999999999999999"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc019(self):
        """TC019: 测试 NumberingSystem.max_value 输入 indian，返回 9999999999999999999"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc020(self):
        """TC020: 测试 NumberingSystem.max_value 输入无效 system，覆盖 case _ 分支"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')
