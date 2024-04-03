#version 330 core

out vec4 out_color;

in vec3 skybox_tex_coords;

uniform samplerCube skybox_map;

void main()
{    
    out_color = texture(skybox_map, skybox_tex_coords);
}