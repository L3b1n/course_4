#version 460

out vec2 v_uv;

void main()
{
    const vec4 v[] = vec4[](
        vec4(-1., -1.,  1.,  1.),
        vec4( 3., -1.,  1., -1.),
        vec4(-1.,  3., -1.,  1.)
    );
    
    gl_Position = vec4(v[gl_VertexID].xy, 0., 1.);
    v_uv        = v[gl_VertexID].zw;
}