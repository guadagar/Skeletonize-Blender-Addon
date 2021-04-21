# Skeletonize-Blender-Addon
This repository contains the files needed to install the skeletonize Blender addon used in this [publication](https://www.biorxiv.org/content/10.1101/2021.03.15.435547v2). It provides an interface in Blender 
to the [Triangulated Surface Mesh Skeletonization](https://doc.cgal.org/latest/Surface_mesh_skeletonization/index.html) from the [Cgal library](https://www.cgal.org/).
It adds the ability to skeletonize a triangulated mesh in Blender. For cigar-shaped objects (as the outer membrane of mitochondria analyzed in this [publication](https://www.biorxiv.org/content/10.1101/2021.03.15.435547v2)),
the length and the average radius of the mesh can be also computed.

## Installation

This addon has been tested in Blender 2.79 and the skeletonize executable was compiled in a MacOS Catalina version 10.15.3. If you are using a different operating system, you will need to compile a new executable, with the sources from [Triangulated Surface Mesh Skeletonization](https://doc.cgal.org/latest/Surface_mesh_skeletonization/index.html) and remplace the skeletonize excecutable in the `bin` folder. 

First, install the [OFF export/import addon](https://github.com/alextsui05/blender-off-addon) for Blender 2.79. Then, download or clone this repository. 

    git clone https://github.com/guadagar/Skeletonize-Blender-Addon.git skeletonize_addon
    cd skeletonize_addon
    
 Create a link to your skeletonize blender addon directory. In a terminal window type:
 
    ln -s . skeletonize_addon

In a terminal window type:

    make install




