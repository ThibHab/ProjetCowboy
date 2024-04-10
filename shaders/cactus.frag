#version 330 core

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 w_position, w_normal;   // in world coodinates

uniform vec3 w_camera_position;

uniform vec3 k_a;
uniform vec3 k_s;

uniform vec3 light_dir;

out vec4 out_color;

void main() {
    vec3 l = normalize(light_dir);
    vec3 n = normalize(w_normal);
    vec3 lambert = 0.7*fragment_color * max(dot(n, -l), 0);

    vec3 r = reflect(l, n);
    vec3 v = normalize(w_camera_position - w_position);
    vec3 phong = 0.5*fragment_color + lambert + vec3(0.2, 0.1, 0) * pow(max(dot(r, v), 0), 1.0);
    
    out_color = vec4(phong, 1);
}