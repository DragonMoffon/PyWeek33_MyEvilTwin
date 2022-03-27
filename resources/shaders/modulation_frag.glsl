#version 330

#define Pi 3.141592
const float[5] FREQUENCIES = float[5](0.5, 1.0, 1.5, 2.0, 3.0);

// Waves. The enemy waves are a list which
uniform vec4[5] twin_waves;
uniform vec3[17] player_waves;
uniform vec2 player_wave;

uniform float shift;
uniform float wave_speed;
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
    vec2 pos = vec2(texel_x, texel_y);
    float twin_wave_x = texel_x / 3 + shift;

    vec3 check_wave = vec3(0);
    for (int i = 0; i < 17; i++){
        vec3 this_wave = player_waves[i];
        if (this_wave[0] != 0){
            float frequency = FREQUENCIES[int(this_wave.y)];
            float time_since = (l_time - this_wave.z)*3*wave_speed - (texel_x - 3);
            if (0 <= time_since && time_since <= frequency){
                check_wave = this_wave;
                break;
            }
        }
        else break;
    }

    float twin_dist = 1;
    float valid_twin_height = 0;
    float test_dist = 1;
    float player_dist = 1;
    float valid_player_height = 0;
    float blend_dist = 1;
    float valid_blend_height = 0;
    for (int i = -5; i <= 5; i++){
        float texel_x_shift = texel_x+i*0.006;
        int wave_index = int(twin_wave_x+i*0.002);
        float wave_pos = mod(twin_wave_x+i*0.002, 1)*3;

        vec4 current_wave = twin_waves[wave_index];
        float twin_wave_y = equation(wave_pos, current_wave.x, FREQUENCIES[int(current_wave.y)]) * 2.5;

        float this_dist = dist_squared(pos, texel_x_shift, twin_wave_y);

        twin_dist = this_dist < twin_dist? this_dist : twin_dist;
        if (this_dist < twin_dist) {twin_dist = this_dist; valid_twin_height = twin_wave_y;}

        float test_wave_y = equation((texel_x_shift-3+player_wave.y), player_wave.x, player_wave.y)*2.5;

        this_dist = dist_squared(pos, texel_x_shift, test_wave_y);

        test_dist = this_dist < test_dist? this_dist : test_dist;

        float player_wave_y = equation(((l_time - check_wave.z)*3*wave_speed - (texel_x_shift - 3)),
                                       check_wave.x, FREQUENCIES[int(check_wave.y)])*2.5;

        this_dist = dist_squared(pos, texel_x_shift, player_wave_y);

        if (this_dist < player_dist) {player_dist = this_dist; valid_player_height = player_wave_y;}

        float blend_wave_y = twin_wave_y + player_wave_y;

        this_dist = dist_squared(pos, texel_x_shift, blend_wave_y);

        if (this_dist < blend_dist) {blend_dist = this_dist; valid_blend_height = blend_wave_y;}
        blend_dist = this_dist < blend_dist? this_dist : blend_dist;
    }

    bool blend = texel_x <= 4;

    twin_dist = blend? blend_dist : twin_dist;
    player_dist = blend? blend_dist : player_dist;

    fragColor = vec4(0.0, 0.0, 0.0, 0.0);
    if (twin_dist < 0.0016){
        fragColor += vec4(1.0, 0.0, 0.0, 1.0);
    }
    if (player_dist < 0.0016 || (test_dist < 0.0016 && texel_x < 3)){
        fragColor += vec4(color, 1);
    }
}
