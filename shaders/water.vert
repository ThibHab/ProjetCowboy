#version 330 core

// global color
uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 colors;
out vec3 w_position, w_normal;

void main() {
    vec3 normal=vec3(0,0,0);
    float h;
    if(position.y>0){
        h=0.05*sin(position.x);
    }else{
        h=0.2*sin(position.x);
    }
    vec3 pos=vec3(position.x,h,position.z);
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position =(model*vec4(pos,1)).xyz;
    colors=global_color;
    gl_Position = projection * view * model * vec4(pos, 1);
    
}