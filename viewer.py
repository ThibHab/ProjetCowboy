#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import RotationControlNode, Shader, Viewer, Mesh, load, Node
from texture import CubeMapTexture, Texture, Textured
from terrain import Terrain
from transform import rotate, scale, translate
from water import River
from fire import Fire,Smoke
from cactus import Cactus, Cylinder

class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

class Skybox(CubeMapTexture):
    def __init__(self, shader, skybox_dir="desert_skybox/", ext="jpg"):
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
    map_size = 200
    SHADERS_FOLDER = "shaders/"

    viewer = Viewer()
    cactus_shader = Shader(SHADERS_FOLDER + "cactus.vert", SHADERS_FOLDER + "cactus.frag")
    terrain_shader = Shader(SHADERS_FOLDER + "terrain.vert", SHADERS_FOLDER + "terrain.frag")
    particle_shader = Shader(SHADERS_FOLDER + "particle.vert", SHADERS_FOLDER + "particle.frag")
    skybox_shader = Shader(SHADERS_FOLDER + "skybox.vert", SHADERS_FOLDER + "skybox.frag")
    river_shader = Shader(SHADERS_FOLDER + "water.vert", SHADERS_FOLDER + "water.frag")
    smoke_Shader = Shader(SHADERS_FOLDER + "Smoke_Particle.vert", SHADERS_FOLDER + "Smoke_Particle.frag")
    
    # start rendering loop
    light_dir = (-0.5, -1, 0)
    viewer.add(Skybox(skybox_shader))
    terrain=Terrain(terrain_shader,map_size,light_dir)
    river=River(river_shader,terrain.pente,light_dir)
    fire = Fire(particle_shader, light_dir)
    smoke = Smoke(smoke_Shader, light_dir)
    viewer.add(fire)
    viewer.add(smoke)
    viewer.add(terrain)
    viewer.add(terrain)
    viewer.add(river)
    viewer.add(Cactus(1.0, terrain.heigth, map_size, cactus_shader, light_dir))

    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped

