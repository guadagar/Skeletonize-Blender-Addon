# Skeletonize-Blender-Addon
This repository contains the files needed to install the skeletonize Blender addon used in this [publication](https://www.biorxiv.org/content/10.1101/2021.03.15.435547v2). It provides an interface in Blender 
to the [Triangulated Surface Mesh Skeletonization](https://doc.cgal.org/latest/Surface_mesh_skeletonization/index.html) from the [CGAL library](https://www.cgal.org/).
It adds the ability to skeletonize a triangulated mesh in Blender. For cigar-shaped objects (as the outer membrane of mitochondria analyzed in this [publication](https://www.biorxiv.org/content/10.1101/2021.03.15.435547v2)),
the length and the average radius of the mesh can be also computed.

## Installation

This addon has been tested in Blender 2.79 and the skeletonize executable was compiled in a MacOS Catalina version 10.15.3. If you are using a different operating system, you will need to compile a new executable, with the sources from [Triangulated Surface Mesh Skeletonization](https://doc.cgal.org/latest/Surface_mesh_skeletonization/index.html) and remplace the skeletonize excecutable in the `bin` folder. 

First, install the [OFF export/import addon](https://github.com/alextsui05/blender-off-addon) for Blender 2.79. Then, download or clone this repository. 

    git clone https://github.com/guadagar/Skeletonize-Blender-Addon.git skeletonize_addon
    cd skeletonize_addon
    
After, type in a terminal window:
 
    make

and finally type in a terminal:

    make install
    
The addon has been installed, and it is available in the `Mesh Analysis` category section. Go to `File` -> `User Preferences` -> `Mesh Analysis`.

Select the object you want to skeletonize, and then hit `skeletonize`. With the object selected you can further compute the length and/or calculate the average radius.     




