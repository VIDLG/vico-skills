$planRoot = Join-Path (Get-Location) ".wilco\plans\active"
if (-not (Test-Path -LiteralPath $planRoot)) {
    exit 0
}

$plans = Get-ChildItem -LiteralPath $planRoot -File -Filter *.md
if ($plans.Count -eq 0) {
    exit 0
}

$content = ($plans | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw }) -join "`n"

if ($content -match "Status:\s*`?in_progress`?") {
    $mentionsBlocker = $content -match "blocker"
    $mentionsNextStep = $content -match "Next Step"
    if (-not $mentionsBlocker -and -not $mentionsNextStep) {
        Write-Output "Wilco execute: active in-progress plan still exists. Stop only if you have completed the current slice, identified a real blocker, or clearly stated the next recommended step."
        exit 2
    }
}

exit 0
