from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
backend_dir = Path(__file__).resolve().parent
venv_dir = root / '.venv'

if not venv_dir.exists():
    subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)

python_exe = venv_dir / 'Scripts' / 'python.exe'
if not python_exe.exists():
    raise FileNotFoundError(f'Virtualenv Python not found: {python_exe}')

subprocess.run([
    str(python_exe),
    '-m', 'pip', 'install', '--disable-pip-version-check', '-r', str(backend_dir / 'requirements.txt')
], check=True)

os.chdir(backend_dir)
subprocess.run([
    str(python_exe),
    '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8001'
], check=True)
