float fkernelSize = float(kernelSize);
int component     = int(round(mod(gl_FragCoord.x - 0.5, fkernelSize) +
    fkernelSize * mod(gl_FragCoord.y - 0.5, fkernelSize)));