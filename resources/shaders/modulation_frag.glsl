#version 330

#define Pi 3.141592

// Waves. The enemy waves are a list which
uniform vec4[5] twin_waves;
uniform vec3[17] player_waves;
uniform vec2 player_wave;

uniform float shift;
uniform ivec2 ;
uniform vec3 color;

out vec4 fragColor;

float dist_squared(vec2 pos, float x, float func){
    return pow(x-pos.x, 2) + pow(func - pos.y ,2);
}


void main() {

}
