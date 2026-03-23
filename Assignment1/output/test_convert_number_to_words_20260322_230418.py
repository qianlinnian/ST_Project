"""自动生成的白盒测试用例 - convert_number_to_words"""
import pytest
import sys
import os

# 将 targets 目录加入 path，以便导入被测模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import convert_small_number, convert_number, NumberingSystem, NumberWords


class TestConvertNumberToWords:
    """白盒测试类 - 由 LLM 自动生成"""

    def test_tc_ns_mv_001(self):
        """TC_NS_MV_001: 测试 NumberingSystem.max_value 方法，输入 'short' 系统，覆盖 case cls.SHORT 分支。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc_ns_mv_002(self):
        """TC_NS_MV_002: 测试 NumberingSystem.max_value 方法，输入 'long' 系统，覆盖 case cls.LONG 分支。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc_ns_mv_003(self):
        """TC_NS_MV_003: 测试 NumberingSystem.max_value 方法，输入 'indian' 系统，覆盖 case cls.INDIAN 分支。"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc_ns_mv_004(self):
        """TC_NS_MV_004: 测试 NumberingSystem.max_value 方法，输入无效系统，覆盖 case _ 分支并抛出 ValueError。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_csn_001(self):
        """TC_CSN_001: 测试 convert_small_number 函数，输入负数，覆盖 L121 (num < 0 -> True) 分支并抛出 ValueError。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc_csn_002(self):
        """TC_CSN_002: 测试 convert_small_number 函数，输入大于等于 100 的数，覆盖 L123 (num >= 100 -> True) 分支并抛出 ValueError。"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc_csn_003(self):
        """TC_CSN_003: 测试 convert_small_number 函数，输入 0，覆盖 L126 (tens == 0 -> True) 分支和复合条件 L127 (NumberWords.ONES.value[ones] -> False, 'zero' -> True)。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc_csn_004(self):
        """TC_CSN_004: 测试 convert_small_number 函数，输入个位数 (例如 5)，覆盖 L126 (tens == 0 -> True) 分支和复合条件 L127 (NumberWords.ONES.value[ones] -> True)。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc_csn_005(self):
        """TC_CSN_005: 测试 convert_small_number 函数，输入十几的数 (例如 15)，覆盖 L128 (tens == 1 -> True) 分支。"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc_csn_006(self):
        """TC_CSN_006: 测试 convert_small_number 函数，输入几十的整数 (例如 20)，覆盖 L128 (tens == 1 -> False) 分支和 L131 (inline if: NumberWords.ONES.value[ones] -> False)。"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc_csn_007(self):
        """TC_CSN_007: 测试 convert_small_number 函数，输入几十带个位的数 (例如 25)，覆盖 L128 (tens == 1 -> False) 分支和 L131 (inline if: NumberWords.ONES.value[ones] -> True)。"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc_cn_001(self):
        """TC_CN_001: 测试 convert_number 函数，输入 0，覆盖 L195 复合条件 (num > 0 -> False, not word_groups -> True)。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc_cn_002(self):
        """TC_CN_002: 测试 convert_number 函数，输入负数，覆盖 L179 (num < 0 -> True) 分支。"""
        result = convert_number(-100, 'short')
        assert result == 'negative one hundred'

    def test_tc_cn_003(self):
        """TC_CN_003: 测试 convert_number 函数，输入超过 'short' 系统最大值的数，覆盖 L183 (num > NumberingSystem.max_value(system) -> True) 分支。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc_cn_004(self):
        """TC_CN_004: 测试 convert_number 函数，输入超过 'long' 系统最大值的数，覆盖 L183 (num > NumberingSystem.max_value(system) -> True) 分支。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc_cn_005(self):
        """TC_CN_005: 测试 convert_number 函数，输入超过 'indian' 系统最大值的数，覆盖 L183 (num > NumberingSystem.max_value(system) -> True) 分支。"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc_cn_006(self):
        """TC_CN_006: 测试 convert_number 函数，输入小于 100 的正数 (例如 42)，覆盖 L195 复合条件 (num > 0 -> True, not word_groups -> True)。"""
        result = convert_number(42, 'short')
        assert result == 'forty-two'

    def test_tc_cn_007(self):
        """TC_CN_007: 测试 convert_number 函数，输入三位数 (例如 123)，覆盖 L188 (digit_group > 0 -> True) 和 L190 (digit_group >= 100 -> False)。"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'

    def test_tc_cn_008(self):
        """TC_CN_008: 测试 convert_number 函数，输入多位数 (例如 123456)，覆盖 L190 (digit_group >= 100 -> True) 触发递归调用。"""
        result = convert_number(123456, 'short')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six'

    def test_tc_cn_009(self):
        """TC_CN_009: 测试 convert_number 函数，输入中间有零组的多位数 (例如 1,000,001)，覆盖 L188 (digit_group > 0 -> False) 和 L195 (num > 0 -> True, not word_groups -> False)。"""
        result = convert_number(1000001, 'short')
        assert result == 'one million one'

    def test_tc_cn_010(self):
        """TC_CN_010: 测试 convert_number 函数，输入一个包含 'short' 系统所有单位的复杂数字 (来自 doctest)。"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc_cn_011(self):
        """TC_CN_011: 测试 convert_number 函数，输入一个包含 'long' 系统所有单位的复杂数字 (来自 doctest)。"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc_cn_012(self):
        """TC_CN_012: 测试 convert_number 函数，输入一个包含 'indian' 系统所有单位的复杂数字 (来自 doctest)。"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc_cn_013(self):
        """TC_CN_013: 测试 convert_number 函数，输入 'short' 系统最大值减一的边界值。"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc_cn_014(self):
        """TC_CN_014: 测试 convert_number 函数，输入 'long' 系统最大值减一的边界值。"""
        result = convert_number(999999999999999999999, 'long')
        assert result == 'nine hundred ninety-nine billiard nine hundred ninety-nine milliard nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine hundred ninety-nine'

    def test_tc_cn_015(self):
        """TC_CN_015: 测试 convert_number 函数，输入 'indian' 系统最大值减一的边界值。"""
        result = convert_number(9999999999999999999, 'indian')
        assert result == 'nine crore crore ninety-nine lakh crore ninety-nine thousand ninety-nine crore ninety-nine lakh nine thousand nine hundred ninety-nine'
