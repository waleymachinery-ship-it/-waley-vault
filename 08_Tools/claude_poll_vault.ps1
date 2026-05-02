param()
$ErrorActionPreference = "SilentlyContinue"
$VP = [Environment]::GetFolderPath("Desktop") + "\伟力机械知识库"
$TP = Join-Path $VP "00_Workflow\memory\task_queue.json"
$ZP = Join-Path $VP "00_Workflow\memory\Z_Memory_Sync.json"
$MP = Join-Path $VP ("memory\" + (Get-Date -Format "yyyy-MM-dd") + ".md")
$LP = "D:\weili_claude_poll.log"
$FT = "oc_2a35b9e85451a57f9c64f93f15912176"
$CL = Join-Path $VP "Claude\claude.cmd"
$STATE = "D:\weili_poll_state.txt"

function GTQ { $c = Get-Content $TP -Raw -Encoding UTF8; if ($c.StartsWith([char]0xFEFF)) { $c = $c.Substring(1) }; ConvertFrom-Json $c }
function STQ { param($d) $d | ConvertTo-Json -Depth 10 | Set-Content $TP -Encoding UTF8 }
function GZM { $c = Get-Content $ZP -Raw -Encoding UTF8; if ($c.StartsWith([char]0xFEFF)) { $c = $c.Substring(1) }; ConvertFrom-Json $c }
function SZM { param($d) $d | ConvertTo-Json -Depth 10 | Set-Content $ZP -Encoding UTF8 }
function WL { param($m) "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $m" | Add-Content $LP -Encoding UTF8 }
function SF { param($m) Start-Process powershell.exe -ArgumentList "-NoProfile", "-Command", "openclaw message send --channel feishu --target '$FT' --message `"$m`"" -WindowStyle Hidden }
function SZM2 { param($e) $z = GZM; $z.version = $z.version + 1; $z.last_modified = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+08:00"); $z.last_writer = "claude"; $z.entries += $e; SZM $z; return $z.version }
function WM { param($c) Add-Content $MP -Value ("`n`n## Poll (" + (Get-Date -Format "HH:mm") + ")`n`n" + $c + "`n") -Encoding UTF8 }
function LD { if (Test-Path $STATE) { Get-Content $STATE -Raw } else { "" } }
function SV { param($s) $s | Set-Content $STATE -Encoding UTF8 }

# Spawn Claude CLI to execute task
function Spawn-Claude {
    param($taskId, $taskContent, $priority)
    
    $prompt = "Please execute the following task: $taskContent`n`nTask ID: $taskId`nAfter completion, update task_queue.json (status=done, result=execution result) and sync to Z_Memory_Sync.json."
    
    $claudeArgs = "--print", "--dangerously-spawn-permission-bypass", "--no-input", $prompt
    
    WL "Spawning Claude CLI for task: $taskId"
    WL "Command: claude.cmd $($claudeArgs -join ' ')"
    
    $logFile = "D:\weili_claude_task_$($taskId -replace '-','_').log"
    
    try {
        $proc = Start-Process -FilePath $CL -ArgumentList $claudeArgs -WindowStyle Hidden -PassThru -RedirectStandardOutput $logFile -ErrorAction Stop
        WL "Claude CLI spawned with PID: $($proc.Id)"
        return $proc
    } catch {
        WL "ERROR spawning Claude CLI: $_"
        return $null
    }
}

$prevInProgress = @{}
$prevStr = LD
if ($prevStr) {
    $prevStr -split "," | ForEach-Object { if ($_) { $prevInProgress[$_] = $true } }
}

$q = GTQ
$pen = $q.tasks | Where-Object { $_.to -eq "claude" -and $_.status -eq "pending" }
$curInProgress = @{}

if (-not $pen) {
    foreach ($t in $q.tasks) {
        if ($t.status -eq "done" -and $prevInProgress.ContainsKey($t.id)) {
            $msg = "[Claude] ID:" + $t.id + " done"
            SF $msg
            WL ("Sent completion for:" + $t.id)
        }
    }
    WL "No pending"
    SV ""
    exit 0
}

WL ("Found " + $pen.Count + " pending")
foreach ($t in $pen) {
    WL ("Processing:" + $t.id)
    $t.status = "in_progress"
    $t.updated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
    STQ $q
    
    $ze = @{ 
        id = ("ct-" + $t.id + "-" + (Get-Date -Format "yyyyMMdd-HHmm")); 
        agent = "claude"; 
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+08:00"); 
        content = ("Task:" + $t.id + " P:" + $t.priority + " running"); 
        tags = @("task","claude"); 
        confidence = 1.0 
    }
    $v = SZM2 $ze
    
    $msg1 = "[Claude Task] ID:" + $t.id + " P:" + $t.priority + " running. Z_Memory v" + $v
    SF $msg1
    WM ("Task:" + $t.id + " Z_Memory:v" + $v)
    
    # Spawn Claude CLI to execute task
    $proc = Spawn-Claude -taskId $t.id -taskContent $t.content -priority $t.priority
    
    $curInProgress[$t.id] = $true
    WL ("Triggered:" + $t.id + (if ($proc) { " PID:$($proc.Id)" } else { " FAILED" }))
}
$keys = ($curInProgress.Keys -join ",")
SV $keys
WL "Poll complete"