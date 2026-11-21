# Keras docstring regression tests

A small automated regression-test contribution for [keras-io issue #2422](https://github.com/keras-team/keras-io/issues/2422), prepared for USC CSCI-566 Deep Learning.

## Problem and contribution

Some preprocessing-layer API pages render ordinary prose and section labels as code. Shared examples are injected at column zero into otherwise indented docstrings, preventing the original documentation renderer from removing the surrounding indentation correctly.

This project contributes **four original automated tests** through the real Keras documentation renderer:

| Test | What it checks | Baseline | PR #2423 |
| --- | --- | --- | --- |
| Prose | Ordinary text becomes a paragraph, not code | Fail | Pass |
| Sections | Arguments and Example labels, plus the argument list, are recognized | Fail | Pass |
| Example indentation | Nested example code retains its exact text and indentation | Pass | Pass |
| Ordinary docstrings | A normal docstring retains its expected Markdown output | Pass | Pass |

**Baseline: 2 passed, 2 failed. Existing PR #2423: 4 passed.** The baseline failures are intentional demonstrations of the bug. The other two tests protect behavior already working before the fix.

These tests use synthetic docstrings, not neural-network training. They do not establish augmentation correctness, model accuracy, or generalization. The connection to deep learning is clearer documentation for preprocessing and data augmentation APIs.

## Attribution and AI assistance

**Shubham Pandey (`pandeyshub-byte`) wrote the production fix in [PR #2423](https://github.com/keras-team/keras-io/pull/2423). My contribution is the automated regression tests, not that fix.** The reviewed PR contains the parser change and manually reported checks, but no automated test file. No tests were copied from it.

AI assisted with development, explanations, and test execution. I reviewed the tests and verified the recorded results. The original development history and the upstream fix are attributed separately; no new production fix is claimed here.

## Pinned versions

- Baseline keras-io commit: `f5891b3cd4df69f6bd5a3c26ea92310f3a973626`
- PR #2423 commit: `2049298dd41b71c3a5e3ff0290a6681335aa75a9`
- Verified interpreter: Python **3.11.18**.
- Direct dependencies: pytest **9.2.0**, Black **26.10.1**, Markdown **3.11.3**.

Black is also imported by the upstream renderer for signatures. TensorFlow, Keras, JAX, GPU packages, and datasets are not needed. Exact installed transitive versions are saved with the evidence.

## Reproduce on Windows PowerShell

Prerequisites: Python 3.11 available as `python`, an internet connection, and this project as the current directory. The following commands create the environment outside the project folder. They do not activate an environment, change system settings, or run Git commands.

```powershell
python --version
$work = Join-Path ([System.IO.Path]::GetTempPath()) ("keras-docstring-verify-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $work | Out-Null
python -m venv "$work\venv"
$python = Join-Path $work "venv\Scripts\python.exe"
& $python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
& $python -B scripts/reproduce.py
```

The script downloads only three unmodified upstream Python modules at each exact commit into temporary directories, then runs this same test file in separate processes. It removes the downloaded sources when finished. No cloned repositories are needed.

The baseline pytest process should exit **1**, and the PR process **0**. The reproduction script exits **0 only if both runs have the exact expected test outcomes**. Unexpected failures, skips, collection errors, or different results cause it to fail. A message that optional KerasHub is unavailable is expected; preset rendering is not used.

Fresh outputs, source URLs/hashes, commands, environment overrides, dependency versions, and JUnit XML are written to `evidence/reproduced/`. Re-running replaces those files; copy them first if you want to preserve a previous run. The temporary virtual environment remains at `$work` for inspection and can be removed later.

## Evidence and scope

- `evidence/original/`: verbatim selected outputs from the original local study, including the two SHAs, test logs, JUnit XML, rendered Markdown, Python version, and dependency lock. These may contain original local paths.
- `evidence/reproduced/`: fresh verification of these packaged tests and pinned upstream sources.
- `evidence/readme-verification.txt`: output from running the README commands in a new environment.
- `evidence/verification-summary.txt`: final integrity and preparation checks.

The source test file is copied unchanged from the original project. Only the small documentation-rendering path is exercised; this is not a complete website build or an all-layer integration suite. HTML assertions use Python-Markdown's `fenced_code` extension, not the full site's rendering extensions. Similar tests may exist elsewhere; originality is assessed relative to the reviewed PR and this project's development history.

Original setup/development commands were partly reconstructed rather than preserved as a continuous terminal recording. The new reproduction saves its actual command arguments, outputs, and return codes directly.
