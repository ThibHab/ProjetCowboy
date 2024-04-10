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
from fire import Fire,Smoke,createFire
import animation
from transform import quaternion, translate, identity, rotate, scale,vec,quaternion_from_euler
from cactus import Cactus, Cylinder,get_map_height_coords

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
    eagle_shader = Shader(SHADERS_FOLDER + "eagle.vert",SHADERS_FOLDER + "eagle.frag")

    # start rendering loop
    light_dir = (-0.5, -1, 0)
    viewer.add(Skybox(skybox_shader))
    terrain=Terrain(terrain_shader,map_size,light_dir)
    river=River(river_shader,terrain.pente,light_dir)
    spx,spy=np.random.randint(0,map_size),np.random.randint(0,map_size)
    x_pos = np.linspace(-50,50,map_size)[spx]
    z_pos = np.linspace(-50,50,map_size)[spy]
    y_pos = terrain.heigth[spx][spy]*7
    while(terrain.heigth[spx][spy]<0):
        spx,spy=np.random.randint(0,map_size),np.random.randint(0,map_size)
        x_pos = np.linspace(-50,50,map_size)[spx]
        z_pos = np.linspace(-50,50,map_size)[spy]
        y_pos = terrain.heigth[spx][spy]*7
    fire,smoke=createFire(particle_shader,smoke_Shader,2,5,(x_pos,y_pos,z_pos))

    eagle=Node(load("Eagle.obj",eagle_shader))
    translate_keys = {0: vec(0, 15, 15), 20: vec(0, 15, 15) }
    scale_keys = {0:1,20:1}
    rotate_keys = {0: quaternion(),10:quaternion_from_euler(0,-180,0),20:quaternion_from_euler(0,-360,0)}
    keynode = animation.KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    eagle.transform= translate(0,15,15) @ rotate ((0,1,0),90)
    keynode = animation.KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(eagle)
    viewer.add(terrain)
    viewer.add(river)
    viewer.add(Cactus(1.0, terrain.heigth, map_size, cactus_shader, light_dir))
    viewer.add(keynode)
    viewer.add(fire)
    viewer.add(smoke)

    print("\nKeys used : (for QWERTY keyboard)\n\nCactus\nAll keys used for the cactus are used to make a clockwise and a counter-clockwise rotation\n- move the left arm : KEY_LEFT and KEY_RIGHT\n- move the right arm : KEY_UP and KEY_DOWN \n- move the left forearm : KEY_KP_1 and KEY_KP_4 (numpad 1 and numpad 4)\n- move the right forearm : KEY_KP_3 and KEY_KP_6 (numpad 3 and numpad 6)\n\nAnimations\nSet time to 0 (used to reset animations) : KEY_SPACE (space bar)\n\nTextures\nChange polygon mode display : KEY_W\n\nGeneral\nQuit : KEY_Q or KEY_ESCAPE\n")

    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped

