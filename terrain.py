from core import Shader, Viewer, Mesh
import OpenGL.GL as GL 
import numpy as np
from perlin import perlin,fractale,slope,redistrib,fenetre,convolve2D
from water import River

def calculate_normals(grid, size):
    normals = []
    for x in range(size):
        for z in range(size):
            height = grid[x*size+z][1]
            dx, dz = 0, 0
            if x > 0:
                dx -= grid[(x-1)*size+z][1] - height
            if x < size - 1:
                dx += grid[(x+1)*size+z][1] - height
            if z > 0:
                dz -= grid[x*size+z-1][1] - height
            if z < size - 1:
                dz += grid[x*size+z+1][1] - height
            normal = (dx, -1., dz)
            normal = normal / np.sqrt(normal[0]**2+normal[1]**2+normal[2]**2)
            normals.append(normal)
    return normals

class Terrain(Mesh):

    def heigthmap(self,size):
        f,n=fractale(size,150,5)
        s=slope(f,size,0.9)
        baseriver=-redistrib(redistrib(s,n,2)-redistrib(s,n,4),1,1)
        river=np.zeros_like(baseriver)
        for i in range(size):
            for j in range(size):
                river[i][j]=1
                if baseriver[i][j]<-0.9:
                    river[i][j]=0
        self.pente=fenetre(convolve2D(river,7,5),-0.3,1)
        f,n=fractale(size,50,5)
        s=slope(f,size,0.5)
        res=redistrib(s,n,4)
        for i in range(size):
            for j in range(size):
                if self.pente[i][j]<0:
                    res[i][j]=self.pente[i][j]
                else:
                    res[i][j]*=self.pente[i][j]
        return res
    
    def __init__(self, shader,size,light_dir):
        distrib=np.linspace(-50,50,size)
        scale=7
        self.heigth=self.heigthmap(size)
        grid=[(distrib[i],scale*self.heigth[i][j],distrib[j]) for j in range(size) for i in range(size)]
        index=[]
        for i in range(0,size-1):
            for j in range(size-1):
                index+=[i*size+j,(i+1)*size+j,i*size+j+1]
                index+=[(i+1)*size+j,(i+1)*size+j+1,i*size+j+1]
        position = np.array(grid, 'f')
        normals=calculate_normals(grid,size)
        self.color = (0.6745, 0.4431, 0.29)
        attributes = dict(position=position,normal=normals)
        uniform=dict(
            light_dir=light_dir,
            k_s=(0.2382, 0.1093, 0),
            s=1)
        self.color=(0,0,1)
        super().__init__(shader, attributes=attributes,index=index,**uniform)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)