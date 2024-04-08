#version 330 core

uniform vec3 k_d;
uniform vec3 k_s;
uniform vec3 k_a;
uniform float s;

uniform vec3 light_dir;

uniform vec3 w_camera_position;

in vec3 w_position, w_normal;

out vec4 out_color;

void main() {
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);
    
    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);
    vec3 res=k_a + diffuse_color + specular_color;
    out_color =vec4(res, 0.6);
    //out_color=vec4(col,0.4);
}