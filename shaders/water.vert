#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 w_position, w_normal;

uniform vec2 dir;
uniform float time;

void main() {
    
    float wave=20;
    float k=2*3.1415/wave;
    float c=2;
    float a=.25;

    float y= a * sin(k*(position.x -c*time)) * sin(k/0.5*(position.z -c*time))-0.3;
    vec3 pos=vec3(position.x,y,position.z);

    float nx=-k*a*cos(k*(position.x -c*time)) * sin(k*(position.z -c*time));
    float nz=-k/0.5*a*cos(k*(position.z -c*time)) * sin(k*(position.x -c*time));
    vec3 normal=vec3(nx,1,nz);

    w_normal = (model * vec4(normal, 0)).xyz;
    w_position =(model*vec4(pos,1)).xyz;
    gl_Position = projection * view * model * vec4(pos, 1);
    
}