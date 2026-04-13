$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$owner = Join-Path $root "adapters\claude\stop_hook.ps1"
& $owner @args
exit $LASTEXITCODE
