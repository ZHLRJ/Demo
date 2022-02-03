# -*- coding: utf-8 -*-
'''
@Time    : 11/15/21 
@Author  : Zhang Haoliang
'''
class MeshPooler:
    def __init__(self,Mesh):
        self.mesh=Mesh
        self.connection_map={}
        self.must_include_center_lst=[]
        self.NewEdgeMap=[]

    def update_connection_map(self,vertice_a,vertice_b):
        for vertice_a,vertice_b in [[vertice_a,vertice_b],[vertice_b,vertice_a]]:
            if vertice_a not in self.connection_map:
                self.connection_map[vertice_a]={vertice_b}
            else:
                if vertice_b not in self.connection_map[vertice_a]:
                    self.connection_map[vertice_a].add(vertice_b)
    # Generated a connection map to store the edge
    # {vertice_a:{vertice_b,vertice_c}, vertice_b:{vertive_a,...},...}
    def set_new_edge_to_connection_map(self):
        for vertice_a,vertice_b,vertice_c in self.mesh.triangles:
            # if vertice_a not in self.connection_map:
                self.update_connection_map(vertice_a,vertice_b)
                self.update_connection_map(vertice_b,vertice_c)
                self.update_connection_map(vertice_c,vertice_a)
    def can_be_center(self,p,radius,cover_lst):
        # check if there are center points in the radius of p. if so return false, else return true
        interest_lst=[p]
        visited= {p}
        r=0
        while r<radius:
            new_interest_lst=[]
            for i in range(len(interest_lst)):
                interest_p=interest_lst[i]
                interest_p_connection_map=self.connection_map[interest_p]
                for neighbor_p in interest_p_connection_map:
                    # neighbor_p=interest_p_connection_map[j]
                    if cover_lst[neighbor_p]==1:
                        return False
                    if neighbor_p not in visited:
                        visited.add(neighbor_p)
                        new_interest_lst.append(neighbor_p)
            interest_lst=new_interest_lst
            r+=1
        for point in interest_lst:
            if cover_lst[point]==1:
                self.NewEdgeMap.append([point,p])
        return True


    def get_center_points_lst(self,stride=2):
        radius=stride-1
        cover_lst= {} # Mark all the vertices as not visited
        # -1 not visited, 0 covered, 1 center
        for i in range(len(self.connection_map)):
            cover_lst[i]=-1

        # BFS
        queue=[]
        # specifing the center point
        for i in self.must_include_center_lst:
            cover_lst[i]=1
            queue.append(i)
        # If specify center point is None, set the idx 0 as initial center point
        if self.must_include_center_lst==[]:
            cover_lst[0]=1
            queue.append(0)

        while queue!=[]:
            s=queue.pop(0)
            s_connection=self.connection_map[s]
            # print(s,s_connection)
            # break
            for p in s_connection:
                # p=s_connection[i]
                if cover_lst[p]>=0:
                    continue
                if self.can_be_center(p,radius,cover_lst):
                    cover_lst[p]=1
                else:
                    cover_lst[p]=0
                queue.append(p)
        sample_points_lst=[]
        for i in range(len(cover_lst)):
            if cover_lst[i]==1:
                sample_points_lst.append(i)
        return sample_points_lst,self.NewEdgeMap





Pooler=MeshPooler(mesh)
Pooler.set_new_edge_to_connection_map()
center_point,NewEdgeMap=Pooler.get_center_points_lst(stride=2)
# print(Pooler.connection_map[0])
# Render(mesh.points,mesh.triangles,Center_point=center_point)
m=2
n=3
dp=[[0]*n for _ in range(m) ]
ALLdp=[[0]*n for _ in range(m) ]
for i in range(m):
    for j in range(n):
        ALLdp[i][j]=dp=[[0]*n for _ in range(m) ]
Value=[[0]*n for _ in range(m)]