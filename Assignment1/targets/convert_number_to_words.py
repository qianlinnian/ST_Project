"""将数字转换为英文单词表示（示例被测代码）"""


def num_to_words(num: int) -> str:
    """
    将整数转换为英文单词
    支持范围: -999,999,999,999 到 999,999,999,999
    :param num: 整数
    :return: 英文单词字符串
    """
    if not isinstance(num, int):
        raise TypeError("输入必须是整数")

    if num < 0:
        return "minus " + num_to_words(-num)

    if num == 0:
        return "zero"

    ones = ["", "one", "two", "three", "four", "five",
            "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty",
            "sixty", "seventy", "eighty", "ninety"]

    def _convert_below_1000(n):
        if n == 0:
            return ""
        elif n < 20:
            return ones[n]
        elif n < 100:
            remainder = ones[n % 10]
            return tens[n // 10] + (" " + remainder if remainder else "")
        else:
            remainder = _convert_below_1000(n % 100)
            return ones[n // 100] + " hundred" + (" and " + remainder if remainder else "")

    result = []
    if num >= 1000000000:
        result.append(_convert_below_1000(num // 1000000000) + " billion")
        num %= 1000000000
    if num >= 1000000:
        result.append(_convert_below_1000(num // 1000000) + " million")
        num %= 1000000
    if num >= 1000:
        result.append(_convert_below_1000(num // 1000) + " thousand")
        num %= 1000
    if num > 0:
        result.append(_convert_below_1000(num))

    return " ".join(result)
