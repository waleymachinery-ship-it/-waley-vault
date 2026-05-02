$file = "D:\桌面文件\伟力机械知识库\2026\图纸\PEII-III120-00 双层带线三模头 - 新设计dxf.dwg"
$bytes = [System.IO.File]::ReadAllBytes($file)
$header = ($bytes[0..15] | ForEach-Object { '{0:X2}' -f $_ }) -join ' '
Write-Output "Header bytes: $header"
Write-Output "File size: $($bytes.Length) bytes"
