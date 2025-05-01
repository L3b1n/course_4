#define FLOAT_PRECISION _PLACEHOLDER_PRECISION_

precision FLOAT_PRECISION float;
precision FLOAT_PRECISION sampler2D;
precision FLOAT_PRECISION sampler2DArray;

#if PLANE_COUNT > 0
layout(location = 0) out vec4 o_pixel;
#endif
#if PLANE_COUNT > 1
layout(location = 1) out vec4 o_pixel1;
#endif
#if PLANE_COUNT > 2
layout(location = 2) out vec4 o_pixel2;
#endif
#if PLANE_COUNT > 3
layout(location = 3) out vec4 o_pixel3;
#endif

_PLACEHOLDER_UNIFORMS_DECLARATION_

void main() {
    int lod = 0;
    ivec2 outLoc = ivec2(gl_FragCoord.xy);
    int layer = _PLACEHOLDER_LAYER_;
#if PLANE_COUNT > 1
    int layer1 = layer + 1;
#endif
#if PLANE_COUNT > 2
    int layer2 = layer + 2;
#endif
#if PLANE_COUNT > 3
    int layer3 = layer + 3;
#endif

#ifdef INPUT_TEXTURE_2D
    vec4 s = texelFetch(inputTextures0, ivec2(outLoc), 0);
#else
    vec4 s = texelFetch(inputTextures0, ivec3(outLoc, layer), 0);
#endif
#if PLANE_COUNT > 1
#ifdef INPUT_TEXTURE_2D
    s = texelFetch(inputTextures0, ivec2(outLoc), 0);
#else
    s = texelFetch(inputTextures0, ivec3(outLoc, layer1), 0);
#endif
#endif
#if PLANE_COUNT > 2
#ifdef INPUT_TEXTURE_2D
    s = texelFetch(inputTextures0, ivec2(outLoc), 0);
#else
    s = texelFetch(inputTextures0, ivec3(outLoc, layer2), 0);
#endif
#endif
#if PLANE_COUNT > 2
#ifdef INPUT_TEXTURE_2D
    s = texelFetch(inputTextures0, ivec2(outLoc), 0);
#else
    s = texelFetch(inputTextures0, ivec3(outLoc, layer3), 0);
#endif
#endif

    _PLACEHOLDER_ACTIVATION_
    o_pixel = s;
#if PLANE_COUNT > 1
    o_pixel1 = s;
#endif
#if PLANE_COUNT > 2
    o_pixel2 = s;
#endif
#if PLANE_COUNT > 3
    o_pixel3 = s;
#endif
}