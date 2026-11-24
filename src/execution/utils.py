"""Utility function to make read/write smaller in db"""


def compress_string(s: str) -> str:
    """Converts a number written in base 2 to a number written in base 16. Adds a 1 at the beginning to avoid loosing leading zeros

    :param s: The number to convert
    :type s: str
    :return: s in base 16
    :rtype: string"""
    if s == "":
        return s
    s = "1" + s
    return format(int(s, 2), "x")


def decompress_string(s: str) -> str:
    """Converts a number written in base 16 to a number written in base 2.
    Removes the 1 at the start that was

    :param s: The number to convert
    :type s: str
    :return: s in base 2
    :rtype: string"""
    if s == "":
        return s
    s = format(int(s, 16), "b")
    if s[0] != "1":
        raise ValueError(
            "String given as input wasn't compress using compress_string"
        )
    return s[1 : len(s)]
