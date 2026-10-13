# Performance evidence

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
