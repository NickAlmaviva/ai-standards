<#
.SYNOPSIS
  Disattiva ai-standards per Kilo Code (Windows): rimuove le variabili
  d'ambiente utente e la config generata. Il clone in ~\.ai-standards resta.
#>
[Environment]::SetEnvironmentVariable("KILO_CONFIG", $null, "User")
[Environment]::SetEnvironmentVariable("KILO_CONFIG_DIR", $null, "User")
$GenDir = Join-Path $HOME ".config\ai-standards"
if (Test-Path $GenDir) { Remove-Item -Recurse -Force $GenDir }
Write-Host "[ai-standards] Disattivato. Chiudi completamente VS Code e riaprilo." -ForegroundColor Cyan
Write-Host "[ai-standards] Per riattivare rilancia install.ps1." -ForegroundColor Cyan
