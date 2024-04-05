from core import Shader, Viewer, Mesh
import OpenGL.GL as GL 
import numpy as np


class River(Mesh):
    def __init__(self, shader,riverpath, index=None, usage=GL.GL_STATIC_DRAW, **uniforms):
        h,w=np.shape(riverpath)
        distrib=np.linspace(-50,50,h)
        grid=[]
        index=[]
        nb=0

        def initquad(x,y,nb):
            return [(distrib[x],riverpath[x][y],distrib[y]),
                   (distrib[x],riverpath[x][y+1],distrib[y+1]),
                   (distrib[x+1],riverpath[x+1][y],distrib[y]),
                   (distrib[x+1],riverpath[x+1][y+1],distrib[y+1])] , (nb*4,nb*4+1,nb*4+2 , nb*4+1,nb*4+3,nb*4+2)

        for i in range(0,h-1,2):
            for j in range(w-1,2):
                c=riverpath[i:i+3,j:j+3]
                for x in np.reshape(c,9):
                    if x<=0:
                        #probleme certains ce repete
                        a,b=initquad(i,j,nb)
                        nb+=1
                    break
        print(np.shape(grid))
        position = np.array(grid, 'f')
        self.color=(1,1,1)
        attributes = dict(position=grid)
        super().__init__(shader, attributes, index, usage, **uniforms)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives,global_colors=self.color, **uniforms)