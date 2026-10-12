# Implementation status

2.0.0 is prepared locally and unreleased. Audit items U01–U06 are addressed;
the focused utility scope remains explicit rather than expanding unsupported APIs.

Evidence on Python 3.11 and 3.12:

- New astral, invalid input and modern policy regression tests failed on baseline
  and pass after the repair.
- Fourteen tests pass, including independent exhaustive classification over all
  1,114,112 code points for modern Unicode 17, legacy Unicode 9 ID properties,
  and the legacy BMP ES5 character categories (six predicates total).
- Vendored source SHA-256 and exact generated-content checks pass offline.
- ECMAScript whitespace/line terminator behavior and additions are checked.
- Source archive builds; wheel built from the archive passes metadata, retained
  Unicode license, clean extracted-wheel import and Python README examples.
- CI is configured for Python 3.11–3.15 on Linux and Windows, plus macOS 3.11/3.15;
  hosted workflows run on the modernization branch; see the
  [live GitHub CI evidence](https://github.com/0o120/esutils-python/actions).

Runtime lookup uses compact ASCII sets and logarithmic scalar interval search,
with no regex compilation or network; generated tables occupy about 59 KiB.
Round-two public identifier ASCII checks take 11–13% less time than the modern
starting implementation. Strict public type/scalar validation retains a gap
against the old unchecked API. Five private ord-derived helpers remove duplicate
checks in coordinated generator joins; whitespace/line pairs take 72–74% less
time than modern-start public checks and 43–62% less than old public checks.
Every trusted helper matches its public policy across all chr/ord values,
including surrogates. [Performance evidence](PERFORMANCE.md) records exact
old/start/current samples, classification differences and earlier separate
startup/allocation data. Old astral identifier results are incorrect.

Limits: character predicates do not validate whole names, escapes or reserved
words. The upstream ast/keyword modules remain intentionally outside this port.
Legacy ES5/ES6 policies are explicitly Unicode 9; modern consumers must use the
new unqualified identifier predicates. Unicode updates require a deliberate
source/checksum/policy release. Shared parser/generator acceptance is coordinated
in the parent toolchain.
