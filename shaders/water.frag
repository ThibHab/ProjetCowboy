#version 330 core

uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

uniform vec3 light_dir;
uniform vec3 light_pos;

uniform vec3 w_camera_position;

in vec3 w_position, w_normal;
in vec3 colors;

out vec4 out_color;

void main() {
    // vec3 n = normalize(w_normal);
    // vec3 l = normalize(-light_dir);
    // vec3 r = reflect(-l, n);
    // vec3 v = normalize(w_camera_position - w_position);
    // vec3 col=defColor(height);
    
    // vec3 diffuse_color = col * max(dot(n, l), 0);
    
    // vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);
    
    //out_color = vec4(0.5*col, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
    out_color=vec4(colors,0.4);
}