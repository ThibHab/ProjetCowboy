#version 330 core

uniform vec3 global_color;
in vec4 frag_position;
in vec4 particle_color;

out vec4 out_color;

void main() {
    // calculate distance from center
    float distance = length(frag_position.xy);

    // set color based on distance from center
    if (distance > 0.5) {
        // red color for particles far from center
        out_color = vec4(1.0, 0.0, 0.0, 1.0);
    } else {
        // yellow color for particles close to center
        out_color = vec4(1.0, 1.0, 0.0, 1.0);
    }
    out_color *= particle_color;
}