#ifdef USE_UNIFORM_WEIGHTS
    uniform vec4 bias[PLANE_COUNT];
    #ifdef USE_BATCH_NORMALIZATION
       uniform vec4 beta[PLANE_COUNT];
       uniform vec4 gamma[PLANE_COUNT];
       uniform vec4 movingMean[PLANE_COUNT];
       uniform vec4 movingVariance[PLANE_COUNT];
    #endif
#else
    _PLACEHOLDER_BIAS_CONSTANTS_
    #ifdef USE_BATCH_NORMALIZATION
       const vec4 beta[]           = vec4[](_PLACEHOLDER_BETA_);
       const vec4 gamma[]          = vec4[](_PLACEHOLDER_GAMMA_);
       const vec4 movingMean[]     = vec4[](_PLACEHOLDER_MOVINGMEAN_);
       const vec4 movingVariance[] = vec4[](_PLACEHOLDER_MOVINGVARIANCE_);
    #endif
#endif