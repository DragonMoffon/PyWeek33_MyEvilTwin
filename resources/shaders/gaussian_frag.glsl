#version 330

// The texture which we are blurring.
uniform sampler2D inImage;

// It takes far less to samples from a texture to just blur on the horizontal then vertically. 9+9 rather than 9x9.
uniform int horizontal;

out vec4 fragColor;

// A 9x9 Gaussian Blur Convolution Kernel.
const float[5] blurKernel = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);


// Take the all the pixels in a 9x9 around the current pixel and use the kernel to blend the colors together.
// This excludes the alpha as that causes the blur to become very difficult to see very quickly.
vec3 apply(ivec2 pixelPos, ivec2 shift){
    vec3 total = vec3(0.0);

    total += texelFetch(inImage, pixelPos, 0).rgb * blurKernel[0];

    for (int i = 1; i < 5; i++){
        total += texelFetch(inImage, pixelPos+shift*i, 0).rgb * blurKernel[i];
        total += texelFetch(inImage, pixelPos-shift*i, 0).rgb * blurKernel[i];
    }

    return total;
}


void main(){
    // texel coordinate we are writing to.
    ivec2 texelPos = ivec2(gl_FragCoord.xy);
    vec3 color = apply(texelPos, ivec2(horizontal, (1-horizontal)));

    // For the alpha to be correct we must additively apply the color to the texture later. So the alpha doesn't matter.
    fragColor = vec4(color, 1.0);
}
