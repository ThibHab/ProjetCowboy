#version 330 core

in float height;

out vec4 out_color;

vec3 yellow = vec3(1.0, 1.0, 0.0); // RGB for yellow
vec3 rouge = vec3(0.6941176470588235,0.13333333333333333,0.03529411764705882);


vec3 color(float dist){
    return mix(yellow,rouge,dist);
}


void main() {
    vec3 col=color(height);

    out_color = vec4(col, 1);
}