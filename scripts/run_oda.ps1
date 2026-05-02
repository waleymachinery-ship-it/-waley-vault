$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$sourceFolder = "C:\Users\pc\Desktop\伟力机械知识库\2026\图纸"
$outputFolder = "C:\Users\pc\Desktop\converted"

Write-Host "=== ODA File Converter Test ==="
Write-Host "Source: $sourceFolder"
Write-Host "Output: $outputFolder"

# Verify source exists
if (!(Test-Path $sourceFolder)) {
    Write-Error "Source folder not found: $sourceFolder"
    exit 1
}

# Create output folder
if (!(Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
    Write-Host "Created output folder"
}

# Run conversion
# Syntax: ODAFileConverter.exe <source> <output> <source_format> <output_format> [subfolder_flag]
$odaExe = "C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"
$arg1 = $sourceFolder
$arg2 = $outputFolder
$arg3 = "DWG"
$arg4 = "DXF"
$arg5 = "1"  # 1 = include subfolders

Write-Host "Running: $odaExe $arg1 $arg2 $arg3 $arg4 $arg5"
& $odaExe $arg1 $arg2 $arg3 $arg4 $arg5

Write-Host "=== Done ==="
