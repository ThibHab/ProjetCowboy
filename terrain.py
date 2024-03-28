from core import Shader, Viewer, Mesh
import OpenGL.GL as GL 
import numpy as np
from perlin import testshow


class Terrain(Mesh):
    
    def __init__(self, shader,size,light_dir):
        distrib=np.linspace(-50,50,size)
        #grid=[(i,self.heigth(i,j,size),j) for j in distrib for i in distrib]
        pic=testshow(size,50)
        for i in range(size):
            for j in range(size):
                if pic[i][j]<=0.7:
                    pic[i][j]=0
        conv=np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
        conv=conv/np.sum(conv)
        low=testshow(size,100)+testshow(size,20)
        res=5*low+20*pic
        grid=[(distrib[i],res[i][j],distrib[j]) for j in range(size) for i in range(size)]
        index=[]
        for i in range(0,size-1):
            for j in range(size-1):
                index+=[i*size+j,(i+1)*size+j,i*size+j+1]
                index+=[(i+1)*size+j,(i+1)*size+j+1,i*size+j+1]
        position = np.array(grid, 'f')
        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1),(0, 0, 0),(1, 0, 1)), 'f')
        self.color = (0.6745, 0.4431, 0.29)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes,index=index)

    def heigth(self,x,z,size):
        return np.cos(x/2)*np.cos(z/2)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)