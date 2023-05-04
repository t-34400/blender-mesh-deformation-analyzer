import bpy
from mathutils import Vector

from typing import List, Tuple
import colorsys

from ..utils import get_strains_of_mesh


class Strain_Calculator(bpy.types.Operator):
    bl_idname = "wm.strain_calculator"
    bl_label = "Strain calculator"

    layer_name = "strain_addon_color_layer"

    
    def execute(self, context):
        props = context.scene.strain_panel_properties

        target_mesh = props.target_mesh_list_prop
        start_frame = props.target_start_frame_prop
        end_frame = props.target_end_frame_prop

        current_frame = context.scene.frame_current
        wm = context.window_manager
        wm.progress_begin(start_frame, end_frame + 1)

        bpy.ops.ptcache.bake_all()
        # get the evaluated dependency graph for the target frame
        depsgraph = context.evaluated_depsgraph_get()

        context.scene.frame_set(props.original_frame_prop)
        original_vertices = Strain_Calculator.get_vertices(context, depsgraph, props.mesh_list_prop)
        faces = Strain_Calculator.get_faces(context, props.mesh_list_prop)
        original_vertex_count = len(original_vertices)

        for frame_index in range(start_frame, end_frame):

            wm.progress_update(frame_index)
            context.scene.frame_set(frame_index)

            target_vertices = Strain_Calculator.get_vertices(context, depsgraph, target_mesh)
            target_vertex_count = len(target_vertices.count)
            if target_vertex_count < original_vertex_count
                self.report({'ERROR'}, f'The target object at frame {frame_index} has fewer vertices than the original')
                return {'CANCELLED'}

            strains = get_strains_of_mesh(original_vertices, target_vertices, faces)
            vertex_colors = [Strain_Calculator.get_color(strain) for strain in strains]
            
            Strain_Calculator.set_vertex_colors(context, target_mesh, vertex_colors, Strain_Calculator.layer_name, frame_index)
        
        context.scene.frame_set(current_frame)
        wm.progress_end()
        self.report({'INFO'}, 'Calculation completed successfully.')
        return {'FINISHED'}


    @classmethod
    def get_vertices(cls, context, depsgraph, obj_name: str) -> List[Vector]:
        obj = bpy.data.objects[obj_name]
        eval_obj = obj.evaluated_get(depsgraph)
    
        return [vert.co.copy() for vert in eval_obj.data.vertices]


    @classmethod
    def get_faces(cls, context, mesh_name: str) -> List[List[int]]:
        mesh = bpy.data.meshes[mesh_name]
        return [face.vertices for face in mesh.polygons]


    @classmethod
    def get_color(cls, strain):
        return colorsys.hsv_to_rgb(max(0, min(1.0, strain * 5)), 0.8, 0.5) + (1.0,)


    @classmethod
    def set_vertex_colors(cls, context, mesh_name, vertex_colors, layer_name, frame_index):
        mesh = context.scene.objects[mesh_name].data
        
        frame_layer_name = layer_name
        if frame_layer_name not in mesh.vertex_colors:
            mesh.vertex_colors.new(name=frame_layer_name)
        
        color_layer = mesh.vertex_colors[frame_layer_name]
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                vertex_index = mesh.loops[loop_index].vertex_index
                color_layer.data[loop_index].color = vertex_colors[vertex_index]
                color_layer.data[loop_index].keyframe_insert(data_path="color", frame=frame_index)