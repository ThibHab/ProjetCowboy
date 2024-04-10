from core import Shader, Viewer, Mesh
import OpenGL.GL as GL 
import numpy as np
import glfw


class River(Mesh):
    def __init__(self, shader,riverpath,ld, index=None, usage=GL.GL_STATIC_DRAW, **uniforms):
        h,w=np.shape(riverpath)
        distrib=np.linspace(-50,50,h)
        grid=[]
        index=[]
        nb=0

        for i in range(0,h-1):
            for j in range(w-1):
                c=riverpath[i:i+2,j:j+2]
                for x in np.reshape(c,4):
                    if x<0.5:
                        grid+=[(distrib[i],riverpath[i][j],distrib[j]),
                                (distrib[i],riverpath[i][j+1],distrib[j+1]),
                                (distrib[i+1],riverpath[i+1][j],distrib[j]),
                                (distrib[i+1],riverpath[i+1][j+1],distrib[j+1])]
                        index+=(nb*4,nb*4+1,nb*4+2 , nb*4+1,nb*4+3,nb*4+2)
                        nb+=1
                    break
        print(np.shape(grid))
        self.color=(0,0,1)
        attributes = dict(position=grid)
        r=np.random.uniform(0,2*3.1416)
        uniform=dict(k_d=(0,0,1),
                     k_s=(1,1,1),
                     k_a=(0.00235294117,0.00235294117,0.04823529411),
                     s=10,
                     light_dir=ld,
                     time=0)
        super().__init__(shader, attributes, index, usage, **uniform)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        uniforms["time"]=glfw.get_time()
        super().draw(primitives=primitives,global_colors=self.color, **uniforms)