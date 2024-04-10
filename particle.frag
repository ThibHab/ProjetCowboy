#version 330 core

uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

uniform vec3 light_dir;
uniform vec3 light_pos;

uniform vec3 w_camera_position;

in float height;
in vec3 w_position, w_normal;

out vec4 out_color;

vec3 yellow = vec3(1.0, 1.0, 0.0); // RGB for yellow
vec3 rouge = vec3(0.6941176470588235,0.13333333333333333,0.03529411764705882);


vec3 mieux(float dist){
    return mix(yellow,rouge,dist);
}


void main() {
    vec3 col=mieux(height);

    out_color = vec4(col, 1);
}