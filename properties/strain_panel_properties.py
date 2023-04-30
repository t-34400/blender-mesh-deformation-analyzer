import bpy


class Strain_Panel_Properties(bpy.types.PropertyGroup):    
    mesh_list_prop_tag = "mesh_list_prop"
    target_mesh_list_prop_tag = "target_mesh_list_prop"
    original_frame_prop_tag = "original_frame_prop"
    target_start_frame_prop_tag = "target_start_frame_prop"
    target_end_frame_prop_tag = "target_end_frame_prop"


    def get_mesh_list(self, context):
        return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'MESH']


    def update_original_frame_prop(self, context):
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        
        # To avoid infinite recursion, assign the value only when there is an update
        new_value = Strain_Panel_Properties.clamp(self.original_frame_prop, frame_start, frame_end)
        if self.original_frame_prop != new_value:
            self.original_frame_prop = new_value


    def update_target_start_frame_prop(self, context):
        frame_start = bpy.context.scene.frame_start

        new_value = Strain_Panel_Properties.clamp(self.target_start_frame_prop, frame_start, self.target_end_frame_prop)
        if self.target_start_frame_prop != new_value:
            self.target_start_frame_prop = new_value


    def update_target_end_frame_prop(self, context):
        frame_end = bpy.context.scene.frame_end

        new_value = Strain_Panel_Properties.clamp(self.target_end_frame_prop, self.target_start_frame_prop, frame_end)
        if self.target_end_frame_prop != new_value:
            self.target_end_frame_prop = new_value


    def clamp(value, min_value, max_value):
        return max(min_value, min(max_value, value))


    mesh_list_prop: bpy.props.EnumProperty(
        name=mesh_list_prop_tag,
        items=get_mesh_list,
        description="Select a mesh object from the list",
    )
    
    target_mesh_list_prop: bpy.props.EnumProperty(
        name=target_mesh_list_prop_tag,
        items=get_mesh_list,
        description="Select a target mesh object to perform strain measurements on",
    )

    original_frame_prop: bpy.props.IntProperty(
        name=original_frame_prop_tag,
        description="Enter a frame number of the mesh to be used as the basis for calculating the strain",
        default=1,
        update=update_original_frame_prop
    )

    target_start_frame_prop: bpy.props.IntProperty(
        name=target_start_frame_prop_tag,
        description="Enter a start frame number for calculating strain of the mesh",
        default=1,
        update=update_target_start_frame_prop
    )

    target_end_frame_prop: bpy.props.IntProperty(
        name=target_end_frame_prop_tag,
        description="Enter a end frame number for calculating strain of the mesh",
        default=1,
        update=update_target_end_frame_prop
    )
