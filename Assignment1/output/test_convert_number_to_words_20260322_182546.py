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
        """TC001: 测试convert_small_number函数：输入0，应返回'zero'"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc002(self):
        """TC002: 测试convert_small_number函数：输入5（个位数）"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc003(self):
        """TC003: 测试convert_small_number函数：输入10（整十数，teens）"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc004(self):
        """TC004: 测试convert_small_number函数：输入15（teens）"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc005(self):
        """TC005: 测试convert_small_number函数：输入20（整十数，非teens）"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc006(self):
        """TC006: 测试convert_small_number函数：输入25（非整十数，非teens）"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc007(self):
        """TC007: 测试convert_small_number函数：输入负数，应抛出ValueError"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc008(self):
        """TC008: 测试convert_small_number函数：输入100，应抛出ValueError"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc009(self):
        """TC009: 测试NumberingSystem.max_value函数：输入'short'，应返回999999999999999999"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc010(self):
        """TC010: 测试NumberingSystem.max_value函数：输入'long'，应返回999999999999999999999"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc011(self):
        """TC011: 测试NumberingSystem.max_value函数：输入'indian'，应返回9999999999999999999"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc012(self):
        """TC012: 测试NumberingSystem.max_value函数：输入无效系统，应抛出ValueError"""
        with pytest.raises(KeyError):
            NumberingSystem.max_value('invalid')

    def test_tc013(self):
        """TC013: 测试convert_number函数：输入0，默认short系统"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc014(self):
        """TC014: 测试convert_number函数：输入1，默认short系统"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc015(self):
        """TC015: 测试convert_number函数：输入100，默认short系统"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc016(self):
        """TC016: 测试convert_number函数：输入-100，默认short系统"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc017(self):
        """TC017: 测试convert_number函数：输入123456789，默认short系统"""
        result = convert_number(123456789, 'short')
        assert result == 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'

    def test_tc018(self):
        """TC018: 测试convert_number函数：输入123456789012345，long系统"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc019(self):
        """TC019: 测试convert_number函数：输入123456789012345，indian系统"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc020(self):
        """TC020: 测试convert_number函数：输入short系统最大值999999999999999999"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc021(self):
        """TC021: 测试convert_number函数：输入short系统最大值+1（1000000000000000000），应抛出ValueError"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc022(self):
        """TC022: 测试convert_number函数：输入long系统最大值999999999999999999999"""
        result = convert_number(999999999999999999999, 'long')
        assert result == 'nine hundred ninety-nine thousand nine hundred ninety-nine billiard nine hundred ninety-nine thousand nine hundred ninety-nine milliard nine hundred ninety-nine thousand nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc023(self):
        """TC023: 测试convert_number函数：输入indian系统最大值9999999999999999999"""
        result = convert_number(9999999999999999999, 'indian')
        assert result == 'nine crore crore ninety-nine lakh crore ninety-nine thousand nine hundred ninety-nine crore ninety-nine lakh ninety-nine thousand nine hundred ninety-nine'

    def test_tc024(self):
        """TC024: 测试convert_number函数：输入101（digit_group=1 < 100，调用convert_small_number）"""
        result = convert_small_number(101, 'short')
        assert result == 'one hundred one'

    def test_tc025(self):
        """TC025: 测试convert_number函数：输入无效系统，应抛出KeyError"""
        with pytest.raises(KeyError):
            convert_number(100, 'invalid')

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试NumberingSystem.max_value方法中无效的numbering system输入，触发默认分支和ValueError"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid_system')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试直接执行模块主程序，覆盖doctest.testmod()和print语句"""
        result = convert_small_number()
        assert result == ''

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试NumberingSystem.max_value的默认分支，传入无效的numbering system"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试直接运行脚本时的主程序入口"""
        result = convert_small_number()
        assert result == 'None'
