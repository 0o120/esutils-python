"""Exhaustively compare scalar classification against the pinned source data."""
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from esutils import code
from esutils._unicode_data import SOURCE_SHA256

ROOT = Path(__file__).resolve().parents[1]


def reference(version):
    start, part = bytearray(0x110000), bytearray(0x110000)
    source = ROOT / "data" / "unicode" / version / "DerivedCoreProperties.txt"
    raw = source.read_bytes()
    if sha256(raw).hexdigest() != SOURCE_SHA256[f"{version}/DerivedCoreProperties.txt"]:
        raise AssertionError("Vendored Unicode property source differs")
    for line in raw.decode("utf-8").splitlines():
        content = line.split("#", 1)[0].strip()
        if not content:
            continue
        span, property_name, *_ = (field.strip() for field in content.split(";"))
        target = start if property_name == "ID_Start" else part if property_name == "ID_Continue" else None
        if target is None:
            continue
        values = span.split("..")
        first, last = int(values[0], 16), int(values[-1], 16)
        target[first:last + 1] = b"\x01" * (last - first + 1)
    for cp in (0x24, 0x5F):
        start[cp] = part[cp] = 1
    part[0x200C] = part[0x200D] = 1
    return start, part


class UnicodePropertiesTests(unittest.TestCase):
    def test_all_modern_and_legacy_scalar_codepoints(self):
        for version, start_fn, part_fn in (("17.0.0", code.isIdentifierStart, code.isIdentifierPart),
                ("9.0.0", code.isIdentifierStartES6, code.isIdentifierPartES6)):
            expected_start, expected_part = reference(version)
            for cp in range(0x110000):
                if start_fn(cp) != bool(expected_start[cp]) or part_fn(cp) != bool(expected_part[cp]):
                    self.fail(f"Unicode {version} predicate mismatch at U+{cp:04X}")

    def test_all_legacy_bmp_categories(self):
        start, part = bytearray(0x110000), bytearray(0x110000)
        first = None
        for line in (ROOT / "data/unicode/9.0.0/UnicodeData.txt").read_text(encoding="utf-8").splitlines():
            point, name, category, *_ = line.split(";")
            cp = int(point, 16)
            if name.endswith(", First>"):
                first = cp
                continue
            low = cp if first is None else first
            first = None
            if low > 0xFFFF:
                continue
            if category in ("Lu", "Ll", "Lt", "Lm", "Lo", "Nl"):
                start[low:cp + 1] = b"\x01" * (cp - low + 1)
                part[low:cp + 1] = b"\x01" * (cp - low + 1)
            elif category in ("Mn", "Mc", "Nd", "Pc"):
                part[low:cp + 1] = b"\x01" * (cp - low + 1)
        for cp in (0x24, 0x5F):
            start[cp] = part[cp] = 1
        part[0x200C] = part[0x200D] = 1
        for cp in range(0x110000):
            if code.isIdentifierStartES5(cp) != bool(start[cp]) or code.isIdentifierPartES5(cp) != bool(part[cp]):
                self.fail(f"Legacy ES5 category mismatch at U+{cp:04X}")

    def test_generated_tables_are_reproducible(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/generate_unicode.py"), "--check"],
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
