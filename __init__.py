bl_info = {
    "name": "Mesh Strain Analysis",
    "description": "Calculate strain of mesh based on its original shape",
    "author": "t-34400",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Strain Analysis",
    "category": "Mesh"
}


modules = (
    '.panels.strain_panel',
    '.operators.strain_operators',
    '.properties.strain_panel_properties'
)


if "bpy" in locals():
    import importlib
    for module_name in modules:
        module = importlib.import_module(module_name, package=__name__)
        importlib.reload(module)
    print('reload classes')


import bpy
from .panels import Strain_Panel
from .operators import Stain_Calculator
from .properties import Strain_Panel_Properties


properties = (
    Strain_Panel_Properties,
)

classes = (
    Strain_Panel,
    Stain_Calculator,
)


def register():
    for props in properties:
        bpy.utils.register_class(props)
        bpy.types.Scene.strain_panel_properties = bpy.props.PointerProperty(type=props)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for props in properties:
        del bpy.types.Scene.strain_panel_properties
        bpy.utils.unregister_class(props)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()