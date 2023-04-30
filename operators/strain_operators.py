import bpy

class Stain_Calculator(bpy.types.Operator):
    bl_idname = "wm.strain_calculator"
    bl_label = "Strain calculator"
    
    def execute(self, context):
        print("Button clicked!")
        return {'FINISHED'}