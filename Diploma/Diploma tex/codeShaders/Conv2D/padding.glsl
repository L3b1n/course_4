FLOAT_PRECISION vec2 replicatePadding(FLOAT_PRECISION vec2 sourceCoords)
{
    FLOAT_PRECISION vec2 repCoords    = vec2(0.0, 0.0);
    FLOAT_PRECISION vec2 offsetCoords = vec2(0.5, 0.5);
    repCoords.x = (sourceCoords.x >= 1.0f) ?
        2.0 - sourceCoords.x - offsetCoords.x :
        0.0 - sourceCoords.x + offsetCoords.x;
    repCoords.y = (sourceCoords.y >= 1.0f) ?
        2.0 - sourceCoords.y - offsetCoords.y :
        0.0 - sourceCoords.y + offsetCoords.y;
    return repCoords;
}

FLOAT_PRECISION vec2 checkboardPadding(FLOAT_PRECISION vec2 sourceCoords)
{
    FLOAT_PRECISION vec2 repCoords    = vec2(0.0, 0.0);
    FLOAT_PRECISION vec2 offsetCoords = vec2(0.5, 0.5);
    repCoords.x = (sourceCoords.x >= 1.0f) ?
        sourceCoords.x - 1.0f + offsetCoords.x :
        sourceCoords.x + 1.0f + offsetCoords.x;
    repCoords.y = (sourceCoords.y >= 1.0f) ?
        sourceCoords.y - 1.0f + offsetCoords.y :
        sourceCoords.y + 1.0f + offsetCoords.y;
    return repCoords;
}