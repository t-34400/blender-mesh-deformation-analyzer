import bpy
from ..properties import Strain_Panel_Properties
from ..operators import Strain_Calculator


class Strain_Panel(bpy.types.Panel):
    bl_idname = "STRAINADDON_PT_strain_panel"
    bl_label = "Strain Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Strain Analysis'


    def draw(self, context):
        layout = self.layout
        props = context.scene.strain_panel_properties

        row = layout.row()
        row.label(text="Original mesh")

        self.obj_list = [(obj.name, obj.name, "") for obj in bpy.context.scene.objects if obj.type == 'MESH']
        layout.prop(props, Strain_Panel_Properties.mesh_list_prop_tag, text="")

        row = layout.row()
        row.label(text="Frame")
        row.prop(props, Strain_Panel_Properties.original_frame_prop_tag, text="")

        layout.separator()
        
        layout.label(text="Target mesh")
        layout.prop(props, "target_mesh_list_prop", text="")
        
        layout.label(text="Target frames")
        row = layout.row()
        row.label(text="Start")
        row.prop(props, Strain_Panel_Properties.target_start_frame_prop_tag, text="")
        row.label(text="End")
        row.prop(props, Strain_Panel_Properties.target_end_frame_prop_tag, text="")

        layout.separator()
        layout.operator(Strain_Calculator.bl_idname, text="Calculate strain")

