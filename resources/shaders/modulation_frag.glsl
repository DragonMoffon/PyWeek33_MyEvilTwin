#version 330

uniform float[10] wave_data;
uniform ivec2 wave_max;
uniform vec3 color;

out vec4 fragColor;


float smootherStep(float f){
    return f * f * f * (f * (f * 6.0 - 15.0) + 1.0);
}


void main() {
    float wavePos = gl_FragCoord.x/530 * 9;
    int waveLower = int(wavePos);
    int waveHigher = int(min(wavePos+1, 9));
    float waveShift = smootherStep(fract(wavePos));

    int waveHeight = int(mix(wave_data[waveLower], wave_data[waveHigher], waveShift) * wave_max.x);
    float diff = abs(gl_FragCoord.y-wave_max.y);
    fragColor = vec4(0);
    if (diff <= 2){
        fragColor = vec4(color*2, 1);
    }
}
