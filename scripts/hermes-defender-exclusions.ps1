# hermes-agent Windows Defender 排除配置
# 用途：为 hermes 安装目录添加 Windows Defender 排除项，避免实时扫描导致安装被 kill
# 运行方式：以管理员身份运行 PowerShell

param(
    [switch]$Remove  # 添加 -Remove 参数可删除排除项
)

$ExclusionPaths = @(
    "C:\hermes-venv",
    "C:\hermes-agent",
    "C:\Users\pc\hermes-agent",
    "C:\Users\pc\hermes-venv",
    "C:\Users\pc\.local\bin"
)

$ExclusionProcesses = @(
    "C:\hermes-venv\Scripts\python.exe",
    "C:\hermes-venv\Scripts\python3.exe",
    "C:\Users\pc\hermes-venv\Scripts\python.exe",
    "C:\Users\pc\.local\bin\uv.exe"
)

function Get-CurrentUser {
    $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
}

Write-Host "===== hermes-agent Windows Defender 排除配置 =====" -ForegroundColor Cyan
Write-Host ""

if (-not (Get-CurrentUser)) {
    Write-Host "[错误] 请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键 -> 以管理员身份运行 PowerShell" -ForegroundColor Yellow
    exit 1
}

if ($Remove) {
    Write-Host "[移除模式] 删除 Windows Defender 排除项..." -ForegroundColor Yellow
    foreach ($path in $ExclusionPaths) {
        if (Test-Path $path) {
            try {
                Remove-MpPreference -ExclusionPath $path -ErrorAction SilentlyContinue
                Write-Host "  [移除] 路径: $path" -ForegroundColor Gray
            } catch {}
        }
    }
    foreach ($proc in $ExclusionProcesses) {
        try {
            Remove-MpPreference -ExclusionProcess $proc -ErrorAction SilentlyContinue
            Write-Host "  [移除] 进程: $proc" -ForegroundColor Gray
        } catch {}
    }
    Write-Host "[完成] 排除项已移除" -ForegroundColor Green
    exit 0
}

Write-Host "[添加模式] 添加 Windows Defender 排除项..." -ForegroundColor Cyan
Write-Host ""

$AddedPaths = 0
$AddedProcs = 0

foreach ($path in $ExclusionPaths) {
    if (-not (Test-Path $path)) {
        Write-Host "  [警告] 路径不存在（将跳过）: $path" -ForegroundColor Yellow
        continue
    }

    try {
        # 检查是否已有排除
        $existing = Get-MpPreference | Select-Object -ExpandProperty ExclusionPath -ErrorAction SilentlyContinue
        if ($existing -contains $path) {
            Write-Host "  [跳过] 已有排除: $path" -ForegroundColor Gray
            continue
        }

        Add-MpPreference -ExclusionPath $path
        Write-Host "  [添加] 路径: $path" -ForegroundColor Green
        $AddedPaths++
    } catch {
        Write-Host "  [错误] 添加路径失败: $path" -ForegroundColor Red
        Write-Host "         $($_.Exception.Message)" -ForegroundColor Red
    }
}

foreach ($proc in $ExclusionProcesses) {
    if (-not (Test-Path $proc)) {
        Write-Host "  [警告] 进程不存在（将跳过）: $proc" -ForegroundColor Yellow
        continue
    }

    try {
        $existing = Get-MpPreference | Select-Object -ExpandProperty ExclusionProcess -ErrorAction SilentlyContinue
        if ($existing -contains $proc) {
            Write-Host "  [跳过] 已有排除: $proc" -ForegroundColor Gray
            continue
        }

        Add-MpPreference -ExclusionProcess $proc
        Write-Host "  [添加] 进程: $proc" -ForegroundColor Green
        $AddedProcs++
    } catch {
        Write-Host "  [错误] 添加进程失败: $proc" -ForegroundColor Red
        Write-Host "         $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===== 配置完成 =====" -ForegroundColor Cyan
Write-Host "添加了 $AddedPaths 个路径排除" -ForegroundColor $(if ($AddedPaths -gt 0) { "Green" } else { "Gray" })
Write-Host "添加了 $AddedProcs 个进程排除" -ForegroundColor $(if ($AddedProcs -gt 0) { "Green" } else { "Gray" })
Write-Host ""
Write-Host "当前排除路径列表：" -ForegroundColor White
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }

Write-Host ""
Write-Host "提示：如果之前安装被 kill，重新运行安装脚本：" -ForegroundColor Cyan
Write-Host "  C:\Users\pc\hermes-venv\Scripts\pip install openai..." -ForegroundColor White
Write-Host ""
Write-Host "或者直接运行分批安装脚本：" -ForegroundColor Cyan
Write-Host "  D:\桌面文件\伟力机械知识库\scripts\hermes-install-windows.cmd" -ForegroundColor White
