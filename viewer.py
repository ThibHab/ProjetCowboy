#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from terrain import Terrain


class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("terrain.vert", "terrain.frag")
    # start rendering loop
    light_dir = (-0.5, -1, 0)
    terrain=Terrain(shader,200,light_dir=light_dir)
    axis=Axis(shader)
    viewer.add(axis)
    viewer.add(terrain)
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
