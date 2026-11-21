python --version
$work = Join-Path ([System.IO.Path]::GetTempPath()) ("keras-docstring-verify-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $work | Out-Null
python -m venv "$work\venv"
$python = Join-Path $work "venv\Scripts\python.exe"
& $python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
& $python -B scripts/reproduce.py

