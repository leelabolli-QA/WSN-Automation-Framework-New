<#
.SYNOPSIS
    Runs a persona's behave feature and writes reports to persona-specific paths
    so different personas no longer overwrite each other's report.

.EXAMPLE
    .\run-report.ps1 -Persona faculty
    .\run-report.ps1 -Persona student
    .\run-report.ps1 -Persona faculty -Feature .\features\faculty_all.feature -Env dev
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Persona,

    [string]$Feature,

    [string]$Env = "dev"
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$python = Join-Path $root "venv\Scripts\python.exe"

# Default feature per persona when not explicitly provided.
$defaultFeatures = @{
    "faculty" = ".\features\faculty_all.feature"
    "student" = ".\features\student.feature"
    "mentor"  = ".\features\mentor.feature"
    "rm"      = ".\features\rm_all.feature"
}

$personaKey = $Persona.ToLower()
if (-not $Feature) {
    if ($defaultFeatures.ContainsKey($personaKey)) {
        $Feature = $defaultFeatures[$personaKey]
    } else {
        throw "No default feature for persona '$Persona'. Pass one with -Feature."
    }
}

# Persona-specific output paths (kept separate so reports don't clobber).
$allureResults = "reports/allure-results/$personaKey"
$htmlReport = "reports/html-report/$personaKey-report.html"

# Ensure the HTML report directory exists (behave creates the allure dir itself).
New-Item -ItemType Directory -Force -Path (Split-Path (Join-Path $root $htmlReport)) | Out-Null

# Clear previous Allure results for this persona so stale results from an older
# run don't accumulate (the formatter appends, which otherwise double-counts
# scenarios and resurfaces already-fixed failures in the dashboard).
$allureResultsFull = Join-Path $root $allureResults
if (Test-Path $allureResultsFull) {
    Remove-Item -Path (Join-Path $allureResultsFull '*') -Recurse -Force -ErrorAction SilentlyContinue
}

$env:ENV = $Env
$env:PERSONA = $personaKey

Write-Host "Running persona '$personaKey' | feature '$Feature'" -ForegroundColor Cyan
Write-Host "  allure-results -> $allureResults" -ForegroundColor DarkCyan
Write-Host "  html report    -> $htmlReport" -ForegroundColor DarkCyan

& $python -m behave $Feature `
    -f allure_behave.formatter:AllureFormatter -o $allureResults `
    -f behave_html_formatter:HTMLFormatter -o $htmlReport `
    --no-capture

$code = $LASTEXITCODE

# Executive stakeholder dashboard (self-contained HTML).
$dashboard = "reports/html-report/$personaKey-executive-dashboard.html"
$env:PERSONA = $personaKey
& $python -m utils.executive_report $allureResults $dashboard
Write-Host "  executive dashboard -> $dashboard" -ForegroundColor DarkCyan

Write-Host "Done (persona='$personaKey', exit=$code). Report: $htmlReport" -ForegroundColor Green
exit $code
