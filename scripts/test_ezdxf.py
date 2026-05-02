# -*- coding: utf-8 -*-
import ezdxf
import sys

# Test reading the DXF file with ezdxf
dxf_file = r"D:\桌面文件\伟力机械知识库\2026\图纸\PSFNpro140-050-SSSD3AF-Z22_55_110_145_B5_M8.dxf"

try:
    print(f"Testing ezdxf on: {dxf_file}")
    doc = ezdxf.readfile(dxf_file)
    print(f"DXF version: {doc.dxfversion}")
    print(f"Entities count: {len(list(doc.modelspace()))}")
    
    # Get some entity info
    msp = doc.modelspace()
    entities = list(msp)[:5]
    for i, ent in enumerate(entities):
        print(f"  Entity {i}: {ent.dxftype()} - {ent}")
    
    print("\nezdxf works correctly on DXF files!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
