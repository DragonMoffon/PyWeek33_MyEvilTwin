#version 330

#define Pi 3.141592

// Waves. The enemy waves are a list which
uniform vec4[5] enemy_waves;
uniform vec4 player_wave;

uniform float shift;
uniform ivec2 wave_max;
uniform vec3 color;

out vec4 fragColor;


float smootherStep(float f){
    return f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
}

float enemy_wave(float f, vec4 w_d){
    float M_mn = mod(w_d.z, 2) == 1? w_d.y*(w_d.z-1)/2 : w_d.y*w_d.z/2;
    float M_mx = mod(w_d.z, 2) == 1? w_d.y*(w_d.z-1)/2 : w_d.y*(w_d.z-2)/2;
    float M_q = w_d.y/2;
    float min_w = 1.5-M_q-M_mn, max_w = 1.5+M_q+M_mx;
    int wave_in = int(min_w+w_d.w <= f && f <= max_w+w_d.w);
    return 0.5*w_d.x*(cos(2*Pi*(f-1.5-w_d.w)/w_d.y)+1) * wave_in;
}

float player_wave_func(float f){
    int wave_in = int(0 <= f && f <= 3*player_wave.y);
    float x = fract(f)*3;
    return 0.5*player_wave.x*(cos(2*Pi*(x-player_wave.y/2)/player_wave.y)+1) * wave_in;
}

float dist_squared(vec2 pos, float x, float func){
    return pow(x-pos.x, 2) + pow(func - pos.y ,2);
}


void main() {
    float wave_shift = 1/150.0, wavePos = 0, waveHeight;
    float enemy_coord = gl_FragCoord.x + 1 + shift/wave_shift;
    float player_coord = gl_FragCoord.x + 1;

    int waveLower, waveHigher;

    bool near_line;
    float e_f = fract(enemy_coord*wave_shift);
    float p_f = fract(player_coord*wave_shift);
    waveLower = int(enemy_coord*wave_shift);
    float lowest_enemy_dist = 1, lowest_player_dist = 1;

    for (int i = -9; i <= 9; i++){
        float f_e = fract((enemy_coord*wave_shift)+i*0.001);
        float f_p = player_coord*wave_shift+i*0.001;

        float enemy_result = enemy_wave(f_e*3, enemy_waves[waveLower]);
        float player_result = f_p*3 <= 3? player_wave_func(f_p) : 0;
        f_p = fract(f_p);

        float e_func = enemy_result;
        float p_func = player_result;

        if (f_p <= 1) { e_func += player_result, p_func += enemy_result; }


        float enemy_dist = dist_squared(vec2(e_f, (gl_FragCoord.y-wave_max.y)/wave_max.x), f_e, e_func);
        float player_dist = dist_squared(vec2(p_f, (gl_FragCoord.y-wave_max.y)/wave_max.x), f_p, p_func);

        lowest_enemy_dist = enemy_dist < lowest_enemy_dist? enemy_dist : lowest_enemy_dist;
        lowest_player_dist = player_dist < lowest_player_dist? player_dist : lowest_player_dist;
    }


    fragColor = vec4(0);
    if (lowest_enemy_dist <= 0.0006){
        fragColor += vec4(color, 1);
    }
    if (lowest_player_dist <= 0.0006){
        fragColor += vec4(0.0, 0.0, 1.0, 1.0);
    }
}
