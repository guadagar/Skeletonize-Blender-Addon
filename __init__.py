
"""
Copyright (C) 2020-2021 by
The Salk Institute for Biological Studies
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

bl_info = {
    "name": "Neuropil tools: skeletonize",
    "author":"Guadalupe C. Garcia, Tom Bartol",
    "version": (1, 1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > Skeletonization",
    "category": "Mesh Analysis",
    "tracker_url": "https://github.com/mcellteam/neuropil_tools/skeletonize_addon"
    ,
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
