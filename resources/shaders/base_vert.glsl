#version 330

in vec2 in_vert;
in vec2 in_uv;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
