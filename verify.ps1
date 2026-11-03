# verify.ps1 - Windows wrapper around verify.py.
# Usage: right-click -> "Run with PowerShell"

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$env:PYTHONIOENCODING = 'utf-8'

$candidates = @(
    'D:\DSH\desktop-home\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe',
    'python', 'py'
)
foreach ($c in $candidates) {
    try { & $c -c "import numpy, pandas" 2>$null | Out-Null; & $c (Join-Path $here 'verify.py'); exit $LASTEXITCODE } catch { }
}
Write-Host 'No Python with numpy and pandas found. Install requirements.txt first.' -ForegroundColor Red
exit 1
