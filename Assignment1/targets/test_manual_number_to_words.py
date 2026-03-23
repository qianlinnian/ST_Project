import pytest
from convert_number_to_words import NumberingSystem, convert_small_number, convert_number  

class TestNumberingSystem:
    def test_max_value(self):
        # TC1 Path1 SHORT
        assert NumberingSystem.max_value("short") == 10**18 - 1
        # TC2 Path2 LONG
        assert NumberingSystem.max_value("long") == 10**21 - 1
        # TC3 Path3 INDIAN
        assert NumberingSystem.max_value("indian") == 10**19 - 1
        # TC4 Path4 非法系统（文档注明抛 KeyError）
        with pytest.raises(KeyError):
            NumberingSystem.max_value("abc")


class TestConvertSmallNumber:
    def test_convert_small_number(self):
        # TC1 Path1 负数
        with pytest.raises(ValueError):
            convert_small_number(-1)
        # TC2 Path2 >=100
        with pytest.raises(ValueError):
            convert_small_number(100)
        # TC3 Path3 个位数（0）
        assert convert_small_number(0) == "zero"
        # TC4 Path3 个位数（7）
        assert convert_small_number(7) == "seven"
        # TC5 Path4 10-19
        assert convert_small_number(15) == "fifteen"
        # TC6 Path5 20-99（带连字符）
        assert convert_small_number(42) == "forty-two"
        # TC7 Path5 20-99（无连字符）
        assert convert_small_number(20) == "twenty"


class TestConvertNumber:
    def test_convert_number(self):
        # TC1 Path1 负数
        assert convert_number(-45) == "negative forty-five"
        # TC2 Path2 超过最大值
        with pytest.raises(ValueError):
            convert_number(10**22)   # 任意超过 max_value 的数字
        # TC3 Path3 普通小数字
        assert convert_number(42) == "forty-two"
        # TC4 Path4 触发递归（三位数）
        assert convert_number(345) == "three hundred forty-five"
        # TC5 Path5 多单位拼接 + 递归（复合路径）
        assert convert_number(12345) == "twelve thousand three hundred forty-five"
        # TC6 Path6 输入 0
        assert convert_number(0) == "zero"