# Implementation status

2.0.0 is prepared locally and unreleased. Audit items U01–U06 are addressed;
the focused utility scope remains explicit rather than expanding unsupported APIs.

Evidence on Python 3.11 and 3.12:

- New astral, invalid input and modern policy regression tests failed on baseline
  and pass after the repair.
- Eight tests pass, including independent exhaustive classification over all
  1,114,112 code points for modern Unicode 17, legacy Unicode 9 ID properties,
  and the legacy BMP ES5 character categories (six predicates total).
- Vendored source SHA-256 and exact generated-content checks pass offline.
- ECMAScript whitespace/line terminator behavior and additions are checked.
- Source archive builds; wheel built from the archive passes metadata, retained
  Unicode license, clean extracted-wheel import and Python README examples.
- CI is configured for Python 3.11–3.15 on Linux and Windows, plus macOS 3.11/3.15;
  remote CI has not
  been executed or published by this local implementation.

Performance can be reproduced with `python tools/benchmark.py`. Runtime lookup
uses the ASCII fast path and logarithmic scalar interval search, with no regex
compilation or network. The generated tables occupy about 59 KiB of source.
On Python 3.12, minimum fresh process import was 2.7 ms versus approximately
24 ms compiling/executing the old regex module. One million validated ASCII
lookups took 0.33 s (old unchecked indexing 0.11 s); BMP lookups took 0.50 s
(old regex 0.40 s); astral lookups took 0.49 s. These local measurements show the
cost of consistent scalar validation and are not cross-machine promises.

Limits: character predicates do not validate whole names, escapes or reserved
words. The upstream ast/keyword modules remain intentionally outside this port.
Legacy ES5/ES6 policies are explicitly Unicode 9; modern consumers must use the
new unqualified identifier predicates. Unicode updates require a deliberate
source/checksum/policy release. Shared parser/generator acceptance is coordinated
in the parent toolchain.
