bl_info = {
    "name": "Neuropil tools: skeletonize",
    "author":"Guadalupe C. Garcia, Tom Bartol",
    "version": (1, 1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > Skeletonization",
    "category": "Mesh Analysis",
    "tracker_url": "https://github.com/mcellteam/neuropil_tools/skeletonization_tool",
}

import bpy
import random
import os

if "skel_panel" not in locals():
    print("Importing skeletonize Addon")
    from . import skel_panel
else:
    print("Reloading skeletonize Addon")
    import imp
    imp.reload(skel_panel)

def register():
    # register all of the components of the Addon
    bpy.utils.register_module(__name__)
    bpy.types.Object.my_obj_props = bpy.props.PointerProperty(type=skel_panel.MyObjectProperties)
    print("Add skeletonize Addon registered")

def unregister():
    bpy.utils.register_module(__name__)
    print("Add skeletonize Addon unregistered")

if __name__ == "__main__":
    register()
