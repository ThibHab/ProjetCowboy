#version 330 core

in float height;

out vec4 out_color;

vec3 gray = vec3(0.7, 0.7, 0.7);
vec3 black = vec3(0,0,0);

vec3 color(float dist){
    return mix(black,gray,dist);
}


void main() {
    vec3 col=color(height);

    out_color = vec4(col, 1);
}