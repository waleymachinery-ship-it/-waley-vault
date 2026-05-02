# -*- coding: utf-8 -*-
import ezdxf
import os

dxf_file = r'D:\桌面文件\伟力机械知识库\2026\图纸\PSFNpro140-050-SSSD3AF-Z22_55_110_145_B5_M8.dxf'

print(f"Testing ezdxf on DXF file...")
print(f"File exists: {os.path.exists(dxf_file)}")
print(f"File size: {os.path.getsize(dxf_file)} bytes")

try:
    doc = ezdxf.readfile(dxf_file)
    print(f"DXF version: {doc.dxfversion}")
    msp = doc.modelspace()
    entities = list(msp)
    print(f"Entities count: {len(entities)}")
    print("First 5 entities:")
    for ent in entities[:5]:
        print(f"  - {ent.dxftype()}")
    print("\nSUCCESS: ezdxf can read DXF files!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
