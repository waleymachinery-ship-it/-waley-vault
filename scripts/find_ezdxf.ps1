# Find ezdxf location
$result = pip show ezdxf 2>&1
Write-Output $result

# Also check which python/pip
Write-Output "---"
$pythonPath = where.exe python 2>$null
$pipPath = where.exe pip 2>$null
Write-Output "Python: $pythonPath"
Write-Output "Pip: $pipPath"

# Try to find site-packages
$pythonCmd = "import site; print(site.getsitepackages())"
python -c $pythonCmd 2>&1
