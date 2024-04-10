#version 330 core

uniform vec3 Kd;

out vec4 out_color;

void main() {

    out_color = vec4(Kd,1);
}