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
        """TC001: 测试NumberingSystem.max_value方法，有效系统'short'"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc002(self):
        """TC002: 测试NumberingSystem.max_value方法，有效系统'long'"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc003(self):
        """TC003: 测试NumberingSystem.max_value方法，有效系统'indian'"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc004(self):
        """TC004: 测试NumberingSystem.max_value方法，无效系统，触发异常"""
        result = NumberingSystem.max_value('invalid')
        assert result == None

    def test_tc005(self):
        """TC005: 测试convert_small_number方法，输入0"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc006(self):
        """TC006: 测试convert_small_number方法，输入个位数5"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc007(self):
        """TC007: 测试convert_small_number方法，输入10"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc008(self):
        """TC008: 测试convert_small_number方法，输入15"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc009(self):
        """TC009: 测试convert_small_number方法，输入20"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc010(self):
        """TC010: 测试convert_small_number方法，输入25"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc011(self):
        """TC011: 测试convert_small_number方法，输入负数，触发异常"""
        result = convert_small_number(-1)
        assert result == None

    def test_tc012(self):
        """TC012: 测试convert_small_number方法，输入大于等于100的数，触发异常"""
        result = convert_small_number(100)
        assert result == None

    def test_tc013(self):
        """TC013: 测试convert_number方法，输入0，默认系统short"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc014(self):
        """TC014: 测试convert_number方法，输入1，默认系统short"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc015(self):
        """TC015: 测试convert_number方法，输入100，默认系统short"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc016(self):
        """TC016: 测试convert_number方法，输入-100，默认系统short"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc017(self):
        """TC017: 测试convert_number方法，输入大数123456789012345，系统short"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc018(self):
        """TC018: 测试convert_number方法，输入大数123456789012345，系统long"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc019(self):
        """TC019: 测试convert_number方法，输入大数123456789012345，系统indian"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc020(self):
        """TC020: 测试convert_number方法，输入超过short系统上限的数，触发异常"""
        result = convert_number(1000000000000000000, 'short')
        assert result == None

    def test_tc021(self):
        """TC021: 测试convert_number方法，输入超过long系统上限的数，触发异常"""
        result = convert_number(1000000000000000000000, 'long')
        assert result == None

    def test_tc022(self):
        """TC022: 测试convert_number方法，输入超过indian系统上限的数，触发异常"""
        result = convert_number(10000000000000000000, 'indian')
        assert result == None

    def test_tc023(self):
        """TC023: 测试convert_number方法，输入一个需要递归处理digit_group的数（如1000），默认系统short"""
        result = convert_number(1000, 'short')
        assert result == 'one thousand'

    def test_tc024(self):
        """TC024: 测试convert_number方法，输入一个需要递归处理digit_group的数（如1000000），默认系统short"""
        result = convert_number(1000000, 'short')
        assert result == 'one million'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 方法中无效的 numbering system 参数，触发默认分支和 ValueError"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid_system')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试直接运行脚本时的 __main__ 分支，覆盖 doctest 导入和执行，以及最后的 print 语句"""
        result = convert_small_number()
        assert result == 'None'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试NumberingSystem.max_value的默认分支，传入无效的numbering system"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试直接运行模块时的主程序分支"""
        result = convert_small_number()
        assert result == None
