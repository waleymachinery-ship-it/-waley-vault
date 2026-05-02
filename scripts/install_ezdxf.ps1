# Install ezdxf into hermes-agent venv
$venvPython = "C:\Users\pc\.hermes\hermes-agent\.venv\Scripts\python.exe"

Write-Output "Python venv: $venvPython"
Write-Output "Checking venv contents..."
Get-ChildItem "C:\Users\pc\.hermes\hermes-agent\.venv\Scripts" | Select-Object Name

Write-Output "---"
Write-Output "Installing ezdxf via python -m pip..."
& $venvPython -m pip install ezdxf 2>&1

Write-Output "---"
Write-Output "Verifying..."
& $venvPython -c "import ezdxf; print('ezdxf version:', ezdxf.__version__)"
