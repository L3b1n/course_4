#ifdef INPUT_TEXTURE_2D
    vec4 s = texelFetch(inputTextures0, ivec2(outLoc), 0);
#else
    vec4 s = texelFetch(inputTextures0, ivec3(outLoc, layer), 0);
#endif