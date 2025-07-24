#ifdef USE_WEIGHT_BUFFERS
#ifdef USE_COMPONENT_R_PLANE_0
layout(STORAGE_FORMAT,binding = 2) VARIABLE_SPECIFIER weightMatrix1 {
    FLOAT_PRECISION vec4 weights1[NUM_INPUT_PLANES * N_DIMS];
};
#endif
...
#endif