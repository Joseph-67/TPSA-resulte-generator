$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm TPSA-Result-Manager.spec
Write-Host ""
Write-Host "Desktop package created in dist\TPSA Result Manager.exe"
