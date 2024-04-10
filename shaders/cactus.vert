#version 330 core

uniform vec3 global_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
in vec3 position;
in vec3 normal;

out vec3 fragment_color;
out vec3 w_position, w_normal;   // in world coordinates

void main() {
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model * vec4(position, 1)).xyz;
    fragment_color = global_color;
    
    gl_Position = projection * view * model * vec4(position, 1);
}
