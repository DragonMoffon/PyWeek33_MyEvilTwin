#version 330

// Takes the HDR game frame buffer and clamps it to be between 0.0 and 1.0 for actual drawing.
out vec4 FragColor;

in vec2 uv;

uniform float exposure;

uniform sampler2D scene;
uniform sampler2D bloomBlur;

void main() {
    const float gamma = 2.2;
    vec3 hdrColor = texture(scene, uv).rgb;
    vec3 bloomColor = texture(bloomBlur, uv).rgb;
    hdrColor += bloomColor; // additive blending
    // tone mapping
    vec3 result = vec3(1.0) - exp(-hdrColor * exposure);
    // also gamma correct while we're at it
    result = pow(result, vec3(1.0 / gamma));
    FragColor = vec4(result, 1.0);
}
