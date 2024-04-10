#version 330 core

// global color
uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out float height;
out vec3 w_position, w_normal;

void main() {
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position =(model*vec4(position,1)).xyz;     

    height= length(position.xy)/30;

    gl_Position = projection * view * model * vec4(position, 1);
    
}
