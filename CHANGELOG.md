# Changelog

## 2.0.0 — unreleased

- Require Python 3.11+; retain focused `code` API and upstream author notices.
- Add explicit Unicode 17 modern identifier predicates with offline generated data.
- Repair Unicode 9 ES6 astral classification; preserve legacy ES5 BMP policy.
- Reject invalid scalar integers consistently and non-integers with `TypeError`.
- Replace surrogate-regex tables and internal pair conversion with scalar intervals.
- Add exhaustive source-data classification tests, checksum checks, package checks and CI.

Migration: choose `isIdentifierStart`/`isIdentifierPart` for the modern toolchain.
ES5/ES6 names remain Unicode 9 legacy policies. `fromCodePoint` returns one Python
scalar rather than a surrogate pair; invalid values now raise `ValueError`.
