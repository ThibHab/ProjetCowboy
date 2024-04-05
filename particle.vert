#version 330 core

in vec2 position;

uniform mat4 projection;
uniform vec2 offset;
uniform vec4 color;

out vec4 frag_position;
out vec4 particle_color;

void main()
{
    float scale = 10.0f;
    vec4 pos = vec4(position, 0.0, 1.0);
    pos.xy += offset;
    pos.xy *= scale;
    gl_Position = projection * pos;
    frag_position = pos;
    particle_color = color;
}