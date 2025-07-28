#ifdef KERNEL_LARGER_THAN_2
    int layer = component / 4;
    component = component % 4;
    ivec3 uvt = ivec3(
        gl_FragCoord.x / fkernelSize,
        gl_FragCoord.y / fkernelSize,
        layer
    );
#else
    ivec3 uvt = ivec3(
        gl_FragCoord.x / fkernelSize,
        gl_FragCoord.y / fkernelSize,
        0
    );
#endif
pixel = texelFetch(inputTextures, uvt, lod);