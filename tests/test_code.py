import unittest
from esutils import code


class CodeTests(unittest.TestCase):
    def test_legacy_astral(self):
        for cp in (0x10400, 0x1D400):
            self.assertTrue(code.isIdentifierStartES6(cp))
            self.assertTrue(code.isIdentifierPartES6(cp))
            self.assertFalse(code.isIdentifierStartES5(cp))

    def test_modern_unicode(self):
        self.assertEqual(code.UNICODE_VERSION, "17.0.0")
        self.assertTrue(code.isIdentifierStart(0x1C90))
        self.assertFalse(code.isIdentifierStartES6(0x1C90))
        self.assertTrue(code.isIdentifierStart(ord("$")))
        self.assertTrue(code.isIdentifierStart(ord("_")))
        for cp in (ord("0"), 0x0300, 0x200C, 0x200D):
            self.assertFalse(code.isIdentifierStart(cp))
            self.assertTrue(code.isIdentifierPart(cp))
        self.assertFalse(code.isIdentifierPart(0x1F600))

    def test_invalid_code_points(self):
        predicates = (code.isIdentifierStartES5, code.isIdentifierPartES5,
            code.isIdentifierStartES6, code.isIdentifierPartES6)
        for predicate in predicates:
            for cp in (-63, -1, 0x110000, 0xD800, 0xDFFF):
                self.assertFalse(predicate(cp))
            for cp in ("x", 1.0, None, True):
                with self.assertRaises(TypeError):
                    predicate(cp)

    def test_identifier_integer_subclasses_do_not_require_hashability(self):
        class CodePoint(int):
            def __hash__(self):
                raise AssertionError("Scalar predicates must not hash integer subclasses")
        predicates = (code.isIdentifierStart, code.isIdentifierPart,
            code.isIdentifierStartES5, code.isIdentifierPartES5,
            code.isIdentifierStartES6, code.isIdentifierPartES6)
        for predicate in predicates:
            for cp in (36, 65, 95, 233, 0x10400, -1, 0xD800, 0x110000):
                self.assertEqual(predicate(CodePoint(cp)), predicate(cp))
            for invalid in (True, False, 65.0, [], {}, "A", None):
                with self.assertRaises(TypeError):
                    predicate(invalid)

    def test_private_ord_paths_match_public_unicode17_policy_exhaustively(self):
        for cp in range(0x110000):
            # ord(chr(cp)) also models unpaired surrogates in Python strings.
            value = ord(chr(cp))
            if code._identifier_start_from_ord(value) != code.isIdentifierStart(cp):
                self.fail(f"Private start policy differs at U+{cp:04X}")
            if code._identifier_part_from_ord(value) != code.isIdentifierPart(cp):
                self.fail(f"Private part policy differs at U+{cp:04X}")

    def test_scalar_predicates_accept_unhashable_integer_subclasses(self):
        class CodePoint(int):
            __hash__ = None

        predicates = (code.isWhiteSpace, code.isLineTerminator,
                      code.isDecimalDigit, code.isHexDigit, code.isOctalDigit,
                      code.isIdentifierStart, code.isIdentifierPart,
                      code.isIdentifierStartES5, code.isIdentifierPartES5,
                      code.isIdentifierStartES6, code.isIdentifierPartES6)
        for predicate in predicates:
            for point in (-1, 0, 9, 10, 11, 12, 13, 32, 48, 65, 95, 0x85,
                          0xA0, 0x1680, 0x180E, 0x2000, 0x200A, 0x2028,
                          0x2029, 0x202F, 0x205F, 0x3000, 0xD800, 0xFEFF,
                          0x10400, 0x10FFFF, 0x110000):
                with self.subTest(predicate=predicate.__name__, point=point):
                    self.assertIs(predicate(CodePoint(point)), predicate(point))

    def test_whitespace_and_line_predicates_do_not_invoke_hash_hooks(self):
        class CodePoint(int):
            def __hash__(self):
                raise AssertionError('Code-point predicates must not hash inputs')

        for predicate in (code.isWhiteSpace, code.isLineTerminator):
            for point in range(0x100):
                self.assertIs(predicate(CodePoint(point)), predicate(point))

    def test_private_ord_boundary_paths_match_public_policy_exhaustively(self):
        pairs = ((code._white_space_from_ord, code.isWhiteSpace),
            (code._line_terminator_from_ord, code.isLineTerminator),
            (code._decimal_digit_from_ord, code.isDecimalDigit))
        for cp in range(0x110000):
            for private, public in pairs:
                if private(ord(chr(cp))) != public(cp):
                    self.fail(f"Private {private.__name__} differs at U+{cp:04X}")

    def test_from_code_point_returns_scalar(self):
        self.assertEqual(code.fromCodePoint(0x10400), chr(0x10400))
        for cp in (-1, 0x110000, 0xD800):
            with self.assertRaises(ValueError):
                code.fromCodePoint(cp)

    def test_ecmascript_whitespace(self):
        for cp in (0x20, 0xA0, 0xFEFF, 0x3000):
            self.assertTrue(code.isWhiteSpace(cp))
        for cp in (0x180E, 0x85, 0x2028, 0x2029):
            self.assertFalse(code.isWhiteSpace(cp))
        for cp in (0xA, 0xD, 0x2028, 0x2029):
            self.assertTrue(code.isLineTerminator(cp))


if __name__ == "__main__":
    unittest.main()
