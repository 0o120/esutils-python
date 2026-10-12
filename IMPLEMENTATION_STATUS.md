# Implementation status

2.0.0 is prepared locally and unreleased. Audit items U01–U06 are addressed;
the focused utility scope remains explicit rather than expanding unsupported APIs.

Evidence on Python 3.11 and 3.12:

- New astral, invalid input and modern policy regression tests failed on baseline
  and pass after the repair.
- Eleven tests pass, including independent exhaustive classification over all
  1,114,112 code points for modern Unicode 17, legacy Unicode 9 ID properties,
  and the legacy BMP ES5 character categories (six predicates total).
- Vendored source SHA-256 and exact generated-content checks pass offline.
- ECMAScript whitespace/line terminator behavior and additions are checked.
- Source archive builds; wheel built from the archive passes metadata, retained
  Unicode license, clean extracted-wheel import and Python README examples.
- CI is configured for Python 3.11–3.15 on Linux and Windows, plus macOS 3.11/3.15;
  hosted workflows run on the modernization branch; see the
  [live GitHub CI evidence](https://github.com/0o120/esutils-python/actions).

Performance can be reproduced with `python tools/benchmark.py`. Runtime lookup
uses the ASCII fast path and logarithmic scalar interval search, with no regex
compilation or network. The generated tables occupy about 59 KiB of source.
Final paired CPython 3.12.0 source-only uninstrumented import was 14.9 ms
versus 24.4 ms for the old module. Validated modern ASCII classification runs
about 7.7 million operations/second on the measured workload, roughly 60% faster
than the first modern implementation. The old unchecked ASCII path was about
11.3 million/second; this investigated budget exception includes the new
type/scalar contract. Current legacy BMP classification is roughly comparable
to the old path. Old astral results are incorrect and cannot support a correctness
equivalence claim. Raw samples, source hashes and separate allocation results
are preserved in [performance.json](performance.json). These are local
measurements rather than cross-machine promises.

Limits: character predicates do not validate whole names, escapes or reserved
words. The upstream ast/keyword modules remain intentionally outside this port.
Legacy ES5/ES6 policies are explicitly Unicode 9; modern consumers must use the
new unqualified identifier predicates. Unicode updates require a deliberate
source/checksum/policy release. Shared parser/generator acceptance is coordinated
in the parent toolchain.
