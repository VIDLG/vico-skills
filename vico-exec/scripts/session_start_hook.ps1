$planRoot = Join-Path (Get-Location) ".vico\plans\active"
if (Test-Path -LiteralPath $planRoot) {
    $plans = Get-ChildItem -LiteralPath $planRoot -File -Filter *.md | Select-Object -ExpandProperty Name
    if ($plans.Count -gt 0) {
        $list = ($plans | ForEach-Object { "- $_" }) -join "`n"
        Write-Output "Vico execute: active plans detected.`n$list`nAnchor execution on the active plan and keep going until complete or a real blocker is reached."
        exit 0
    }
}

Write-Output "Vico execute: no active .vico plan detected."
exit 0
