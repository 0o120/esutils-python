# esutils

Pure Python character utilities for ECMAScript language tools. Python 3.11+;
no runtime dependencies or network calls. This remains a focused partial port
of [estools/esutils](https://github.com/estools/esutils): the `code` module is
provided; upstream `ast` and `keyword` APIs are not ported.

```console
python -m pip install esutils
```

## Upgrading from 1.x

Version 2.0 requires Python 3.11 or newer. Choose the unqualified identifier
predicates for Unicode 17; the ES5/ES6 names retain explicit Unicode 9 policies.
Predicates reject invalid integer scalars with `False` and reject non-integer
inputs, including bool, with `TypeError`. `fromCodePoint` returns one Python
scalar character and raises `ValueError` for invalid scalar integers. See the
[migration notes](https://github.com/0o120/esutils-python/blob/master/CHANGELOG.md).
The distribution and import name remain `esutils`; `esutils.__version__` is the
distribution version string.

## Usage

```python
from esutils import code
assert code.UNICODE_VERSION == "17.0.0"
assert code.isIdentifierStart(0x10400)
assert code.isIdentifierStart(0x1C90)
assert code.isIdentifierPart(0x200C)
assert not code.isIdentifierStart(0x200C)
assert not code.isIdentifierPart(0x1F600)
assert code.isWhiteSpace(0xFEFF)
assert not code.isWhiteSpace(0x180E)
```

| API | Policy |
| --- | --- |
| `isIdentifierStart(cp)` | Unicode **17.0.0** `ID_Start` plus `$` and `_` |
| `isIdentifierPart(cp)` | Unicode **17.0.0** `ID_Continue` plus `$`, `_`, ZWNJ and ZWJ |
| `isIdentifierStartES6(cp)`, `isIdentifierPartES6(cp)` | Legacy Unicode **9.0.0** ID properties; astral scalar behavior repaired |
| `isIdentifierStartES5(cp)`, `isIdentifierPartES5(cp)` | Legacy Unicode **9.0.0** BMP ES5 categories and ECMAScript additions |
| `isDecimalDigit(cp)`, `isHexDigit(cp)`, `isOctalDigit(cp)` | ASCII numeric-literal digits |
| `isWhiteSpace(cp)` | ECMAScript whitespace; excludes line terminators and U+180E |
| `isLineTerminator(cp)` | LF, CR, U+2028 and U+2029 |
| `fromCodePoint(cp)` | One Python scalar character; invalid scalars raise `ValueError` |

Inputs are integer Unicode scalar code points, such as `ord(character)`.
Integer subclasses are accepted and do not need to be hashable.
Predicates return `False` for negative integers, values above U+10FFFF and
surrogates. Non-integers (including bool) raise `TypeError` consistently.
`fromCodePoint` returns one Python character for astral inputs; it is not a
JavaScript UTF-16 surrogate-pair helper.

The modern policy is explicit, reproducible Unicode 17 acceptance for the
ECMAScript 2026 toolchain. ES5/ES6 names preserve the previous package's Unicode
9 policy. Edition names do not imply that a particular Unicode version is
required by every implementation of that edition. Character classification
does not validate full identifier names, escapes, reserved words or contextual
keywords. Python's `str.isidentifier()` and `isspace()` use different rules and
are not used.

Generated scalar intervals use binary search with an ASCII fast path. Checked-in
source files, exact SHA-256 checksums and the offline generator are documented
in [data provenance](https://github.com/0o120/esutils-python/blob/master/data/unicode/README.md). Results are independent of the
Python interpreter's Unicode database. Unicode updates require deliberate releases.

See [contributor instructions](https://github.com/0o120/esutils-python/blob/master/CONTRIBUTING.md),
[migration notes](https://github.com/0o120/esutils-python/blob/master/CHANGELOG.md)
and [CI results](https://github.com/0o120/esutils-python/actions).
Maintainers can follow the
[release instructions](https://github.com/0o120/esutils-python/blob/master/RELEASING.md).

[Performance measurements](https://github.com/0o120/esutils-python/blob/master/PERFORMANCE.md) document the public validation cost
and the private ord paths used by the coordinated toolchain. Public API
validation and Unicode policies remain unchanged.
