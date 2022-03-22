#version 330

in vec2 uv;

layout (location = 0) out vec4 fragColor;
layout (location = 1) out vec4 brightColor;

uniform sampler2D tex;

void main() {
    fragColor = texture(tex, uv, 0);

    float brightness = dot(fragColor.rgb, vec3(1, 1, 1));
    if (brightness > 1.0){
        brightColor = vec4(fragColor.rgb, 1.0);
    }
    else{
        brightColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}
