# Unicode provenance

Sources are unchanged downloads of these Unicode Character Database files:

| Source | SHA-256 |
| --- | --- |
| [17.0.0 DerivedCoreProperties.txt](https://www.unicode.org/Public/17.0.0/ucd/DerivedCoreProperties.txt) | `24c7fed1195c482faaefd5c1e7eb821c5ee1fb6de07ecdbaa64b56a99da22c08` |
| [9.0.0 DerivedCoreProperties.txt](https://www.unicode.org/Public/9.0.0/ucd/DerivedCoreProperties.txt) | `6662c7e30b572df5d948c092692f52bcc79ab36d49a063a73d6435042db6fb3b` |
| [9.0.0 UnicodeData.txt](https://www.unicode.org/Public/9.0.0/ucd/UnicodeData.txt) | `68dfc414d28257b9b5d6ddbb8b466c768c00ebdf6cbf7784364a9b6cad55ee8f` |

Unicode data is copyright Unicode, Inc.; the applicable permission notice is
retained in [LICENSE.txt](LICENSE.txt). The original utility author notices
remain in `esutils/code.py`.

`python tools/generate_unicode.py` verifies checksums before creating
`esutils/_unicode_data.py`. `--check` verifies exact generated content offline.
Modern/ES6 tables use ID_Start/ID_Continue with ECMAScript additions. ES5 tables
use BMP categories Lu/Ll/Lt/Lm/Lo/Nl for starts, additionally Mn/Mc/Nd/Pc for
parts, plus `$`/`_` and ZWNJ/ZWJ as documented. Flat intervals alternate inclusive
starts and exclusive ends; `bisect_right(table, cp) % 2` implements membership.

Source distributions include source data and generator; wheels contain only the
small runtime tables and license notices. Tests independently parse the source
files and check every scalar code point against all three policies.
