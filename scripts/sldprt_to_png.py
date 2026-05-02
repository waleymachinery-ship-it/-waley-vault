# FreeCAD Python script: SLDPRT to PNG
import sys
import os

# Get arguments
if len(sys.argv) < 3:
    print("Usage: freecadcmd sldprt_to_png.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[2]
output_file = sys.argv[3]

print(f"Input: {input_file}")
print(f"Output: {output_file}")

# Import FreeCAD
import FreeCAD
import Part
import Import
import Mesh

# Open the file
doc = FreeCAD.open(input_file)
print(f"Opened document: {doc.Name}")

# Get the first shape/part
shapes = []
for obj in doc.Objects:
    if hasattr(obj, 'Shape') and obj.Shape.Solids:
        shapes.append(obj)
        print(f"Found shape: {obj.Name}")

if not shapes:
    print("No shapes found!")
    sys.exit(1)

# Create a new view
from FreeCAD import Base
import Render

# Use the first shape
obj = shapes[0]
print(f"Rendering: {obj.Name}")

# Export to PNG using render
# FreeCAD doesn't have direct PNG export from view, so we use Mesh module
mesh = Mesh.Mesh()
mesh.addMeshFromShape(obj.Shape)

# Save mesh as PNG isn't direct either - let's try a different approach
# Actually FreeCAD can export to STEP/IGES then use other tools

print("FreeCAD direct PNG export not straightforward. Consider:")
print("1. Export to STEP, then use Blender")
print("2. Use FreeCAD's TechDraw module for 2D export")
print("3. Take screenshot manually")

# For now, export to STEP as intermediate format
step_file = output_file.replace('.png', '.step')
Part.export([obj], step_file)
print(f"Exported to STEP: {step_file}")

FreeCAD.closeDocument(doc.Name)
print("Done!")
