"""Reproduce four tests against pinned, unmodified upstream parser sources."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
COMMITS = {
    "baseline": "f5891b3cd4df69f6bd5a3c26ea92310f3a973626",
    "pr-2423": "2049298dd41b71c3a5e3ff0290a6681335aa75a9",
}
MODULES = ("docstrings.py", "render_presets.py", "hub_master.py")
TEST_NAMES = (
    "test_injected_prose_is_a_paragraph_not_code",
    "test_injected_sections_are_recognized",
    "test_injected_example_preserves_exact_indentation",
    "test_normal_docstring_output_is_unchanged",
)


def main():
    if sys.version_info[:2] != (3, 11):
        raise SystemExit("Use Python 3.11 for the recorded reproduction environment.")
    output = ROOT / "evidence" / "reproduced"
    output.mkdir(parents=True, exist_ok=True)
    installed = sorted(
        f"{package.metadata['Name']}=={package.version}"
        for package in importlib.metadata.distributions()
    )
    (output / "requirements-lock.txt").write_text("\n".join(installed) + "\n", encoding="utf-8")
    record = {
        "python": sys.version, "platform": platform.platform(),
        "test_sha256": hashlib.sha256((ROOT / "tests/test_docstring_rendering.py").read_bytes()).hexdigest(),
        "runs": [],
    }
    success = True
    # Download only the real parser and its two local imports; no Git operations.
    with tempfile.TemporaryDirectory(prefix="keras-docstring-sources-") as temporary:
        for name, commit in COMMITS.items():
            checkout = Path(temporary) / name
            scripts = checkout / "scripts"
            scripts.mkdir(parents=True)
            sources = []
            for module in MODULES:
                url = f"https://raw.githubusercontent.com/keras-team/keras-io/{commit}/scripts/{module}"
                with urlopen(url, timeout=60) as response:
                    data = response.read()
                (scripts / module).write_bytes(data)
                sources.append({"url": url, "sha256": hashlib.sha256(data).hexdigest()})
            junit = output / f"{name}-junit.xml"
            command = [sys.executable, "-B", "-m", "pytest", "tests/test_docstring_rendering.py",
                       "-vv", "--tb=short", "--color=no", "-p", "no:cacheprovider",
                       f"--junitxml={junit}"]
            overrides = {"KERAS_IO_CHECKOUT": str(checkout), "PYTHONDONTWRITEBYTECODE": "1",
                         "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
            result = subprocess.run(command, cwd=ROOT, env=os.environ | overrides,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            (output / f"{name}-pytest.txt").write_text(result.stdout, encoding="utf-8")
            cases = ET.parse(junit).findall(".//testcase") if junit.exists() else []
            expected_failed = set(TEST_NAMES[:2]) if name == "baseline" else set()
            observed_failed = {case.attrib["name"] for case in cases if case.find("failure") is not None}
            valid = (
                result.returncode == (1 if name == "baseline" else 0)
                and len(cases) == 4
                and {case.attrib["name"] for case in cases} == set(TEST_NAMES)
                and observed_failed == expected_failed
                and all(case.find("error") is None and case.find("skipped") is None for case in cases)
            )
            record["runs"].append({"name": name, "commit": commit, "sources": sources,
                "cwd": str(ROOT), "argv": command, "environment": overrides,
                "exit_code": result.returncode, "failed_tests": sorted(observed_failed),
                "matches_expected": valid})
            success = success and valid
            print(result.stdout)
    record["matches_expected"] = success
    (output / "commands-and-results.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Both runs match the expected outcomes:", success)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
