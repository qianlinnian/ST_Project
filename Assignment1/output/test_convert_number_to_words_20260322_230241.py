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
        """TC001: 测试 convert_small_number 负数输入，应引发异常。覆盖分支 L121 条件为 True。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc002(self):
        """TC002: 测试 convert_small_number 输入大于等于 100，应引发异常。覆盖分支 L123 条件为 True。"""
        with pytest.raises(ValueError):
            convert_small_number(123)

    def test_tc003(self):
        """TC003: 测试 convert_small_number 输入为 0，覆盖 tens==0 分支和复合条件 L127（子条件 NumberWords.ONES.value[ones] 为 False）。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc004(self):
        """TC004: 测试 convert_small_number 个位数输入 5，覆盖 tens==0 分支和复合条件 L127（子条件 NumberWords.ONES.value[ones] 为 True）。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc005(self):
        """TC005: 测试 convert_small_number 十几位输入 15，覆盖 tens==1 分支。"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc006(self):
        """TC006: 测试 convert_small_number 几十位输入 20，覆盖 tens 既不为 0 也不为 1 的分支，且个位为 0。"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc007(self):
        """TC007: 测试 convert_small_number 几十几输入 25，覆盖 tens 既不为 0 也不为 1 的分支，且个位不为 0。"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc008(self):
        """TC008: 测试 convert_number 输入为 0，默认 short 系统。覆盖 num<0 为 False，num>max_value 为 False，循环中所有 digit_group 为 0，复合条件 L195 中 num>0 为 False 且 not word_groups 为 True。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc009(self):
        """TC009: 测试 convert_number 输入小于 100 的正数 5，默认 short 系统。覆盖循环中所有 digit_group 为 0，复合条件 L195 中 num>0 为 True 且 not word_groups 为 True。"""
        result = convert_number(5, 'short')
        assert result == 'five'

    def test_tc010(self):
        """TC010: 测试 convert_number 输入 100，默认 short 系统。覆盖循环中 digit_group > 0 为 True（对于 hundred），且 digit_group < 100，调用 convert_small_number。最后复合条件 L195 中 num>0 为 False 且 not word_groups 为 False。"""
        result = convert_small_number(100, 'short')
        assert result == 'one hundred'

    def test_tc011(self):
        """TC011: 测试 convert_number 输入负数 -100，默认 short 系统。覆盖 num<0 分支为 True。"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc012(self):
        """TC012: 测试 convert_number 输入超过 short 系统最大值 10**18，应引发异常。覆盖 L183 条件为 True。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc013(self):
        """TC013: 测试 convert_number 输入超过 long 系统最大值 10**21，应引发异常。覆盖 L183 条件为 True。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc014(self):
        """TC014: 测试 convert_number 输入超过 indian 系统最大值 10**19，应引发异常。覆盖 L183 条件为 True。"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc015(self):
        """TC015: 测试 convert_number 复杂数字 123456789，short 系统，覆盖循环中多个 digit_group > 0，且有的 digit_group >= 100 导致递归调用 convert_number。"""
        result = convert_number(123456789, 'short')
        assert result == 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'

    def test_tc016(self):
        """TC016: 测试 convert_number 复杂数字 123456789012345，long 系统，覆盖 long 系统特定单位和递归。"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc017(self):
        """TC017: 测试 convert_number 复杂数字 123456789012345，indian 系统，覆盖 indian 系统特定单位和递归。"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc018(self):
        """TC018: 测试 convert_number 使用无效数字系统 'invalid'，应引发 ValueError（来自 max_value 调用）。"""
        with pytest.raises(ValueError):
            convert_number(0, 'invalid')

    def test_tc019(self):
        """TC019: 直接测试 NumberingSystem.max_value('short')，覆盖 SHORT case 分支。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc020(self):
        """TC020: 直接测试 NumberingSystem.max_value('long')，覆盖 LONG case 分支。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc021(self):
        """TC021: 直接测试 NumberingSystem.max_value('indian')，覆盖 INDIAN case 分支。"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc022(self):
        """TC022: 直接测试 NumberingSystem.max_value('invalid')，应引发 ValueError（覆盖默认 case 分支）。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc023(self):
        """TC023: 测试 convert_number 输入 123，short 系统，覆盖循环中 digit_group>0 (hundred)，且最后 num>0，复合条件 L195 中 num>0 为 True 且 not word_groups 为 False。"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'
