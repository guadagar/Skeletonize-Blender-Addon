import bpy
import os, sys, tempfile
import subprocess as sp
import numpy as np


'''This file contains classes for the skeletonization tool, to generate the skeleton of an object.
For a cigar-shaped object (like the outer membrane of a mitochondrion), with only one skeleton component the length and the mean radius can be calculated.
GCG
04.21
'''

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

class MyObjectProperties(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Test Obj Prop", default="Unknown")
    value1 = bpy.props.FloatProperty(name="Total length", default=0) #save value len
    value2 = bpy.props.FloatProperty(name="Average radius", default=0) #save value mean rad
    value3 = bpy.props.FloatProperty(name="value 3", default=0) #save value err mean rad

class SkelPanel(bpy.types.Panel):
     bl_label = "Skeletonize Panel"
     bl_idname = "Skel_panel"
     bl_space_type = "VIEW_3D"
     bl_region_type = "TOOLS"
     bl_category = "Skeletonize"

     def draw(self, context):
         layout = self.layout
         obj = context.active_object

         row = layout.row()
         row.label(text = "Skeletonize an object", icon = 'IPO_LINEAR')
         row = layout.row()
         row.operator("object.skeletonize")

         row = layout.row()
         row.label(text=obj.name, icon='ARROW_LEFTRIGHT')
         row.operator("object.len")
         row = layout.row()
         row.prop(obj.my_obj_props, "value1", text="Total length")

         row = layout.row()
         row.label(text=obj.name, icon='CURVE_NCIRCLE')
         row.operator("object.rad")
         row = layout.row()
         row.prop(obj.my_obj_props, "value2", text="Average radius")
         row = layout.row()
         row.prop(obj.my_obj_props, "value3", text="Error radius")


class Skeletonize(bpy.types.Operator):
     bl_idname = "object.skeletonize"
     bl_label = "skeletonize object"
     bl_options = {'REGISTER', 'UNDO'}
     def execute(self, context):
         dir = os.path.dirname(os.path.abspath(__file__))
         exe = os.path.join(dir,"bin/")
         tdir = tempfile.mkdtemp() #temporary folder I need to make this global, so the other classes can see tdir
         #print(tdir)
         meshname = bpy.context.object.data.name + str('.off')
         mesh_tmp = os.path.join(tdir,meshname)
         bpy.ops.export_mesh.off(filepath = mesh_tmp) #export mesh off format to the temporary folder
         cmd = os.path.join(os.path.dirname(__file__), 'bin', 'skeletonize')
         #if subprocess.call([cmd, mesh_tmp]):
         Proc = sp.call([cmd, mesh_tmp],cwd =tdir )
         if Proc != 0:
             print('skeletonize error')
         else:
             print('skeleton done')
         nr = []
         vertices = []
         skel_tmp = os.path.join(tdir,"skel-poly.cgal")
         f = open(skel_tmp, "r")
         for line in f:
             line_split = line.split()
             nr_points_per_line = np.int(line_split[0])
             nr.append(nr_points_per_line)
             temp_line = line_split[1:]
             fpoints = []
             for i in range(nr_points_per_line):
                 fpoints.append((float(temp_line[i*3]),float(temp_line[i*3+1]),float(temp_line[i*3+2])))
             vertices.append(fpoints)

         for i in vertices:
             verts = i
             edges = []
             for e in range(len(verts)-1):
                 edges.append([e,e+1])

             mymesh = bpy.data.meshes.new(bpy.context.object.data.name+"_ske")
             myobject = bpy.data.objects.new(bpy.context.object.data.name+"_ske",mymesh)

             bpy.context.scene.objects.link(myobject)

             mymesh.from_pydata(verts,edges,[])
             mymesh.update()

         return {'FINISHED'}

class LenObj(bpy.types.Operator):

    bl_idname = "object.len"
    bl_label = "Compute length object"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        nr = []
        verts = []
        skel_tmp = os.path.join(tdir,"skel-poly.cgal")
        f = open(skel_tmp, "r")
        for line in f:
            line_split = line.split()
            nr_points = np.int(line_split[0])
            nr.append(nr_points)
            temp_line = line_split[1:]
            fpoints = []
            for i in range(nr_points):
                fpoints.append((float(temp_line[i*3]),float(temp_line[i*3+1]),float(temp_line[i*3+2])))
            verts.append(fpoints)
            #verts is a list of lists with the vertices of each segment

             #I flatten the list
        new_verts = []
        for i in verts:
            for j in i:
                new_verts.append(j)

        anv = np.array(new_verts)
        n = len(anv)
        d = np.zeros((n,n))  #distance matrix

         #euclidean distance
        def dist(x1,y1,z1,x2,y2,z2):
            d = np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
            return d
         #norm of a vector
        def nor(vx,vy,vz):
            n = np.sqrt(vx**2+vy**2+vz**2)
            return n
         #scalar product
        def prod(vx,vy,vz,wx,wy,wz):
            p = vx*wx + vy*wy + vz*wz
            return p

        for i in range(n):
            for j in range(n):
                d[i,j] = dist(anv[i,0],anv[i,1],anv[i,2],anv[j,0],anv[j,1],anv[j,2])

         #look for the maximal distance to select the
          #np.amax(d) #max distance
        nrv1 = np.where(d==np.amax(d))[0][0]
        nrv2 = np.where(d==np.amax(d))[0][1]
        co_v1 = new_verts[nrv1]
        co_v2 = new_verts[nrv2]

        try:
            d[nrv1,nrv1+1] and d[nrv1,nrv1-1]
             #print(co_v1,'lower end')
            ext_inf = co_v1
        except:
             #print(co_v1,'upper end: do something ')
            ext_sup = co_v1

         #compute the length of the skeleton
        sd = 0
        for i in range(n-1):
            sd += dist(anv[i,0],anv[i,1],anv[i,2],anv[i+1,0],anv[i+1,1],anv[i+1,2])
         #print('Length skelethon:',sd, 'Max distance:',np.amax(d))
        #Max-Min coordinates
        co_v = []
        co_v.append(new_verts[nrv1]) #coords max
        co_v.append(new_verts[nrv2]) #coords min

        me_verts = []
        me_verts_norm = []

        for i in range(0,len(bpy.context.object.data.vertices)):
            me_verts.append((bpy.context.object.data.vertices[i].co[0],bpy.context.object.data.vertices[i].co[1],bpy.context.object.data.vertices[i].co[2]))
            me_verts_norm.append((bpy.context.object.data.vertices[i].normal[0],bpy.context.object.data.vertices[i].normal[1],bpy.context.object.data.vertices[i].normal[2]))

        #Length using the minimal distance from the skeleton to the mesh
        distancen = np.zeros(len(me_verts))
        distancen1 = np.zeros(len(me_verts))

        for i,j in enumerate(me_verts):
            x0 = j[0]
            y0 = j[1]
            z0 = j[2]
            distancen[i] = dist(co_v[0][0],co_v[0][1],co_v[0][2],x0,y0,z0)
        for i,j in enumerate(me_verts):
            x0 = j[0]
            y0 = j[1]
            z0 = j[2]
            distancen1[i] = dist(co_v[1][0],co_v[1][1],co_v[1][2],x0,y0,z0)
        #co_v1 extremo inferior
        if ext_inf == co_v1:
            nx = co_v1[0] - new_verts[nrv1+1][0]
            ny = co_v1[1] - new_verts[nrv1+1][1]
            nz = co_v1[2] - new_verts[nrv1+1][2]
        elif ext_sup == co_v1:
            nx = co_v1[0] - new_verts[nrv1-1][0]
            ny = co_v1[1] - new_verts[nrv1-1][1]
            nz = co_v1[2] - new_verts[nrv1-1][2]
     #print(co_v1,'ext_sup')
        ax = co_v1[0]
        ay = co_v1[1]
        az = co_v1[2]

        multi = 1.5 #def
        l_aux = []
        nr_aux = []
        for i,j in enumerate(me_verts):
            if distancen[i] < multi*np.amin(distancen):
                if (prod(me_verts_norm[i][0],me_verts_norm[i][1],me_verts_norm[i][2],nx,ny,nz)/(nor(float(me_verts_norm[i][0]),float(me_verts_norm[i][1]),float(me_verts_norm[i][2]))*nor(nx,ny,nz)) < 1.0):
                    l_aux.append(prod(me_verts_norm[i][0],me_verts_norm[i][1],me_verts_norm[i][2],nx,ny,nz)/(nor(float(me_verts_norm[i][0]),float(me_verts_norm[i][1]),float(me_verts_norm[i][2]))*nor(nx,ny,nz)))
                    nr_aux.append(i)

        if ext_inf == co_v1:
            nx = co_v2[0] - new_verts[nrv2-1][0]
            ny = co_v2[1] - new_verts[nrv2-1][1]
            nz = co_v2[2] - new_verts[nrv2-1][2]
        elif ext_sup == co_v1:
            nx = co_v2[0] - new_verts[nrv2+1][0]
            ny = co_v2[1] - new_verts[nrv2+1][1]
            nz = co_v2[2] - new_verts[nrv2+1][2]

        ax = co_v2[0]
        ay = co_v2[1]
        az = co_v2[2]

        l_aux1 = []
        nr_aux1 = []
        for i,j in enumerate(me_verts):
            if distancen1[i] < multi*np.amin(distancen1):
                if (prod(me_verts_norm[i][0],me_verts_norm[i][1],me_verts_norm[i][2],nx,ny,nz)/(nor(float(me_verts_norm[i][0]),float(me_verts_norm[i][1]),float(me_verts_norm[i][2]))*nor(nx,ny,nz)) < 1.0):
                    l_aux1.append(prod(me_verts_norm[i][0],me_verts_norm[i][1],me_verts_norm[i][2],nx,ny,nz)/(nor(float(me_verts_norm[i][0]),float(me_verts_norm[i][1]),float(me_verts_norm[i][2]))*nor(nx,ny,nz)))
                    nr_aux1.append(i)
        total_len = distancen[nr_aux[l_aux.index(max(l_aux))]] + distancen1[nr_aux1[l_aux1.index(max(l_aux1))]] + sd
#       #Approximation of the length using the minimal distance ot the mesh
#        print('total length: ',np.round(total_len,decimals=4))
        obj = context.active_object
        obj.my_obj_props.value1 = np.round(total_len,decimals=4)

        return {'FINISHED'}

class RadObj(bpy.types.Operator):
    """Calulate radius of my object"""
    bl_idname = "object.rad"
    bl_label = "Average radius object"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        nr = []
        verts = []
        skel_tmp = os.path.join(tdir,"skel-poly.cgal")
        f = open(skel_tmp, "r")
        for line in f:
            line_split = line.split()
            nr_points = np.int(line_split[0])
            nr.append(nr_points)
            temp_line = line_split[1:]
            fpoints = []
            for i in range(nr_points):
                fpoints.append((float(temp_line[i*3]),float(temp_line[i*3+1]),float(temp_line[i*3+2])))
            verts.append(fpoints)
         #verts is a list of lists with the vertices of each segment
         #print(verts)
         #I flatten the list, it contains all the vertices
        new_verts = []
        for i in verts:
            for j in i:
                new_verts.append(j)
        anv = np.array(new_verts)
        n = len(anv)
        d = np.zeros((n,n))  #distance matrix
      #euclidean distance
        def dist(x1,y1,z1,x2,y2,z2):
            d = np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
            return d

        for i in range(n):
            for j in range(n):
                d[i,j] = dist(anv[i,0],anv[i,1],anv[i,2],anv[j,0],anv[j,1],anv[j,2])
        #look for the maximal distance to select the
        np.amax(d) #max distance
        nrv1 = np.where(d==np.amax(d))[0][0]
        nrv2 = np.where(d==np.amax(d))[0][1]
        co_v1 = new_verts[nrv1]
        co_v2 = new_verts[nrv2]

        #compute the length of the skeleton
        sd = 0
        for i in range(n-1):
            sd += dist(anv[i,0],anv[i,1],anv[i,2],anv[i+1,0],anv[i+1,1],anv[i+1,2])
        #print('Length skelethon:',sd, 'Max distance:',np.amax(d))
       #Max-Min coordinates
        co_v = []
        co_v.append(new_verts[nrv1]) #coords max
        co_v.append(new_verts[nrv2]) #coords min
        co_v.append(sd) #distance segment
#
        me_verts = []
        for i in range(0,len(bpy.context.object.data.vertices)):
            me_verts.append((bpy.context.object.data.vertices[i].co[0],bpy.context.object.data.vertices[i].co[1],bpy.context.object.data.vertices[i].co[2]))

#         #point = () (the previous point)
        epsilon = 0.01
        li = []
#
        for i in range(n-1):
            norm_i = anv[i+1,0] - anv[i,0]
            norm_j = anv[i+1,1] - anv[i,1]
            norm_k = anv[i+1,2] - anv[i,2]
            d = -(norm_i*anv[i,0] + norm_j*anv[i,1] + norm_k*anv[i,2])
#             #x0,y0,z0 = # point in the meshes
            li_aux = [(anv[i,0],anv[i,1],anv[i,2])]
            for j in me_verts[1:]:
                x0 = j[0]
                y0 = j[1]
                z0 = j[2]
                dist_p_plane = np.abs(norm_i*x0 + norm_j*y0 + norm_k*z0 + d)/(np.sqrt(norm_i**2+norm_j**2+norm_k**2))
                if dist_p_plane < epsilon:
                    li_aux.append((x0,y0,z0))
            li.append(li_aux) #first point from the skeleton, and the rest from the mesh
        r = []
        di_or = []
        for i in li:
            di_or.append(dist(i[0][0],i[0][1],i[0][2],li[0][0][0],li[0][0][1],li[0][0][2]))
             #print(dist(i[0][0],i[0][1],i[0][2],li[0][0][0],li[0][0][1],li[0][0][2]))
            r_aux = []
            for j in i[1:]:
                r_aux.append(dist(i[0][0],i[0][1],i[0][2],j[0],j[1],j[2]))
            r.append(r_aux)

        ra_l = []
        s_ra_l = []
#         print(len(r))
        for i in r:
            ra_l.append(np.mean(i))
            s_ra_l.append(np.std(i))

        #plt.errorbar(di_or,ra_l,yerr =s_ra_l)
    #    print(np.round(np.mean(ra_l),decimals=3), np.round(np.std(ra_l),decimals=3))
        obj = context.active_object
        obj.my_obj_props.value2 = np.round(np.mean(ra_l),decimals=3)
        obj.my_obj_props.value3 = np.round(np.std(ra_l),decimals=3)
        return {'FINISHED'}
