# Contributing

Use Python 3.11+ and an isolated development environment:

```console
python -m venv .venv
python -m pip install --require-hashes -r requirements-dev.lock
python -m unittest discover -s tests -v
python tools/generate_unicode.py --check
python -m build --no-isolation
python tools/check_distribution.py
```

Activate `.venv` using the platform's normal activation command before installing.
The tests independently check all scalar code points against vendored source
properties and legacy categories. Unicode changes require source revision,
checksum/provenance/license updates, deterministic regeneration and all-scalar
verification. Never make behavior depend on the Python Unicode database.

The build creates a source archive, then its wheel from that archive. The checker
validates metadata, imports from a clean extracted wheel and runs Python README
examples outside the source checkout. Keep the focused API scope and legacy
policy explicit. Do not publish until the coordinated toolchain and supported
Python CI pass. Regenerate locked tools deliberately with `uv pip compile
requirements-dev.in --universal --generate-hashes --output-file requirements-dev.lock`.
