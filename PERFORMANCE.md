# Performance evidence

## Post-gap performance audit — October 2026

Exact built-in integers use direct digit and whitespace/line-terminator
checks, avoiding repeated scalar validation. Other inputs retain the existing
validation path, including integer subclasses and enums. Booleans still raise
`TypeError`; invalid/out-of-range values and surrogates remain false. Bounded
comparisons avoid hashing enormous invalid integers. Identifier tables and
Unicode policies are unchanged.

| Mixed public predicate batch | Before, milliseconds | After, milliseconds | Less time |
| --- | ---: | ---: | ---: |
| ASCII | 25.789 | 15.541 | 39.7% |
| Unicode | 39.506 | 27.088 | 31.4% |

These batches mix identifier, digit and spacing predicates; unchanged identifier
predicates are included. All 40 test methods and 216 subtests pass on CPython
3.11-3.15, including exhaustive Unicode checks and scalar/type boundary tests.

Measurements use CPython 3.12.0 on Windows, default garbage collection and
sequential alternating before/after processes. Large-file figures are medians
of three fresh processes per version. Component figures use three fresh
processes per version, seven warmed calls per process and the median of process
medians. All raw samples, including outliers and small regressions, are retained.
Imports, input reading and correctness comparisons are outside timing windows.

Reproduction scripts, exact Python source hashes, profiles, logs, environments,
and distributions are outside the repositories in
`C:/Users/Ryzen/Benchmarks/toolchain-performance-2026-10-13/`.
The report covers first-call/allocation costs, compatibility fallbacks and
Python 3.11/3.15 boundary timings as well as the main comparisons. These are
workload-specific results, not a universal speed guarantee.

## Earlier performance work

This round compares original master (`ce16f4e`), modern starting implementation
(`6e32e20`), and current runtime (`1e85352`). [performance-round2.json](performance-round2.json)
contains exact source hashes, seven timing samples per case, classifications,
and all fifteen policy/workload comparisons.

CPython 3.12.0 / Windows; uninstrumented batches of 800,000 ASCII or 400,000 BMP
or 300,000 astral checks. Import and explicit garbage collection are excluded:

| ASCII operation pair | Old seconds | Modern start seconds | Current seconds |
| --- | ---: | ---: | ---: |
| Public legacy identifier start/part | 0.0729 | 0.1081 | 0.0942 |
| Public Unicode17 identifier start/part | Unavailable | 0.1095 | 0.0977 |
| Trusted ord identifier start/part | 0.0729* | 0.1073* | 0.0753 |
| Public whitespace/line terminator | 0.1063 | 0.2462 | 0.2417 |
| Trusted ord whitespace/line terminator | 0.1151* | 0.2468* | 0.0652 |

Starred rows compare earlier public predicates with the new private trusted
path on identical valid ASCII inputs. Public legacy ASCII checks take 12.9%
less time than the modern starting version, but remain about 29% above the old
unchecked API. Public Unicode17 ASCII improves 10.8%; BMP changes are within
about 1% in this sample. Old astral identifier results are wrong and some BMP
policy results differ, so the raw evidence flags those classification mismatches.

Trusted identifier paths take 30% less time on ASCII and about 42% less time
on BMP/astral than the earlier modern public path. Trusted whitespace/line
checks take 72–74% less time than modern-start public checks and 43–62% less
than the corresponding old public checks. They remove duplicate validation
inside the coordinated generator's character joins.

The five private helpers require exact integers obtained from
`ord(one_python_character)`. Their identifier policy is Unicode17; all surrogate
values remain false. Exhaustive comparison covers every one of the 1,114,112
chr/ord values. They are excluded from `__all__` and do not change the public
integer/subclass/bool/invalid-scalar contract. External callers should use the
public APIs.

The earlier import/allocation investigation remains in
[performance.json](performance.json). Its uninstrumented source-only imports
were about 14.9 ms versus 24.4 ms old; those measurements predate this round.
Local timings vary across machines and do not promise a universal speed ratio.

Archived measurements use `<workspace>/` for the original checkout root;
machine-specific absolute paths have been removed. Timing samples, source
hashes and classifications retain their recorded values; error diagnostics
use the same portable path marker.
