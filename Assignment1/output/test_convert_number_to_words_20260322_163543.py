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
        """TC001: 测试 convert_small_number 函数，输入 0"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc002(self):
        """TC002: 测试 convert_small_number 函数，输入 5"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc003(self):
        """TC003: 测试 convert_small_number 函数，输入 10"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 函数，输入 15"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc005(self):
        """TC005: 测试 convert_small_number 函数，输入 20"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 函数，输入 25"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 函数，输入 -1"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc008(self):
        """TC008: 测试 convert_small_number 函数，输入 123"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc009(self):
        """TC009: 测试 convert_number 函数，输入 0"""
        result = convert_number(0)
        assert result == 'zero'

    def test_tc010(self):
        """TC010: 测试 convert_number 函数，输入 1"""
        result = convert_number(1)
        assert result == 'one'

    def test_tc011(self):
        """TC011: 测试 convert_number 函数，输入 100"""
        result = convert_number(100)
        assert result == 'one hundred'

    def test_tc012(self):
        """TC012: 测试 convert_number 函数，输入 -100"""
        result = convert_number(-100)
        assert result == 'negative one hundred'

    def test_tc013(self):
        """TC013: 测试 convert_number 函数，输入 123456789012345"""
        result = convert_number(123456789012345)
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc014(self):
        """TC014: 测试 convert_number 函数，输入 10**18"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000)

    def test_tc015(self):
        """TC015: 测试 convert_number 函数，输入 10**21, system = 'long'"""
        with pytest.raises(ValueError):
            convert_number(100000000000000000000, 'long')

    def test_tc016(self):
        """TC016: 测试 convert_number 函数，输入 10**19, system = 'indian'"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc017(self):
        """TC017: 测试 NumberingSystem.max_value 函数，输入 'short'"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc018(self):
        """TC018: 测试 NumberingSystem.max_value 函数，输入 'long'"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc019(self):
        """TC019: 测试 NumberingSystem.max_value 函数，输入 'indian'"""
        result = NumberingSystem.max_value('indian')
        assert result == 99999999999999999999

    def test_tc020(self):
        """TC020: 测试 NumberingSystem.max_value 函数，输入无效的系统"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 max_value 方法传入无效的 numbering system"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试主程序导入 doctest"""
        result = convert_small_number()
        assert result == '无错误'

    def test_tc_sup_003(self):
        """TC_SUP_003: 测试主程序打印 convert_number 的结果"""
        result = convert_number()
        assert result == "convert_number(123456789) = 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'"

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 max_value 方法，传入无效的 numbering system"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试 convert_number 方法，调用时使用无效的 numbering system"""
        with pytest.raises(ValueError):
            convert_number(123, 'invalid')

    def test_tc_sup_003(self):
        """TC_SUP_003: 测试主模块，确保 doctest 被执行"""
        result = convert_small_number()
        assert result == '无错误'

    def test_tc_sup_004(self):
        """TC_SUP_004: 测试主模块，确保 convert_number 调用正常"""
        result = convert_number()
        assert result == '无错误'
