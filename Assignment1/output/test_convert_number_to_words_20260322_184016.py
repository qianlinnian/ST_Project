"""自动生成的白盒测试用例 - convert_number_to_words"""
import pytest
import sys
import os

# 将 targets 目录加入 path，以便导入被测模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import convert_small_number, convert_number, NumberingSystem, NumberWords


class TestConvertNumberToWords:
    """白盒测试类 - 由 LLM 自动生成"""

    def test_tc_max_001(self):
        """TC_MAX_001: 测试 NumberingSystem.max_value 方法，使用 'short' 系统。"""
        result = NumberingSystem.max_value('short')
        assert result == 999999999999999999

    def test_tc_max_002(self):
        """TC_MAX_002: 测试 NumberingSystem.max_value 方法，使用 'long' 系统。"""
        result = NumberingSystem.max_value('long')
        assert result == 999999999999999999999

    def test_tc_max_003(self):
        """TC_MAX_003: 测试 NumberingSystem.max_value 方法，使用 'indian' 系统。"""
        result = NumberingSystem.max_value('indian')
        assert result == 9999999999999999999

    def test_tc_max_004(self):
        """TC_MAX_004: 测试 NumberingSystem.max_value 方法，使用无效系统名。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('invalid')

    def test_tc_small_001(self):
        """TC_SMALL_001: 测试 convert_small_number 函数，输入负数。"""
        with pytest.raises(ValueError):
            convert_small_number(-1)

    def test_tc_small_002(self):
        """TC_SMALL_002: 测试 convert_small_number 函数，输入大于等于 100 的数。"""
        with pytest.raises(ValueError):
            convert_small_number(100)

    def test_tc_small_003(self):
        """TC_SMALL_003: 测试 convert_small_number 函数，输入 0。"""
        result = convert_small_number(0)
        assert result == 'zero'

    def test_tc_small_004(self):
        """TC_SMALL_004: 测试 convert_small_number 函数，输入个位数 (例如 5)。"""
        result = convert_small_number(5)
        assert result == 'five'

    def test_tc_small_005(self):
        """TC_SMALL_005: 测试 convert_small_number 函数，输入 10-19 之间的数 (例如 10)。"""
        result = convert_small_number(10)
        assert result == 'ten'

    def test_tc_small_006(self):
        """TC_SMALL_006: 测试 convert_small_number 函数，输入 10-19 之间的数 (例如 15)。"""
        result = convert_small_number(15)
        assert result == 'fifteen'

    def test_tc_small_007(self):
        """TC_SMALL_007: 测试 convert_small_number 函数，输入整十数 (例如 20)。"""
        result = convert_small_number(20)
        assert result == 'twenty'

    def test_tc_small_008(self):
        """TC_SMALL_008: 测试 convert_small_number 函数，输入两位数 (例如 25)。"""
        result = convert_small_number(25)
        assert result == 'twenty-five'

    def test_tc_small_009(self):
        """TC_SMALL_009: 测试 convert_small_number 函数，输入最大有效两位数 (99)。"""
        result = convert_small_number(99)
        assert result == 'ninety-nine'

    def test_tc_conv_001(self):
        """TC_CONV_001: 测试 convert_number 函数，输入 0。"""
        result = convert_number(0, 'short')
        assert result == 'zero'

    def test_tc_conv_002(self):
        """TC_CONV_002: 测试 convert_number 函数，输入 1。"""
        result = convert_number(1, 'short')
        assert result == 'one'

    def test_tc_conv_003(self):
        """TC_CONV_003: 测试 convert_number 函数，输入负数 (-1)。"""
        result = convert_number(-1, 'short')
        assert result == 'negative one'

    def test_tc_conv_004(self):
        """TC_CONV_004: 测试 convert_number 函数，输入小于 100 的数 (99)。"""
        result = convert_number(99, 'short')
        assert result == 'ninety-nine'

    def test_tc_conv_005(self):
        """TC_CONV_005: 测试 convert_number 函数，输入 100 (第一个需要 'hundred' 的数)。"""
        result = convert_number(100, 'short')
        assert result == 'one hundred'

    def test_tc_conv_006(self):
        """TC_CONV_006: 测试 convert_number 函数，输入 123 (包含百、十、个位)。"""
        result = convert_number(123, 'short')
        assert result == 'one hundred twenty-three'

    def test_tc_conv_007(self):
        """TC_CONV_007: 测试 convert_number 函数，输入 1000 (第一个需要 'thousand' 的数)。"""
        result = convert_number(1000, 'short')
        assert result == 'one thousand'

    def test_tc_conv_008(self):
        """TC_CONV_008: 测试 convert_number 函数，输入 123456 (多组数字，包含 digit_group >= 100 的递归调用)。"""
        result = convert_number(123456, 'short')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six'

    def test_tc_conv_009(self):
        """TC_CONV_009: 测试 convert_number 函数，输入 'short' 系统的最大有效数字。"""
        result = convert_number(999999999999999999, 'short')
        assert result == 'nine hundred ninety-nine quadrillion nine hundred ninety-nine trillion nine hundred ninety-nine billion nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine'

    def test_tc_conv_010(self):
        """TC_CONV_010: 测试 convert_number 函数，输入超出 'short' 系统最大值的数字。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000, 'short')

    def test_tc_conv_011(self):
        """TC_CONV_011: 测试 convert_number 函数，输入 'long' 系统的最大有效数字。"""
        result = convert_number(999999999999999999999, 'long')
        assert result == 'nine hundred ninety-nine thousand nine hundred ninety-nine billiard nine hundred ninety-nine thousand nine hundred ninety-nine milliard nine hundred ninety-nine million nine hundred ninety-nine thousand ninety-nine'

    def test_tc_conv_012(self):
        """TC_CONV_012: 测试 convert_number 函数，输入超出 'long' 系统最大值的数字。"""
        with pytest.raises(ValueError):
            convert_number(1000000000000000000000, 'long')

    def test_tc_conv_013(self):
        """TC_CONV_013: 测试 convert_number 函数，输入 'indian' 系统的最大有效数字。"""
        result = convert_number(9999999999999999999, 'indian')
        assert result == 'ninety-nine thousand nine hundred ninety-nine crore crore ninety-nine lakh crore ninety-nine thousand nine hundred ninety-nine crore ninety-nine lakh nine thousand ninety-nine'

    def test_tc_conv_014(self):
        """TC_CONV_014: 测试 convert_number 函数，输入超出 'indian' 系统最大值的数字。"""
        with pytest.raises(ValueError):
            convert_number(10000000000000000000, 'indian')

    def test_tc_conv_015(self):
        """TC_CONV_015: 测试 convert_number 函数，使用 'short' 系统转换大数字 (doctest 示例)。"""
        result = convert_number(123456789012345, 'short')
        assert result == 'one hundred twenty-three trillion four hundred fifty-six billion seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc_conv_016(self):
        """TC_CONV_016: 测试 convert_number 函数，使用 'long' 系统转换大数字 (doctest 示例)。"""
        result = convert_number(123456789012345, 'long')
        assert result == 'one hundred twenty-three thousand four hundred fifty-six milliard seven hundred eighty-nine million twelve thousand three hundred forty-five'

    def test_tc_conv_017(self):
        """TC_CONV_017: 测试 convert_number 函数，使用 'indian' 系统转换大数字 (doctest 示例)。"""
        result = convert_number(123456789012345, 'indian')
        assert result == 'one crore crore twenty-three lakh crore forty-five thousand six hundred seventy-eight crore ninety lakh twelve thousand three hundred forty-five'

    def test_tc_conv_018(self):
        """TC_CONV_018: 测试 convert_number 函数，输入一个精确的 10 的幂 (1 百万)。"""
        result = convert_number(1000000, 'short')
        assert result == 'one million'

    def test_tc_conv_019(self):
        """TC_CONV_019: 测试 convert_number 函数，输入一个 10 的幂加 1 (1 百万零 1)。"""
        result = convert_number(1000001, 'short')
        assert result == 'one million one'

    def test_tc_conv_020(self):
        """TC_CONV_020: 测试 convert_number 函数，输入中间有零的数字组 (例如 10 亿)。"""
        result = convert_number(1000000000, 'short')
        assert result == 'one billion'

    def test_tc_conv_021(self):
        """TC_CONV_021: 测试 convert_number 函数，输入中间有零的数字组 (例如 1 千万亿)。"""
        result = convert_number(1000000000000000, 'short')
        assert result == 'one quadrillion'

    def test_tc_conv_022(self):
        """TC_CONV_022: 测试 convert_number 函数，输入数字组大于等于 100 的数字 (例如 100 千万亿)。"""
        result = convert_number(100000000000000000, 'short')
        assert result == 'one hundred quadrillion'

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 函数，传入一个无效的数字系统名称，以覆盖 match 语句中的默认分支 (case _) 并抛出 ValueError。此测试旨在触发 L51 和 L52。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('unknown')

    def test_tc_sup_001(self):
        """TC_SUP_001: 测试 NumberingSystem.max_value 方法，传入一个无效的数字系统名称，以触发 ValueError 并覆盖默认匹配分支。"""
        with pytest.raises(ValueError):
            NumberingSystem.max_value('UNKNOWN_SYSTEM')

    def test_tc_sup_002(self):
        """TC_SUP_002: 测试 convert_number 函数，传入与主执行块 (L205) 中示例相同的数字 123456789，确保该特定输入被覆盖。"""
        result = convert_number(123456789, 'short')
        assert result == 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'
