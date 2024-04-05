#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import CubeMapTexture, Texture, Textured
from texture import Texture, Textured 
 # import core classes
from math import sin, pi, cos, sqrt           # sinusoidal function used to animate
from random import randint,random

# -----------------------------------------------------------------------------
pointnumber = 128

#cone values Height then Radius
a= 50
r = 10
#wind
w = 0.1
dwind = 0.0 # derivative aka speed of wind
# -------------- Useful functions for fire -----------------------------
def generate_coords_cone(n):
    points = []

    for i in range(n):

        #Computing values inside the cone
        h = a * (random()) ** (1/3)
        local_r = (r / a) * h * sqrt(random())
        t = 2 * pi * random()

        #assigning values to x,y,z
        x = local_r*sin(t)
        y = local_r * cos(t)
        z = h
        points.append((x, y, -z+a))
    return tuple(map(tuple, points))

def compute_color_fire(coords):
    # Normalize the distance to range between 0 and 1
    distance = np.linalg.norm(np.array(coords), axis=1)
    normalized_distance = (distance - np.min(distance)) / (np.max(distance) - np.min(distance))
    # The closer the point to the center, the more yellow it gets, the farther away, the redder it gets
    colors = [( 2.0*d, 2.0*(1-d), 0, 1) for d in normalized_distance]
    return colors

# -------------- Useful functions for smoke -----------------------------

def generate_coords_Cloud(n):
    points = []

    for i in range(n):

        #Computing values inside the cloud
        local_r = (r * sqrt(random()))/2
        theta = random() * 2 * pi

        #assigning values to x,y,z
        x = r * sqrt(random()) 
        y = local_r * cos(theta)
        z = local_r * sin(theta) - a/3
        points.append((x, y, -z+ a/3))
    return tuple(map(tuple, points))


def compute_color_smoke(coords):
    # Normalize the distance to range between 0 and 1
    distance = np.linalg.norm(np.array(coords), axis=1)
    normalized_distance = (distance - np.min(distance)) / (np.max(distance) - np.min(distance))
    # The closer the point to the center, the more yellow it gets, the farther away, the redder it gets
    shade = random()
    colors = [( shade *0.5 , shade *0.5, shade *0.5, 1) for d in normalized_distance]
    return colors

# ----------------------- Fire ---------------------------------------
class Fire(Mesh):
    
    def __init__(self, shader):

        GL.glPointSize(37)
        self.coords = generate_coords_cone(pointnumber)
        self.colors = compute_color_fire(self.coords)
        self.life = [randint(500, 800) for _ in range(pointnumber)]


        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        super().__init__(shader, attributes=dict(position=self.coords, color=self.colors),
                         usage=GL.GL_STREAM_DRAW, global_color=(0.5, 0.5, 0.8))

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        # Decrease TTL and reset position and TTL of dead particles
        coords_list  = list(self.coords)
        wind = random()
        for i in range(len(self.life)):
            self.life[i] -= 1
            # coords_list[i][1] = coords_list[i][1]
            if self.life[i] <= 0:
                coords_list[i] = generate_coords_cone(1)[0]
                self.life[i] = randint(100, 200)
            else:
                # Move the particle vertically upward
                coords_list[i] = (self.coords[i][0] + ( w *self.coords[i][2]/a ), self.coords[i][1] + 0.02, self.coords[i][2])
        
        self.coords = tuple(coords_list)
        self.colors = compute_color_fire(self.coords)
        # compute a sinusoidal x-coord displacement, different for each point.
        # this could be any per-point function: build your own particle system!
        dp = [[sin(i + glfw.get_time()), 0, 0] for i in range(len(self.coords))]

        # update position buffer on CPU, send to GPU attribute to draw with it
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')
        super().draw(primitives, attributes=dict(position=coords), **uniforms)

# ---------------------- Smoke ---------------------------------------

class Smoke(Mesh):
    
    def __init__(self, shader):

        GL.glPointSize(37)
        self.coords = generate_coords_Cloud(pointnumber)
        self.colors = compute_color_smoke(self.coords)
        self.life = [randint(2000, 8000) for _ in range(pointnumber)]


        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        super().__init__(shader, attributes=dict(position=self.coords, color=self.colors),
                         usage=GL.GL_STREAM_DRAW, global_color=(0.5, 0.5, 0.8))

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        # Decrease TTL and reset position and TTL of dead particles
        coords_list  = list(self.coords)
        wind = random()
        for i in range(len(self.life)):
            self.life[i] -= 1
            # coords_list[i][1] = coords_list[i][1]
            if self.life[i] <= 0:
                coords_list[i] = generate_coords_Cloud(1)[0]
                self.life[i] = randint(100, 200)
            else:
                # Move the particle vertically upward
                coords_list[i] = (self.coords[i][0] +( w *self.coords[i][2] / a ), self.coords[i][1] + 0.07, self.coords[i][2])
        
        self.coords = tuple(coords_list)
        self.colors = compute_color_smoke(self.coords)
        # compute a sinusoidal x-coord displacement, different for each point.
        # this could be any per-point function: build your own particle system!
        dp = [[sin(i + glfw.get_time()), 0, 0] for i in range(len(self.coords))]

        # update position buffer on CPU, send to GPU attribute to draw with it
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')
        super().draw(primitives, attributes=dict(position=coords), **uniforms)


# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        loaded_texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=loaded_texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            loaded_texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=loaded_texture)

class Skybox(CubeMapTexture):
    def __init__(self, shader, skybox_dir="skybox/desert_skybox", ext="jpg"):
        # setup cube mesh to be textured
        base_coords = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), # left face
                    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]        # right face
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array([
                    0, 1, 2, 2, 3, 0,  # Back face
                    6, 5, 4, 4, 7, 6,  # Front face
                    7, 4, 0, 0, 3, 7,  # Left face
                    1, 5, 6, 6, 2, 1,  # Right face
                    2, 6, 7, 7, 3, 2,  # Top face
                    0, 4, 5, 5, 1, 0   # Bottom face
                ], np.uint32)
        
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'skybox_map'
        super().__init__(mesh, skybox_dir, ext)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    skybox_shader = Shader("skybox/skybox.vert", "skybox/skybox.frag")

    viewer.add(Skybox(skybox_shader))
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    viewer.add(Fire(shader))
    viewer.add(Smoke(shader))
    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        viewer.add(TexturedPlane(shader, "grass.png"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
