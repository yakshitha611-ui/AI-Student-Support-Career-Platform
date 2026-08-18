$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path '.\.venv')) {
    py -3 -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --disable-pip-version-check -r .\requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8001
