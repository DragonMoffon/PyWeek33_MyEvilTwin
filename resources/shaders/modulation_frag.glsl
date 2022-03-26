#version 330

#define Pi 3.141592
const float[5] FREQUENCIES = float[5](0.5, 1.0, 1.5, 2.0, 3.0);

// Waves. The enemy waves are a list which
uniform vec4[5] twin_waves;
uniform vec3[17] player_waves;
uniform vec2 player_wave;

uniform float shift;
uniform float l_time;

uniform vec3 color;

out vec4 fragColor;

float dist_squared(vec2 pos, float x, float func){
    return pow(x-pos.x, 2) + pow(func - pos.y ,2);
}

float equation(float x, float peak, float frequency){
    int wave_in = 0 <= x && x <= frequency? 1 : 0;
    return 0.5*peak*(-cos(2*Pi*x/frequency)+1) * wave_in;
}



void main() {
    float texel_x = gl_FragCoord.x/550 * 11;
    float texel_y = (gl_FragCoord.y+1)/50 - 3;
    float twin_wave_x = texel_x / 3 + shift;

    float twin_dist = 1;

    for (int i = -3; i <= 3; i++){
        int wave_index = int(twin_wave_x+i*0.001);
        float wave_pos = mod(twin_wave_x+i*0.001, 1)*3;

        vec4 current_wave = twin_waves[wave_index];
        float twin_wave_y = equation(wave_pos, current_wave.x, FREQUENCIES[int(current_wave.y)]) * 2.5;

        float this_dist = dist_squared(vec2(texel_x, texel_y), wave_pos, twin_wave_y);

        twin_dist = this_dist < twin_dist? this_dist : twin_dist;
        if (twin_dist < 0.0016) break;
    }

    float player_wave_y = 0;
    for (int i = 0; i < 17; i++){
        vec3 check_wave = player_waves[i];
        if (check_wave[0] != 0){
            float frequency = FREQUENCIES[int(check_wave.y)];
            float time_since = (l_time - check_wave.z) - (texel_x - 3);
            if (0 <= time_since && time_since <= frequency){
                player_wave_y = equation(time_since, check_wave.x, frequency) * 2.5;
                break;
            }
        }
        else break;
    }

    float player_dist = pow(abs(player_wave_y - texel_y), 2);

    float test_dist = pow(abs(equation((texel_x-3+player_wave.y), player_wave.x, player_wave.y)*2.5 - texel_y), 2);

    fragColor = vec4(0.0, 0.0, 0.0, 0.0);
    if (twin_dist < 0.0016){
        fragColor += vec4(1.0, 0.0, 0.0, 1.0);
    }
    if (player_dist < 0.0016 || (test_dist < 0.0016 && texel_x < 3)){
        fragColor += vec4(color, 1);
    }
}
