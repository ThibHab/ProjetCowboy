import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np
from core import Shader, Viewer, Mesh

# -----------------------------------------------------------------------------
pointnumber = 128
w = 0.005
def createFire(shaderfire,shadersmoke, radius, height,offset):
    return Fire(shaderfire, radius, height,offset),Smoke(shadersmoke, radius, height,offset)

# -------------- Useful functions for fire -----------------------------
def generate_coords_cone(n, offset, radius, height):
    points = []
    r=radius
    a=height
    for i in range(n):

        #Computing values inside the cone
        h = a * (np.random.random()) ** (1/3)
        local_r = (r / a) * h * np.sqrt(np.random.random())
        t = 2 * np.pi * np.random.random()

        #assigning values to x,y,z
        x = local_r * np.cos(t)
        y =  h 
        z =  local_r*np.sin(t)
        points.append((x + offset[0], -y+a + offset[1] , z + offset[2] ))
    return tuple(map(tuple, points))

# -------------- Useful functions for smoke -----------------------------

def generate_coords_Cloud(n, offset, radius, height):
    points = []
    r=radius
    a=height
    for i in range(n):

        #Computing values inside the cloud
        local_r = (r * np.sqrt(np.random.random()))/2
        theta = np.random.random() * 2 * np.pi

        #assigning values to x,y,z
        x =  local_r * np.cos(theta) 
        y =  local_r * np.sin(theta) - a/3
        z =  r * np.sqrt(np.random.random())
        points.append(( x + offset[0], y + a + offset[1], z + offset[2]))
    return tuple(map(tuple, points))

# ----------------------- Fire ---------------------------------------
class Fire(Mesh):
    
    def __init__(self, shader, radius, height,offset):

        GL.glPointSize(15)
        self.offset=offset
        self.radius = radius
        self.height = height
        self.coords = generate_coords_cone(pointnumber, self.offset, self.radius, self.height)
        self.life = [np.random.random_integers(0, 0) for _ in range(pointnumber)]
        uniform=dict()

        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        super().__init__(shader, attributes=dict(position=self.coords), offset=self.offset,
                         usage=GL.GL_STREAM_DRAW, **uniform)

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        # Decrease TTL and reset position and TTL of dead particles
        coords_list  = list(self.coords)
        wind = np.random.random()
        for i in range(len(self.life)):
            self.life[i] -= 1
            # coords_list[i][1] = coords_list[i][1]
            if self.life[i] <= 0:
                coords_list[i] = generate_coords_cone(1, self.offset, self.radius, self.height )[0]
                self.life[i] = np.random.random_integers(100, 200)
            else:
                # Move the particle vertically upward
                coords_list[i] = (self.coords[i][0] + ( w *self.coords[i][2]/self.height ), self.coords[i][1] + 0.01, self.coords[i][2])
        
        self.coords = tuple(coords_list)
        # compute a sinusoidal x-coord displacement, different for each point.
        # this could be any per-point function: build your own particle system!
        dp = [[np.sin(i + glfw.get_time()), 0, 0] for i in range(len(self.coords))]

        # update position buffer on CPU, send to GPU attribute to draw with it
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')
        super().draw(primitives, attributes=dict(position=coords),offset=self.offset, **uniforms)

# ---------------------- Smoke ---------------------------------------

class Smoke(Mesh):
    
    def __init__(self, shader, radius, height,offset):

        
        GL.glPointSize(15)
        self.radius = radius
        self.height = height
        self.offset = offset
        self.coords = generate_coords_Cloud(pointnumber, self.offset, self.radius, self.height)
        self.life = [np.random.random_integers(0, 0) for _ in range(pointnumber)]

        uniform=dict()
        
        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        super().__init__(shader, attributes=dict(position=self.coords),offset=self.offset,
                         usage=GL.GL_STREAM_DRAW, **uniform)

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        # Decrease TTL and reset position and TTL of dead particles
        coords_list  = list(self.coords)
        wind = np.random.random()
        for i in range(len(self.life)):
            self.life[i] -= 1
            # coords_list[i][1] = coords_list[i][1]
            if self.life[i] <= 0:
                coords_list[i] = generate_coords_Cloud(1, self.offset, self.radius, self.height)[0]
                self.life[i] = np.random.random_integers(200, 500)
            else:
                # Move the particle vertically upward
                coords_list[i] = (self.coords[i][0] +( w *self.coords[i][2] / self.height ), self.coords[i][1] + 0.07, self.coords[i][2] + ( w *self.coords[i][2] / self.height ))
        
        self.coords = tuple(coords_list)
        # compute a sinusoidal x-coord displacement, different for each point.
        # this could be any per-point function: build your own particle system!
        dp = [[np.sin(i + glfw.get_time()), 0, 0] for i in range(len(self.coords))]

        # update position buffer on CPU, send to GPU attribute to draw with it
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')
        super().draw(primitives, attributes=dict(position=coords),offset=self.offset, **uniforms)
