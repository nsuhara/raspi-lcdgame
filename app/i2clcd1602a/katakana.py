"""i2clcd1602a/katakana.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""

SP_CODE = 0xfec0


def convert(message):
    """convert
    """
    converted = []
    for char in message:
        if ord(char) > SP_CODE:
            converted.append(chr(ord(char)-SP_CODE))
        else:
            converted.append(char)
    return ''.join(converted)
