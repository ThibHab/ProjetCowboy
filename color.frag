#version 330 core

// global color variable
uniform vec3 global_color;
in vec3 position;

// receiving interpolated color for fragment shader
in vec3 fragment_color;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    out_color = vec4(0.8,1-(pos.y + 13)/10,0,1);
}