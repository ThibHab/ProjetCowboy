#version 330 core

uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

uniform vec3 light_dir;
uniform vec3 light_pos;

uniform vec3 w_camera_position;

in vec3 fragment_color;
in vec3 w_position, w_normal;

out vec4 out_color;

void main() {
    vec3 n=normalize(w_normal);
    vec3 l=normalize(light_dir);
    vec3 lambert=k_d*max(dot(n,-l),0);

    vec3 r=reflect(l,n);
    vec3 v=normalize(w_camera_position-w_position);
    vec3 spec=k_s*pow(max(dot(r,v),0),s);
    
    vec3 phong=k_a+lambert+spec;
    out_color = vec4(phong, 1);
}