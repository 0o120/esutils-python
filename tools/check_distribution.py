"""Verify distribution contents, metadata and clean-wheel README examples."""
import argparse
import ast
import email
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    version_source = ast.parse((ROOT / "esutils/_version.py").read_text(encoding="utf-8"))
    expected_version = next(ast.literal_eval(statement.value) for statement in version_source.body
                            if isinstance(statement, ast.Assign)
                            and any(isinstance(target, ast.Name) and target.id == "__version__"
                                    for target in statement.targets))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert all(target.startswith(("https://", "http://", "#"))
               for target in re.findall(r"\]\(([^)]+)\)", readme)), "README links must work on PyPI"
    wheel = max(args.dist.glob("*.whl"), key=lambda path: path.stat().st_mtime)
    with zipfile.ZipFile(wheel) as archive:
        metadata = email.message_from_bytes(archive.read(next(name for name in archive.namelist() if name.endswith("/METADATA"))))
        assert metadata["Name"] == "esutils"
        assert metadata["Version"] == expected_version
        assert metadata["Requires-Python"] == project["requires-python"]
        assert metadata["License-Expression"] == project["license"]
        assert metadata["Description-Content-Type"] == "text/markdown"
        assert set(metadata.get_all("Classifier", [])) == set(project["classifiers"])
        assert set(metadata.get_all("Project-URL", [])) == {
            f"{name}, {url}" for name, url in project["urls"].items()}
        assert metadata.get_payload().strip() == readme.strip()
        assert not metadata.get_all("Requires-Dist")
        assert any(name.endswith("licenses/data/unicode/LICENSE.txt") for name in archive.namelist())
        assert not any("__pycache__" in name or name.startswith(("tests/", "data/")) for name in archive.namelist())
        with tempfile.TemporaryDirectory() as folder:
            archive.extractall(folder)
            examples = re.findall(r"```python\n(.*?)```", readme, re.S)
            script = ("import sys\nsys.path.insert(0, sys.argv[1])\nimport esutils\n"
                      f"assert esutils.__version__ == {expected_version!r}\n" + "\n".join(examples))
            subprocess.run([sys.executable, "-I", "-B", "-c", script, folder], cwd=folder, check=True)
    assert (args.dist / f"esutils-{expected_version}.tar.gz").is_file(), "Source distribution missing"
    print("Source archive, wheel metadata, Unicode license, clean imports and README examples verified")


if __name__ == "__main__":
    main()
