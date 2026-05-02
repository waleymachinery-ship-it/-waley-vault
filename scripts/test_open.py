# Test FreeCAD opening SLDPRT
import FreeCAD
import Part
import os

input_file = os.path.expanduser("~/sldprt_test.SLDPRT")
print(f"Testing FreeCAD with: {input_file}")
print(f"File exists: {os.path.exists(input_file)}")

try:
    doc = FreeCAD.open(input_file)
    print(f"Success! Opened: {doc.Name}")
    print(f"Objects: {len(doc.Objects)}")
    for obj in doc.Objects[:5]:
        print(f"  - {obj.Name} ({obj.TypeId})")
    FreeCAD.closeDocument(doc.Name)
except Exception as e:
    print(f"Error: {e}")
