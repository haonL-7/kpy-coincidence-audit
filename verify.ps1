# verify.ps1 - confirm the archive reproduces the manuscript's numbers.
# Usage: right-click -> "Run with PowerShell", or  powershell -ExecutionPolicy Bypass -File verify.ps1

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$env:PYTHONIOENCODING = 'utf-8'

if (-not (Test-Path (Join-Path $here 'tools'))) {
    Write-Host ''
    Write-Host 'No tools folder next to this script, so the archive has not been extracted here.' -ForegroundColor Red
    Write-Host ''
    Write-Host 'This folder currently contains:'
    Get-ChildItem $here | Select-Object -First 10 Name | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host 'Expected after extraction: CITATION.cff, LICENSE, README.md, VERIFY.md, data, figs, requirements.txt, tools'
    Write-Host ''
    Write-Host 'Fix: unzip the Zenodo archive into THIS folder, then run this script again.'
    exit 1
}

# pick an interpreter: bundled runtime first, then python on PATH
$candidates = @(
    'D:\DSH\desktop-home\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe',
    'python', 'py'
)
$py = $null
foreach ($c in $candidates) {
    try { & $c -c "import numpy, pandas" 2>$null; $py = $c; break } catch { }
}
if (-not $py) { Write-Host 'No Python with numpy and pandas found. Install requirements.txt first.' -ForegroundColor Red; exit 1 }

Write-Host ("Interpreter: " + $py) -ForegroundColor Cyan
Write-Host ""

function Check($label, $script, $mustContain) {
    Write-Host ("== " + $label + " ==") -ForegroundColor Cyan
    $out = & $py (Join-Path $here $script) 2>&1 | Out-String
    Write-Host $out.Trim()
    $ok = $true
    foreach ($m in $mustContain) { if ($out -notmatch [regex]::Escape($m)) { $ok = $false } }
    if ($ok) { Write-Host ("  PASS: " + $label) -ForegroundColor Green }
    else { Write-Host ("  FAIL: expected to find " + ($mustContain -join ', ')) -ForegroundColor Red }
    Write-Host ""
    return $ok
}

$results = @()
$results += Check 'exact conditional estimate' 'tools\exact_ci.py'      @('MH OR = 2.60', '0.224', '0.60 - 10.25')
$results += Check 'leave-one-out across nine acylations' 'tools\leave_one_out.py' @('1.97 - 65.12', 'OR=2.60')
$results += Check 'power across effect sizes' 'tools\power_scale.py'   @('power at OR 5.19 = 0.49', 'power at OR 10.25 = 0.80')

if ($results -contains $false) {
    Write-Host 'One or more checks failed: the archive does not reproduce the manuscript.' -ForegroundColor Red
    exit 1
}
Write-Host 'All three checks pass: this archive reproduces the reported numbers.' -ForegroundColor Green
