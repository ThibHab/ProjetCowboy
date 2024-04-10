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

vec3 base = vec3(0.6745, 0.4431, 0.29);
vec3 pale = vec3(0.674509803921,0.29411764705882354,0.12549019607843137);
vec3 orange = vec3(0.8549019607843137,0.41568627450980394,0.16470588235294117);
vec3 dark = vec3(0.3176470588235294,0.11372549019607843,0.06274509803921569);
vec3 rouge = vec3(0.49411764705882355,0.13333333333333333,0.03529411764705882);
float threshold = 0.09;

vec3 defColor(float height){
    if(height<-0.1){
        return dark;
    }
    if(height<0.05){
        return mix(dark,base,(height+0.1)/0.15);
    }
    if(height<0.3 && height>0.3-threshold){
        return mix(base,rouge,(height-0.3+threshold)/threshold);
    }
    if(height<0.5 && height>0.5-threshold){
        return mix(base,pale,(height-0.5+threshold)/threshold);
    }
    if(height<0.75 && height>0.75-threshold){
        return mix(base,orange,(height-0.75+threshold)/threshold);
    }
    if(height>0.3 && height<0.3+threshold){
        return mix(rouge,base,(height-0.3)/threshold);
    }
    if(height>0.5 && height<0.5+threshold){
        return mix(pale,base,(height-0.5)/threshold);
    }
    if(height>0.75 && height<0.75+threshold){
        return mix(orange,base,(height-0.75)/threshold);
    }
    return base;
}


void main() {
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);
    vec3 col=defColor(height);
    
    vec3 diffuse_color = col * max(dot(n, l), 0);
    
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);
    
    out_color = vec4(0.5*col, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
}