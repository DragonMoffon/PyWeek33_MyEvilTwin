#version 330

uniform float shift;
uniform int[13] values;

uniform vec3 color;

out vec4 fragColor;

void main() {
    float texel_x = gl_FragCoord.x/550 * 11 + shift;
    float texel_y = gl_FragCoord.y/72.0 * 3.0;

    int current_signal = int(texel_x);
    int next_signal = current_signal + 1;

    float through = fract(texel_x);
    float height = 3.0*values[current_signal];
    if (through > 0.9){
        height = mix(values[current_signal]*3.0, values[next_signal]*3.0, (through-0.9)/0.1);
    }

    float dist = abs(height - texel_y);

    fragColor = vec4(0.0);
    if (dist < 0.2){
        fragColor = vec4(color, 1);
    }
}
