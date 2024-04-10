#version 330 core

in vec3 position;

uniform vec3 offset;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out float height;

void main() {
    height = (position.y-offset.y)/5;
    gl_Position = projection * view * model * vec4(position, 1);
}
