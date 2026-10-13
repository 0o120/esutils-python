"""Identifier fast paths preserve scalar/type contracts and legacy policies."""
from enum import IntEnum
import unittest

from esutils import code

PREDICATES = (
    code.isIdentifierStart, code.isIdentifierPart,
    code.isIdentifierStartES5, code.isIdentifierPartES5,
    code.isIdentifierStartES6, code.isIdentifierPartES6,
)


class CodePoint(int):
    pass


class NamedPoint(IntEnum):
    LETTER = 65
    DIGIT = 48
    INVALID = -1


class AsciiFastPathTests(unittest.TestCase):
    def test_ascii_grammar_results(self):
        starts = set(map(ord, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$_'))
        parts = starts | set(map(ord, '0123456789'))
        for predicate in PREDICATES:
            expected = parts if 'Part' in predicate.__name__ else starts
            for cp in range(128):
                self.assertIs(predicate(cp), cp in expected)

    def test_int_subclasses_and_enums_keep_scalar_contract(self):
        points = (-63, -1, 0, 36, 48, 65, 95, 127, 233, 0x0300, 0x10400, 0xD800, 0xDFFF, 0x110000)
        for predicate in PREDICATES:
            for point in points:
                with self.subTest(predicate=predicate.__name__, point=point):
                    self.assertIs(predicate(CodePoint(point)), predicate(point))
            for point in NamedPoint:
                self.assertIs(predicate(point), predicate(int(point)))

    def test_invalid_inputs_cannot_index_ascii_table(self):
        for predicate in PREDICATES:
            for value in (True, False, None, 'A', 65.0, b'A'):
                with self.subTest(predicate=predicate.__name__, value=value), self.assertRaises(TypeError):
                    predicate(value)
            for value in (-1, -128, -0x110000, 0xD800, 0xDFFF, 0x110000, 10 ** 100):
                with self.subTest(predicate=predicate.__name__, value=value):
                    self.assertIs(predicate(value), False)


if __name__ == '__main__':
    unittest.main()
