$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$owner = Join-Path $root "adapters\claude\session_start_hook.ps1"
& $owner @args
exit $LASTEXITCODE
