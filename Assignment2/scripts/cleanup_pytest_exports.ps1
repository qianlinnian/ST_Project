$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$exportsDir = Join-Path $projectRoot "exports"

if (-not (Test-Path -LiteralPath $exportsDir)) {
    Write-Host "Exports directory not found: $exportsDir"
    exit 0
}

$targets = Get-ChildItem -LiteralPath $exportsDir -File -Filter "pytest_*"

if (-not $targets) {
    Write-Host "No pytest_* export files found in $exportsDir"
    exit 0
}

$deleted = 0
$failed = @()

foreach ($file in $targets) {
    try {
        if ($file.IsReadOnly) {
            $file.IsReadOnly = $false
        }

        [System.IO.File]::SetAttributes($file.FullName, [System.IO.FileAttributes]::Normal)
        Remove-Item -LiteralPath $file.FullName -Force
        Write-Host "Deleted $($file.Name)"
        $deleted++
    }
    catch {
        $failed += [PSCustomObject]@{
            Name = $file.Name
            Error = $_.Exception.Message
        }
    }
}

Write-Host ""
Write-Host "Deleted files: $deleted"

if ($failed.Count -gt 0) {
    Write-Host "Failed files:"
    $failed | Format-Table -AutoSize
    exit 1
}

Write-Host "Cleanup completed."
