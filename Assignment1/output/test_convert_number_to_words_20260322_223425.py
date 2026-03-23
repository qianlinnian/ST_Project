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
        """TC001: 测试convert_small_number函数：负数输入，覆盖L121分支True"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc002(self):
        """TC002: 测试convert_small_number函数：大于等于100的输入，覆盖L121分支False，L123分支True"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc003(self):
        """TC003: 测试convert_small_number函数：输入0，覆盖L121分支False，L123分支False，L126分支True，复合条件L127中第一个子条件为False"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc004(self):
        """TC004: 测试convert_small_number函数：输入5（个位数），覆盖L121分支False，L123分支False，L126分支True，复合条件L127中第一个子条件为True"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc005(self):
        """TC005: 测试convert_small_number函数：输入10（十几，个位为0），覆盖L121分支False，L123分支False，L126分支False，L128分支True"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc006(self):
        """TC006: 测试convert_small_number函数：输入15（十几，个位非0），覆盖L121分支False，L123分支False，L126分支False，L128分支True"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc007(self):
        """TC007: 测试convert_small_number函数：输入20（几十，个位为0），覆盖L121分支False，L123分支False，L126分支False，L128分支False"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc008(self):
        """TC008: 测试convert_small_number函数：输入25（几十，个位非0），覆盖L121分支False，L123分支False，L126分支False，L128分支False"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc009(self):
        """TC009: 测试convert_number函数：负数输入，覆盖L179分支True"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc010(self):
        """TC010: 测试convert_number函数：输入0，覆盖L179分支False，L183分支False，for循环体不执行，复合条件L195中num>0为False，not word_groups为True"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc011(self):
        """TC011: 测试convert_number函数：输入1（short系统），覆盖L179分支False，L183分支False，for循环体不执行，复合条件L195中num>0为True，not word_groups为False"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc012(self):
        """TC012: 测试convert_number函数：输入100（short系统），覆盖L179分支False，L183分支False，for循环执行，digit_group>0为True，digit_group>=100为False"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc013(self):
        """TC013: 测试convert_number函数：输入123456789012345（short系统），覆盖L179分支False，L183分支False，for循环多次执行，digit_group>0为True，digit_group>=100为True（递归调用）"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc014(self):
        """TC014: 测试convert_number函数：输入123456789012345（long系统），覆盖L179分支False，L183分支False，for循环多次执行"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc015(self):
        """TC015: 测试convert_number函数：输入123456789012345（indian系统），覆盖L179分支False，L183分支False，for循环多次执行"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc016(self):
        """TC016: 测试convert_number函数：输入超过short系统最大值，覆盖L179分支False，L183分支True"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc017(self):
        """TC017: 测试convert_number函数：输入超过long系统最大值，覆盖L179分支False，L183分支True"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc018(self):
        """TC018: 测试convert_number函数：输入超过indian系统最大值，覆盖L179分支False，L183分支True"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc019(self):
        """TC019: 测试NumberingSystem.max_value方法：short系统，覆盖case cls.SHORT分支"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc020(self):
        """TC020: 测试NumberingSystem.max_value方法：long系统，覆盖case cls.LONG分支"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc021(self):
        """TC021: 测试NumberingSystem.max_value方法：indian系统，覆盖case cls.INDIAN分支"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc022(self):
        """TC022: 测试NumberingSystem.max_value方法：无效系统，覆盖case _分支"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')
