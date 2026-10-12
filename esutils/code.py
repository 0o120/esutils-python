# Copyright (C) 2013-2014 Yusuke Suzuki <utatane.tea@gmail.com>
# Copyright (C) 2014 Ivan Nikulin <ifaaan@gmail.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# https://github.com/estools/esutils/blob/master/lib/code.js

"""ECMAScript character predicates using pinned, Python-native Unicode data."""
from bisect import bisect_right
from ._unicode_data import (
    UNICODE_VERSION, LEGACY_UNICODE_VERSION, ID_START, ID_CONTINUE,
    ES5_ID_START, ES5_ID_CONTINUE, ES6_ID_START, ES6_ID_CONTINUE,
)

__all__ = [
    "UNICODE_VERSION", "LEGACY_UNICODE_VERSION", "isDecimalDigit", "isHexDigit",
    "isOctalDigit", "isWhiteSpace", "isLineTerminator", "isIdentifierStart",
    "isIdentifierPart", "isIdentifierStartES5", "isIdentifierPartES5",
    "isIdentifierStartES6", "isIdentifierPartES6", "fromCodePoint",
]


def _valid(ch: int) -> bool:
    if isinstance(ch, bool) or not isinstance(ch, int):
        raise TypeError("A Unicode code point must be an integer, not bool")
    return 0 <= ch <= 0x10FFFF and not 0xD800 <= ch <= 0xDFFF


def isDecimalDigit(ch: int) -> bool:
    return _valid(ch) and 0x30 <= ch <= 0x39


def isHexDigit(ch: int) -> bool:
    return _valid(ch) and (0x30 <= ch <= 0x39 or 0x61 <= ch <= 0x66 or 0x41 <= ch <= 0x46)


def isOctalDigit(ch: int) -> bool:
    return _valid(ch) and 0x30 <= ch <= 0x37


_WHITE_SPACE = frozenset((0x9, 0xB, 0xC, 0x20, 0xA0, 0x1680,
    *range(0x2000, 0x200B), 0x202F, 0x205F, 0x3000, 0xFEFF))
_LINE_TERMINATORS = frozenset((0xA, 0xD, 0x2028, 0x2029))


def isWhiteSpace(ch: int) -> bool:
    return _valid(ch) and ch in _WHITE_SPACE


def isLineTerminator(ch: int) -> bool:
    return _valid(ch) and ch in _LINE_TERMINATORS


def fromCodePoint(cp: int) -> str:
    """Return one Python scalar character; invalid scalar values raise ValueError."""
    if not _valid(cp):
        raise ValueError(f"Invalid Unicode scalar code point: {cp!r}")
    return chr(cp)


_ASCII_START = tuple(0x61 <= cp <= 0x7A or 0x41 <= cp <= 0x5A or cp in (0x24, 0x5F) for cp in range(128))
_ASCII_PART = tuple(_ASCII_START[cp] or 0x30 <= cp <= 0x39 for cp in range(128))


def _identifier(ch: int, table: tuple[int, ...], ascii_table: tuple[bool, ...]) -> bool:
    if not _valid(ch):
        return False
    if ch < 128:
        return ascii_table[ch]
    return bool(bisect_right(table, ch) % 2)


def isIdentifierStart(ch: int) -> bool:
    """Unicode 17 ID_Start plus ECMAScript dollar and underscore additions."""
    return _identifier(ch, ID_START, _ASCII_START)


def isIdentifierPart(ch: int) -> bool:
    """Unicode 17 ID_Continue plus ECMAScript dollar, ZWNJ and ZWJ additions."""
    return _identifier(ch, ID_CONTINUE, _ASCII_PART)


def isIdentifierStartES5(ch: int) -> bool:
    """Legacy Unicode 9 BMP letter/Nl policy, matching the previous ES5 API."""
    return _identifier(ch, ES5_ID_START, _ASCII_START)


def isIdentifierPartES5(ch: int) -> bool:
    """Legacy Unicode 9 BMP ES5 categories and ECMAScript additions."""
    return _identifier(ch, ES5_ID_CONTINUE, _ASCII_PART)


def isIdentifierStartES6(ch: int) -> bool:
    """Legacy Unicode 9 ID_Start policy, including astral scalar characters."""
    return _identifier(ch, ES6_ID_START, _ASCII_START)


def isIdentifierPartES6(ch: int) -> bool:
    """Legacy Unicode 9 ID_Continue policy and ECMAScript additions."""
    return _identifier(ch, ES6_ID_CONTINUE, _ASCII_PART)
