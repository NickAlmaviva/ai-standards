<#
.SYNOPSIS
  Installa/aggiorna ai-standards per Kilo Code (Windows).
.EXAMPLE
  .\install.ps1
  .\install.ps1 -Ref v1.2.0
#>
param(
  [string]$Ref = "",
  [string]$Dir = $(if ($env:AI_STD_HOME) { $env:AI_STD_HOME } else { Join-Path $HOME ".ai-standards" }),
  [string]$Repo = $(if ($env:AI_STD_REPO_URL) { $env:AI_STD_REPO_URL } else { "https://github.com/NickAlmaviva/ai-standards.git" })
)
$ErrorActionPreference = "Stop"
function Log($m) { Write-Host "[ai-standards] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[ai-standards] $m" -ForegroundColor Yellow }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git non trovato" }

# 1. Clone o fetch
if (Test-Path (Join-Path $Dir ".git")) {
  Log "Aggiorno $Dir"
  git -C $Dir fetch --tags --prune --quiet origin
} else {
  Log "Clono $Repo in $Dir"
  git clone --quiet $Repo $Dir
}

# 2. Versione
if (-not $Ref) {
  $Ref = (git -C $Dir tag --list "v*" --sort=-v:refname | Select-Object -First 1)
  if (-not $Ref) { $Ref = "main" }
}
Log "Versione: $Ref"
git -C $Dir -c advice.detachedHead=false checkout --quiet $Ref
git -C $Dir show-ref --verify --quiet "refs/remotes/origin/$Ref"
if ($LASTEXITCODE -eq 0) { git -C $Dir merge --ff-only --quiet "origin/$Ref" }

# 3. Config generata (slash in avanti: validi in JSON e accettati da Kilo)
$AbsDir = (Resolve-Path $Dir).Path
$JsonDir = $AbsDir -replace '\\', '/'
$GenDir = Join-Path $HOME ".config\ai-standards"
$GenFile = Join-Path $GenDir "kilo.jsonc"
New-Item -ItemType Directory -Force -Path $GenDir | Out-Null
$template = Get-Content -Raw -Path (Join-Path $AbsDir "config\kilo.template.jsonc")
$template.Replace("__AI_STANDARDS_HOME__", $JsonDir) | Set-Content -Path $GenFile -Encoding UTF8
Set-Content -Path (Join-Path $GenDir "installed-ref") -Value $Ref
Log "Config generata: $GenFile"

# 4. Variabili d'ambiente utente (persistenti)
[Environment]::SetEnvironmentVariable("KILO_CONFIG", $GenFile, "User")
[Environment]::SetEnvironmentVariable("KILO_CONFIG_DIR", $AbsDir, "User")
$env:KILO_CONFIG = $GenFile
$env:KILO_CONFIG_DIR = $AbsDir
Log "KILO_CONFIG e KILO_CONFIG_DIR impostate a livello utente"

# 5. Controlli
if (-not [Environment]::GetEnvironmentVariable("AI_STD_GITLAB_TOKEN", "User")) {
  Warn "AI_STD_GITLAB_TOKEN non impostata: il server MCP GitLab non si autenticherà."
}
if ((Test-Path "$HOME\.config\kilo\kilo.jsonc") -or (Test-Path "$HOME\.config\kilo\kilo.json")) {
  Warn "Esiste una config globale personale: le chiavi in conflitto verranno sovrascritte da ai-standards."
}
Log "Fatto. Chiudi completamente VS Code (tutte le finestre) e riaprilo."
