$ErrorActionPreference = "Stop"
$python = "python"
$venvPython = "$PSScriptRoot\..\.venv\Scripts\python.exe"
$codexPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path $venvPython) { $python = $venvPython }
elseif (Test-Path $codexPython) { $python = $codexPython }
& $python -m pip install -r "$PSScriptRoot\..\requirements.txt"
& $python "$PSScriptRoot\data\preprocess.py"
Write-Host "智维引擎已启动: http://127.0.0.1:8000" -ForegroundColor Cyan
& $python "$PSScriptRoot\backend\main.py"
