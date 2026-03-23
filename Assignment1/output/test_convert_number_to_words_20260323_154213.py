import pytest
import sys
import os

# 导入被测代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from convert_number_to_words import *


class TestNumberingSystemMaxValue:
    """测试 NumberingSystem.max_value 方法"""
    
    def test_tc001_max_value_short(self):
        """测试NumberingSystem.max_value方法，有效系统'short'"""
        result = NumberingSystem.max_value("short")
        assert result == 999999999999999999
    
    def test_tc002_max_value_long(self):
        """测试NumberingSystem.max_value方法，有效系统'long'"""
        result = NumberingSystem.max_value("long")
        assert result == 999999999999999999999
    
    def test_tc003_max_value_indian(self):
        """测试NumberingSystem.max_value方法，有效系统'indian'"""
        result = NumberingSystem.max_value("indian")
        assert result == 9999999999999999999
    
    def test_tc004_max_value_invalid_system(self):
        """测试NumberingSystem.max_value方法，无效系统，触发异常"""
        with pytest.raises(ValueError, match="Invalid numbering system"):
            NumberingSystem.max_value("invalid")


class TestConvertSmallNumber:
    """测试 convert_small_number 方法"""
    
    def test_tc005_convert_small_number_zero(self):
        """测试convert_small_number方法，输入0"""
        result = convert_small_number(0)
        assert result == "zero"
    
    def test_tc006_convert_small_number_single_digit(self):
        """测试convert_small_number方法，输入个位数5"""
        result = convert_small_number(5)
        assert result == "five"
    
    def test_tc007_convert_small_number_ten(self):
        """测试convert_small_number方法，输入10"""
        result = convert_small_number(10)
        assert result == "ten"
    
    def test_tc008_convert_small_number_teen(self):
        """测试convert_small_number方法，输入15"""
        result = convert_small_number(15)
        assert result == "fifteen"
    
    def test_tc009_convert_small_number_twenty(self):
        """测试convert_small_number方法，输入20"""
        result = convert_small_number(20)
        assert result == "twenty"
    
    def test_tc010_convert_small_number_twenty_five(self):
        """测试convert_small_number方法，输入25"""
        result = convert_small_number(25)
        assert result == "twenty-five"
    
    def test_tc011_convert_small_number_negative(self):
        """测试convert_small_number方法，输入负数，触发异常"""
        with pytest.raises(ValueError, match="This function only accepts non-negative integers"):
            convert_small_number(-1)
    
    def test_tc012_convert_small_number_too_large(self):
        """测试convert_small_number方法，输入大于等于100的数，触发异常"""
        with pytest.raises(ValueError, match="This function only converts numbers less than 100"):
            convert_small_number(100)


class TestConvertNumber:
    """测试 convert_number 方法"""
    
    def test_tc013_convert_number_zero_short(self):
        """测试convert_number方法，输入0，默认short系统"""
        result = convert_number(0, "short")
        assert result == "zero"
    
    def test_tc014_convert_number_one_short(self):
        """测试convert_number方法，输入1，默认short系统"""
        result = convert_number(1, "short")
        assert result == "one"
    
    def test_tc015_convert_number_hundred_short(self):
        """测试convert_number方法，输入100，默认short系统"""
        result = convert_number(100, "short")
        assert result == "one hundred"
    
    def test_tc016_convert_number_negative_hundred_short(self):
        """测试convert_number方法，输入-100，默认short系统"""
        result = convert_number(-100, "short")
        assert result == "negative one hundred"
    
    def test_tc017_convert_number_medium_short(self):
        """测试convert_number方法，输入一个中等大小的数，覆盖short系统多个单位"""
        result = convert_number(1234567, "short")
        expected = "one million two hundred thirty-four thousand five hundred sixty-seven"
        assert result == expected
    
    def test_tc018_convert_number_recursive_digit_group(self):
        """测试convert_number方法，输入一个需要递归转换digit_group的数（digit_group >= 100）"""
        result = convert_number(1000000, "short")
        assert result == "one million"
    
    def test_tc019_convert_number_long_system(self):
        """测试convert_number方法，使用long系统"""
        result = convert_number(1000000000, "long")
        assert result == "one milliard"
    
    def test_tc020_convert_number_indian_system(self):
        """测试convert_number方法，使用indian系统"""
        result = convert_number(10000000, "indian")
        assert result == "one crore"
    
    def test_tc021_convert_number_exceed_short_max(self):
        """测试convert_number方法，输入超过short系统最大值，触发异常"""
        with pytest.raises(ValueError, match="Input number is too large"):
            convert_number(1000000000000000000, "short")
    
    def test_tc022_convert_number_exceed_long_max(self):
        """测试convert_number方法，输入超过long系统最大值，触发异常"""
        with pytest.raises(ValueError, match="Input number is too large"):
            convert_number(1000000000000000000000, "long")
    
    def test_tc023_convert_number_exceed_indian_max(self):
        """测试convert_number方法，输入超过indian系统最大值，触发异常"""
        with pytest.raises(ValueError, match="Input number is too large"):
            convert_number(10000000000000000000, "indian")
    
    def test_tc024_convert_number_negative_exceed_max(self):
        """测试convert_number方法，输入负数且超过最大值，先处理符号再检查最大值"""
        with pytest.raises(ValueError, match="Input number is too large"):
            convert_number(-1000000000000000000, "short")