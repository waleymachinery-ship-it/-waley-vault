# Use the Python that HAS ezdxf installed
$pythonExe = "C:\Users\pc\AppData\Local\Programs\Python\Python313\python.exe"
$pipExe = "C:\Users\pc\AppData\Local\Programs\Python\Python313\Scripts\pip.exe"

Write-Output "Python: $pythonExe"
Write-Output "Verifying ezdxf..."
& $pythonExe -c "import ezdxf; print('ezdxf version:', ezdxf.__version__)"

Write-Output "---"
Write-Output "Testing DXF file read..."
$testScript = @"
import ezdxf
dxf_file = r'D:\桌面文件\伟力机械知识库\2026\图纸\PSFNpro140-050-SSSD3AF-Z22_55_110_145_B5_M8.dxf'
try:
    doc = ezdxf.readfile(dxf_file)
    print(f'DXF version: {doc.dxfversion}')
    msp = doc.modelspace()
    entities = list(msp)
    print(f'Entities count: {len(entities)}')
    print('First 3 entities:')
    for ent in entities[:3]:
        print(f'  - {ent.dxftype()}: {ent}')
    print('SUCCESS: ezdxf can read DXF files!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"@

& $pythonExe -c $testScript 2>&1
