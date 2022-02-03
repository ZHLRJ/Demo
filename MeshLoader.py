# -*- coding: utf-8 -*-
'''
@Time    : 11/2/21
@Author  : Zhang Haoliang
'''
import numpy as np
class Mesh:
    def __init__(self,fileName):
        # Test file
        self.fileName=fileName
        self.points=[]
        self.colors=[]
        self.triangles=[]

    def LoadOBJ(self):
        try:
            file=open(self.fileName)
            for f in file:
                line=f.split(' ')
                if line[0]=='v':
                    # Load the vertices with color
                    if len(line)>6:
                        self.points.append([float(line[1]), float(line[2]), float(line[3])])
                        self.colors.append([float(line[4]), float(line[5]), float(line[6])])
                    else:
                        self.points.append([float(line[1]), float(line[2]), float(line[3])])


                elif line[0]=='f':
                    self.triangles.append([int(line[1].split('//')[0])-1,int(line[2].split('//')[0])-1,
                                           int(line[3].split(
                        '//')[0])-1 ])

                    # print(self.triangles[-1])
                    # break
                else:continue
            self.points = np.array(self.points,dtype=np.float32)
            self.colors = np.array(self.colors,dtype=np.float32)
            self.triangles=np.array(self.triangles,dtype=np.int16)
            file.close()
        except IOError:
            print("The OBJ file not exist")
from Visualizer_opengl.visualizer import Render
fileName="/Users/mars_zhang/Downloads/mesh/downloadcode/MeshConvolution-master/data/DFAUST/template.obj"
mesh=Mesh(fileName)
mesh.LoadOBJ()
Render(mesh.points,mesh.triangles,Center_point=[1,2,3,4,5])
#
# def Boundary(objpoints):
#     x,y,z=objpoints[:,0],objpoints[:,1],objpoints[:,2]
#     print([x.min(),x.max()],[y.min(),y.max()],[z.min(),z.max()],"The mean",np.mean(objpoints,axis=0))
# # Boundary(mesh.points)
