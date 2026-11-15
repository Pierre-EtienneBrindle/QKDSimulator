"""Utility function to make read/write smaller in db"""


def base_2_to_base_16(s: str) -> str:
    """Converts a number written in base 2 to a number written in base 16

    :param s: The number to convert
    :type s: str
    :return: s in base 16
    :rtype: string"""
    if s == "":
        return s
    return format(int(s, 2), "x")


def base_16_to_base_2(s: str) -> str:
    """Converts a number written in base 16 to a number written in base 2

    :param s: The number to convert
    :type s: str
    :return: s in base 2
    :rtype: string"""
    if s == "":
        return s
    return format(int(s, 16), "b")
