from core import Mesh, Node, RotationControlNode, load
from transform import rotate, scale, translate
import glfw
import numpy as np

def get_map_height_coords(height, heightMap, map_size):
    for row in range(map_size):
        for column in range(map_size):
            if heightMap[row][column] == height:
                return row + 5, column + 5

class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader, light_dir):
        super().__init__()
        self.add(*load('cylinder.obj', shader, global_color=(0.4, 0.45, 0), light_dir=light_dir))

class Cactus(Node):
    def __init__(self, height, height_map, map_size, cactus_shader, light_dir):
        #axis = Axis(cactus_shader)
        #viewer.add(axis)

        spx,spy = get_map_height_coords(height, height_map, map_size)

        arm_angle = 90
        forearm_angle = 0
        cactus_height = 3
        cactus_radius = 0.5

        cactus_x_pos = np.linspace(-50,50,map_size)[spx]
        cactus_z_pos = np.linspace(-50,50,map_size)[spy]
        cactus_y_pos = 7 + cactus_height

        cylinder = Cylinder(cactus_shader, light_dir)
        cactus_left_arm_shape = Node(children=[cylinder], transform=translate(-1, 1, 0) @ rotate((0, 0, 1), 90) @ scale(0.5, 1.5, 0.5))
        cactus_right_arm_shape = Node(children=[cylinder], transform=translate(1, 1, 0) @ rotate((0, 0, 1), 90) @ scale(0.5, 1.5, 0.5))
        cactus_left_forearm_shape = Node(children=[cylinder], transform=translate(-1.2, 1.2, 0) @ scale(0.5, 1.5, 0.5))
        cactus_right_forearm_shape = Node(children=[cylinder], transform=translate(1.2, 1.2, 0) @ scale(0.5, 1.5, 0.5))
        cactus_base = Node(children=[cylinder], transform=scale(cactus_radius, cactus_height, cactus_radius))

        transform_left_forearm = RotationControlNode(glfw.KEY_KP_1, glfw.KEY_KP_4, (1, 0, 0), forearm_angle, trans=(-1, 1, 0), children=[cactus_left_forearm_shape])
        transform_right_forearm = RotationControlNode(glfw.KEY_KP_3, glfw.KEY_KP_6, (1, 0, 0), forearm_angle, trans=(1, 1, 0), children=[cactus_right_forearm_shape])
        transform_left_arm = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, (0, 1, 0), arm_angle, children=[cactus_left_arm_shape, transform_left_forearm])
        transform_right_arm = RotationControlNode(glfw.KEY_UP, glfw.KEY_DOWN, (0, 1, 0), arm_angle, children=[cactus_right_arm_shape, transform_right_forearm])
        transform_cactus_base = Node(children=[cactus_base, transform_left_arm, transform_right_arm], transform=translate(cactus_x_pos, cactus_y_pos, cactus_z_pos))
        
        super().__init__(children=[transform_cactus_base])