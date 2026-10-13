"""Small reproducible startup/lookup benchmark; no optional dependencies."""
from pathlib import Path
import subprocess
import sys
import timeit

root = str(Path(__file__).resolve().parents[1])
code = f"import sys,time;sys.path.insert(0,{root!r});t=time.perf_counter();import esutils;print(time.perf_counter()-t)"
imports = [float(subprocess.check_output([sys.executable, "-I", "-c", code], text=True)) for _ in range(10)]
sys.path.insert(0, root)
from esutils import code as predicates
ascii_time = timeit.timeit(lambda: predicates.isIdentifierPart(0x61), number=1_000_000)
scalar_time = timeit.timeit(lambda: predicates.isIdentifierStart(0x10400), number=1_000_000)
print(f"Fresh import minimum: {min(imports) * 1000:.3f} ms")
print(f"1,000,000 ASCII lookups: {ascii_time:.3f} s")
print(f"1,000,000 astral lookups: {scalar_time:.3f} s")
