#version 330 core

layout (location = 0) in vec3 position;

out vec3 skybox_tex_coords;

uniform mat4 projection;
uniform mat4 view;

void main()
{

    vec4 skybox_pos = projection * mat4(mat3(view)) * vec4(position, 1.0);
    gl_Position = skybox_pos.xyww;
    skybox_tex_coords = position;
}