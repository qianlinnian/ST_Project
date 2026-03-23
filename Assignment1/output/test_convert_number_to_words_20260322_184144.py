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
        """TC001: 测试零值处理"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc002(self):
        """TC002: 测试正数小于100的转换"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc003(self):
        """TC003: 测试负数的转换"""
        result = convert_number(-100)
        assert result == 'negative one hundred'

    def test_tc004(self):
        """TC004: 测试大于100的输入抛出异常"""
        with pytest.raises(ValueError):
            convert_number(123)

    def test_tc005(self):
        """TC005: 测试短制最大值边界"""
        result = convert_number(1000000000000000000, 'short')
        assert result == 'one quintillion'

    def test_tc006(self):
        """TC006: 测试超出短制最大值抛出异常"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000001, 'short')

    def test_tc007(self):
        """TC007: 测试长制的转换"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc008(self):
        """TC008: 测试印度制的转换"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc009(self):
        """TC009: 测试无效的命名系统抛出异常"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value(100, 'invalid')

    def test_tc010(self):
        """TC010: 测试连字符的使用"""
        result = convert_small_number(21)
        assert result == 'twenty-one'

    def test_tc011(self):
        """TC011: 测试teens的特殊处理"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 max_value 方法，传入无效的 numbering system"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试 convert_small_number 方法，传入负数"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc_sup_003(self):
        """TC_SUP_003: 测试 convert_small_number 方法，传入大于等于100的数"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc_sup_005(self):
        """TC_SUP_005: 测试主程序，确保 doctest 正常执行"""
        result = convert_small_number()
        assert result == '无异常抛出'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试无效的编号系统"""
        with pytest.raises(ValueError):
            convert_small_number('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试 doctest 导入"""
        result = convert_small_number()
        assert result == 'None'

    def test_tc_sup_003(self):
        """TC_SUP_003: 测试打印 convert_number 的结果"""
        result = convert_number()
        assert result == "convert_number(123456789) = 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'"
