# Blender-Mesh-Strain-Analyzer Addon
This addon calculates mesh strains based on the original and deformed mesh shapes and sets vertex colors accordingly. The strain information can be used for various purposes, such as identifying areas where deformation occurs too much or creating procedural textures based on mesh shapes.

## Usage
1. Save the project directory as a ZIP.
2. Click <code>Edit</code> > <code>Preference</code> on the Blender menu bar. Select the <code>Add-ons</code> tab in the window, press the <code>install</code> button, and open the ZIP without unzipping it.
3. Click the checkbox to activate the addon.
4. If the menu bar is not displayed in the 3D viewport, hover the mouse over the 3D viewport and press the <code>N</code> key.
5. Select <code>Strain analysis</code> tab to open the <code>Strain Panel</code>.
6. In the <code>Original mesh</code> pull-down menu, specify the mesh objects and frames that have the shape of the original mesh.
7. Specify the target mesh and frame for which the strain is to be calculated.
8. Press the <code>Calculate strain</code> button to run the calculation.

## Demo
TODO:

## Note
- The strain calculation may take some time for large meshes.
- The strain calculation is based on the assumption that the original and deformed meshes have the same topology.

## Additional Information
### How it Works
- The addon calculates strains of mesh by comparing the original mesh with the deformed mesh on a per-vertex basis. For each vertex, the addon calculates the weighted average of max principal strains of the meshes around a vertex. 
- The vertex color is then set based on the magnitude of this strain. The vertex color is green when there is no distortion, turn progressively red as it increases beyond zero, and turn progressively blue as it decreases below zero.
