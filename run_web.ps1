$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python -m pip install -r requirements.txt
$env:TPSA_DATABASE = Join-Path $PSScriptRoot "tpsa.db"
python web_app.py
