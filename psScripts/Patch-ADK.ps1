# Configurable: URL of the ADK patch zip file
$patchZipUrl = "https://aka.ms/WindowsADK10.1.26100.2454UpdateKB5053656.zip"

# Temp folders
$tempRoot   = Join-Path $env:TEMP "adkpatch"
$zipPath    = Join-Path $tempRoot "ADKPatch.zip"
$extractDir = Join-Path $tempRoot "extracted"
$logDir     = Join-Path $tempRoot "logs"

# Create temp dirs
$dirs = @{
    ItemType = 'Directory'
    Path     = $tempRoot, $extractDir, $logDir
    Force    = $true
}
New-Item @dirs | Out-Null

Write-Host "📥 Downloading ADK patch zip..."
Invoke-WebRequest -Uri $patchZipUrl -OutFile $zipPath

Write-Host "📦 Extracting patch files..."
Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

Write-Host "🛠️  Applying patches..."
Get-ChildItem -Path $extractDir -Filter *.msp | ForEach-Object {
    $patchFile = $_.FullName
    $logFile   = Join-Path $logDir "msiexec-$($_.Name).log"

    Write-Host "➡️  Patching $($_.Name)..."

    $msiexecArgs = @{
        FilePath     = "msiexec.exe"
        ArgumentList = @("/l*", "`"$logFile`"", "/qn", "/p", "`"$patchFile`"")
        Wait         = $true
    }

    Start-Process @msiexecArgs
}

Write-Host "`n✅ Done. Logs saved to: $logDir"
