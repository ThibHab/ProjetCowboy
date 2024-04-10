#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load, Node
from texture import CubeMapTexture, Texture, Textured
from terrain import Terrain
from water import River
from fire import Fire,Smoke
import animation
from transform import quaternion, translate, identity, rotate, scale,vec,quaternion_from_euler


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
    terrain_shader = Shader("terrain.vert", "terrain.frag")
    particle_shader = Shader("particle.vert", "particle.frag")
    skybox_shader = Shader("skybox/skybox.vert", "skybox/skybox.frag")
    river_shader = Shader("water.vert", "water.frag")
    eagle_shader = Shader("eagle.vert","eagle.frag")
    translate_keys = {0: vec(0, 20, 20), 20: vec(0, 20, 20) }
    scale_keys = {0:1,20:1}
    rotate_keys = {0: quaternion(),10:quaternion_from_euler(0,-180,0),20:quaternion_from_euler(0,-360,0)}
    keynode = animation.KeyFrameControlNode(translate_keys, rotate_keys, scale_keys) 
    
    # start rendering loop
    light_dir = (-0.5, -1, 0)
    viewer.add(Skybox(skybox_shader))
    terrain=Terrain(terrain_shader,200,light_dir)
    river=River(river_shader,terrain.pente,light_dir)
    eagle=Node(load("Eagle.obj",eagle_shader))
    eagle.transform= translate(0,15,15) @ rotate ((0,1,0),90)
    keynode = animation.KeyFrameControlNode(translate_keys, rotate_keys, scale_keys) 
    keynode.add(eagle) 
    viewer.add(keynode)
    #viewer.add(Fire(particle_shader))
    #viewer.add(Smoke(particle_shader))
    viewer.add(terrain)
    viewer.add(river)
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
