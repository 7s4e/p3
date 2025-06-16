# --- CONFIGURATION ---
$arch     = "amd64"  # or x86, arm64
$workDir  = "C:\WinPE_$arch"
$usbDrive = "E:"     # Change to USB drive letter (e.g., D:, E:)

# --- PATH TO ADK TOOLS ---
$adkPath   = "C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit"
$copype    = "$adkPath\Deployment Tools\$arch\copype.cmd"
$makeMedia = "$adkPath\Deployment Tools\MakeWinPEMedia.cmd"

# --- VALIDATION ---
if (-not (Test-Path $copype)) {
    Write-Error "copype.cmd not found at expected path: $copype"
    exit 1
}

if (-not (Test-Path $makeMedia)) {
    Write-Error "MakeWinPEMedia.cmd not found at expected path: $makeMedia"
    exit 1
}

if (-not (Test-Path $usbDrive)) {
    Write-Error "USB drive $usbDrive not found. Insert USB or update variable."
    exit 1
}

# --- CREATE WINPE WORKING FOLDER ---
if (Test-Path $workDir) {
    Write-Host "Removing existing work directory: $workDir"
    Remove-Item -Recurse -Force $workDir
}

Write-Host "Creating WinPE working directory..."
& $copype $arch $workDir

# --- CREATE BOOTABLE USB ---
Write-Host "Creating bootable WinPE USB on $usbDrive..."
& $makeMedia /UFD $workDir $usbDrive

Write-Host "`n✅ Windows PE bootable USB created successfully."

# ######################
# # --- ADD DISKPART SCRIPT TO MEDIA ---
# $toolsDir = Join-Path $workDir "media\Tools"
# New-Item -Path $toolsDir -ItemType Directory -Force | Out-Null

# $diskpartScript = @"
# select disk 0
# clean
# convert gpt
# create partition efi size=100
# format quick fs=fat32 label=System
# assign letter=S
# create partition primary
# format quick fs=ntfs label=Windows
# assign letter=W
# exit
# "@
# $diskpartPath = Join-Path $toolsDir "diskpart.txt"
# $diskpartScript | Set-Content -Path $diskpartPath -Encoding ASCII
# Write-Host "Added disk partitioning script to $diskpartPath"

# # --- CREATE BOOTABLE USB ---
# Write-Host "Creating bootable WinPE USB on $usbDrive..."
# & $makeMedia /UFD $workDir $usbDrive

# Write-Host "`n✅ Windows PE bootable USB created successfully."
# Write-Host "📄 To partition a disk in WinPE, run:"
# Write-Host "    diskpart /s X:\Tools\diskpart.txt"
# Write-Host "    (Replace X: with your WinPE drive letter, usually X:)"

