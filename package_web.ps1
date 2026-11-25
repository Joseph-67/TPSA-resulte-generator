$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$release = "dist\TPSA-Result-Manager-Web"
$releaseZip = "dist\TPSA-Result-Manager-Web.zip"
New-Item -ItemType Directory -Force -Path $release | Out-Null
Copy-Item -Force web_app.py, desktop_app.py, grade.py, tpsa.db, tpsa_logo.png, Report_Card_Template.xlsx, requirements.txt, run_web.ps1 -Destination $release
Copy-Item -Recurse -Force classes, templates, static, template, subjectsfolder -Destination $release
if (Test-Path $releaseZip) { Remove-Item -Force $releaseZip }
Compress-Archive -Force -Path $release -DestinationPath $releaseZip
Write-Host "Web/PWA package created: dist\TPSA-Result-Manager-Web.zip"
