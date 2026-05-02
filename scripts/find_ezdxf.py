# -*- coding: utf-8 -*-
import site
import subprocess

# Find ezdxf
try:
    import ezdxf
    print(f"ezdxf version: {ezdxf.__version__}")
except ImportError:
    print("ezdxf not found via import")

# Get site packages
print("Site packages:", site.getsitepackages())

# Check which python
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Try to find ezdxf location
import pkgutil
for importer in pkgutil.iter_modules():
    if 'ezdxf' in str(importer):
        print(f"Found: {importer}")
