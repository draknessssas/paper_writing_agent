# Native-Windows bootstrap for the manuscript writing workspace (PowerShell 5.1+).
# Use this ONLY if you run Claude Code / Codex CLI natively on Windows.
# If you use WSL, run scripts/bootstrap.sh instead.
#
# The repo stores POSIX symlinks (.claude/skills/* -> ../../skills/*). Git for Windows materializes
# them as plain text files unless core.symlinks is enabled. This script recreates the links as
# directory junctions, which need no admin rights and no Developer Mode.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1                 # repo + user scope
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Scope local
#   Environment: IEEE_MANUSCRIPT_PATH, IEEE_BIB_PATH, IEEE_VENUE (e.g. tpel), IEEE_PAPER_TYPE

param(
    [ValidateSet('user', 'local')]
    [string]$Scope = 'user'
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$Profile = Join-Path $Root 'profiles\active_profile.yml'

$Python = if ($env:IEEE_PYTHON) { $env:IEEE_PYTHON } elseif (Test-Path (Join-Path $Root '.venv\Scripts\python.exe')) { Join-Path $Root '.venv\Scripts\python.exe' } else { 'python' }
& $Python (Join-Path $Root 'scripts\profile_config.py') --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Profile configuration failed; no links changed.' }

function Remove-Existing {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -ne $item) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            if ($item.PSIsContainer) { [IO.Directory]::Delete($item.FullName) } else { [IO.File]::Delete($item.FullName) }
        }
        else {
            Move-Item -LiteralPath $Path -Destination "$Path.backup.$(Get-Date -Format yyyyMMddHHmmssfffffff)"
        }
    }
}

function Remove-StaleLink {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -ne $item) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            if ($item.PSIsContainer) { [IO.Directory]::Delete($item.FullName) } else { [IO.File]::Delete($item.FullName) }
            Write-Host "pruned stale link: $Path"
        }
    }
}

function Link-Directory {
    param([string]$Source, [string]$Dest)
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
    Remove-Existing -Path $Dest
    New-Item -ItemType Junction -Path $Dest -Target $Source | Out-Null
}

function Link-File {
    param([string]$Source, [string]$Dest)
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
    Remove-Existing -Path $Dest
    try { New-Item -ItemType SymbolicLink -Path $Dest -Target $Source -ErrorAction Stop | Out-Null }
    catch {
        try { New-Item -ItemType HardLink -Path $Dest -Target $Source -ErrorAction Stop | Out-Null }
        catch {
            Copy-Item -LiteralPath $Source -Destination $Dest -Force
            Write-Warning "Copied instead of linked: $Dest (edits will NOT sync back; enable Developer Mode for symlinks)"
        }
    }
}

$skills = @('writing-skill', 'style-profiler', 'citation-verifier', 'manuscript-reviewer')
$legacySkills = @(
    'paper-corpus-ingest', 'author-style-profiler', 'journal-style-profiler', 'topic-style-profiler',
    'domain-style-profiler', 'intro-reference-miner', 'ieee-paragraph-writer', 'ieee-reviewer',
    'ieee-style-extractor', 'ieee-claim-ledger', 'ieee-citation-verifier', 'ieee-section-planner',
    'ieee-figure-caption-writer', 'ieee-submission-auditor', 'ieee-response-writer', 'ieee-page-compressor'
)
$legacyClaudeAgents = @('ieee-writing-agent.md', 'ieee-technical-skeptic.md')
$legacyCodexAgents = @('ieee-writer', 'ieee-technical-skeptic')
$legacyOutputStyles = @('ieee-writer.md')

$dirs = @(
    '.agents\skills', '.claude\skills', '.codex\agents', '.claude\agents', '.claude\output-styles',
    'corpora\exemplars', 'corpora\my_papers', 'processed\exemplars', 'processed\my_papers', 'processed\refs',
    'profiles', 'working\briefs', 'working\drafts', 'working\ref_notes', 'refs', 'manuscript\sections',
    'templates', 'knowledge\venues'
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path (Join-Path $Root $d) | Out-Null }

foreach ($skill in $skills) {
    $src = Join-Path $Root "skills\$skill"
    if (-not (Test-Path -LiteralPath (Join-Path $src 'SKILL.md'))) { throw "Missing skills\$skill\SKILL.md" }
    Link-Directory -Source $src -Dest (Join-Path $Root ".agents\skills\$skill")
    Link-Directory -Source $src -Dest (Join-Path $Root ".claude\skills\$skill")
}
foreach ($skill in $legacySkills) {
    Remove-StaleLink (Join-Path $Root ".agents\skills\$skill")
    Remove-StaleLink (Join-Path $Root ".claude\skills\$skill")
}


if ($Scope -ne 'local') {
    $home_ = $env:USERPROFILE
    foreach ($skill in $skills) {
        Link-Directory -Source (Join-Path $Root "skills\$skill") -Dest (Join-Path $home_ ".claude\skills\$skill")
        Link-Directory -Source (Join-Path $Root "skills\$skill") -Dest (Join-Path $home_ ".codex\skills\$skill")
        Link-Directory -Source (Join-Path $Root "skills\$skill") -Dest (Join-Path $home_ ".agents\skills\$skill")
    }
    foreach ($skill in $legacySkills) {
        Remove-StaleLink (Join-Path $home_ ".claude\skills\$skill")
        Remove-StaleLink (Join-Path $home_ ".codex\skills\$skill")
        Remove-StaleLink (Join-Path $home_ ".agents\skills\$skill")
    }
    foreach ($f in Get-ChildItem (Join-Path $Root '.claude\agents') -Filter *.md) {
        Link-File -Source $f.FullName -Dest (Join-Path $home_ ".claude\agents\$($f.Name)")
    }
    foreach ($n in $legacyClaudeAgents) { Remove-StaleLink (Join-Path $home_ ".claude\agents\$n") }
    foreach ($f in Get-ChildItem (Join-Path $Root '.claude\output-styles') -Filter *.md) {
        Link-File -Source $f.FullName -Dest (Join-Path $home_ ".claude\output-styles\$($f.Name)")
    }
    foreach ($n in $legacyOutputStyles) { Remove-StaleLink (Join-Path $home_ ".claude\output-styles\$n") }
    foreach ($d in Get-ChildItem (Join-Path $Root '.codex\agents') -Directory) {
        Link-Directory -Source $d.FullName -Dest (Join-Path $home_ ".codex\agents\$($d.Name)")
    }
    foreach ($n in $legacyCodexAgents) { Remove-StaleLink (Join-Path $home_ ".codex\agents\$n") }
}

Write-Host "Writing workspace bootstrapped ($Scope scope)."
Write-Host "Active profile: profiles\active_profile.yml"
Write-Host "Parity check:   python scripts\check_parity.py"
