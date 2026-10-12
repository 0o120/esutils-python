"""Verify distribution contents, metadata and clean-wheel README examples."""
import email
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with zipfile.ZipFile(next((ROOT / "dist").glob("*.whl"))) as archive:
        metadata = email.message_from_bytes(archive.read(next(name for name in archive.namelist() if name.endswith("/METADATA"))))
        assert metadata["Name"] == "esutils"
        assert metadata["Version"] == "2.0.0"
        assert metadata["Requires-Python"] == ">=3.11"
        assert not metadata.get_all("Requires-Dist")
        assert any(name.endswith("licenses/data/unicode/LICENSE.txt") for name in archive.namelist())
        assert not any("__pycache__" in name or name.startswith(("tests/", "data/")) for name in archive.namelist())
        with tempfile.TemporaryDirectory() as folder:
            archive.extractall(folder)
            examples = re.findall(r"```python\n(.*?)```", (ROOT / "README.md").read_text(encoding="utf-8"), re.S)
            script = "import sys\nsys.path.insert(0, sys.argv[1])\nimport esutils\nassert esutils.__version__ == '2.0.0'\n" + "\n".join(examples)
            subprocess.run([sys.executable, "-I", "-c", script, folder], cwd=folder, check=True)
    assert list((ROOT / "dist").glob("*.tar.gz")), "Source distribution missing"
    print("Source archive, wheel metadata, Unicode license, clean imports and README examples verified")


if __name__ == "__main__":
    main()
