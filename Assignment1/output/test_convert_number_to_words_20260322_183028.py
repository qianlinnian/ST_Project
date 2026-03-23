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
        """TC001: 测试 NumberingSystem.max_value 使用 system='short'"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc002(self):
        """TC002: 测试 NumberingSystem.max_value 使用 system='long'"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc003(self):
        """TC003: 测试 NumberingSystem.max_value 使用 system='indian'"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc004(self):
        """TC004: 测试 NumberingSystem.max_value 使用无效 system，期望抛出 KeyError"""
        with pytest.raises(KeyError):
            NumberingSystem.max_value('invalid')

    def test_tc005(self):
        """TC005: 测试 convert_small_number 输入负数 num=-1"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc006(self):
        """TC006: 测试 convert_small_number 输入 num=100（大于等于100）"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc007(self):
        """TC007: 测试 convert_small_number 输入 num=0"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc008(self):
        """TC008: 测试 convert_small_number 输入 num=5（1-9范围）"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc009(self):
        """TC009: 测试 convert_small_number 输入 num=10（teens 且 ones=0）"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc010(self):
        """TC010: 测试 convert_small_number 输入 num=15（teens 且 ones≠0）"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc011(self):
        """TC011: 测试 convert_small_number 输入 num=20（tens≥2 且 ones=0）"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc012(self):
        """TC012: 测试 convert_small_number 输入 num=25（tens≥2 且 ones≠0）"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc013(self):
        """TC013: 测试 convert_number 输入 num=0, system='short'"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc014(self):
        """TC014: 测试 convert_number 输入 num=1, system='short'"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc015(self):
        """TC015: 测试 convert_number 输入 num=-1, system='short'"""
        result = convert_number(-1, 'short')
        assert result == 'negative one'

    def test_tc016(self):
        """TC016: 测试 convert_number 输入 num=100, system='short'"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc017(self):
        """TC017: 测试 convert_number 输入 num=123, system='short'"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'

    def test_tc018(self):
        """TC018: 测试 convert_number 输入 num=1000, system='short'"""
        result = convert_number(1000, 'short')
        assert result == 'one thousand'

    def test_tc019(self):
        """TC019: 测试 convert_number 输入 num=1001, system='short'"""
        result = convert_number(1001, 'short')
        assert result == 'one thousand one'

    def test_tc020(self):
        """TC020: 测试 convert_number 输入 num=123456789, system='short'"""
        result = convert_number(123456789, 'short')
        assert result == 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'

    def test_tc021(self):
        """TC021: 测试 convert_number 输入 num=999999999999999999 (short 最大值), system='short'"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc022(self):
        """TC022: 测试 convert_number 输入 num=1000000000000000000 (超过 short 最大值), system='short'"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc023(self):
        """TC023: 测试 convert_number 输入 num=123456789012345, system='long'"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc024(self):
        """TC024: 测试 convert_number 输入 num=999999999999999999999 (long 最大值), system='long'"""
        result = convert_number(999999999999999999999, 'long')
        assert result == 'nine hundred ninety-nine billiard nine hundred ninety-nine milliard nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc025(self):
        """TC025: 测试 convert_number 输入 num=1000000000000000000000 (超过 long 最大值), system='long'"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc026(self):
        """TC026: 测试 convert_number 输入 num=123456789012345, system='indian'"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc027(self):
        """TC027: 测试 convert_number 输入 num=9999999999999999999 (indian 最大值), system='indian'"""
        result = convert_number(9999999999999999999, 'indian')
        assert result == 'nine crore crore ninety-nine lakh crore ninety-nine crore ninety lakh ninety-nine thousand nine hundred ninety-nine'

    def test_tc028(self):
        """TC028: 测试 convert_number 输入 num=10000000000000000000 (超过 indian 最大值), system='indian'"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc029(self):
        """TC029: 测试 convert_number 输入无效 system='invalid'"""
        with pytest.raises(KeyError):
            convert_number(123, 'invalid')

    def test_tc_sup_001(self):
        """TC_SUP_001: 补充测试 NumberingSystem.max_value 使用无效 numbering system，触发默认分支"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 执行 __main__ 块以覆盖主程序代码"""
        result = convert_small_number()
        assert result == None

    def test_tc_sup_001(self):
        """TC_SUP_001: 执行模块主块，覆盖 import doctest、doctest.testmod() 和打印语句"""
        result = convert_small_number()
        assert result == "convert_number(123456789) = 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'"

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试 NumberingSystem.max_value 的无效输入，通过模拟使 match 进入默认分支"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')
