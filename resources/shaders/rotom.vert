#version 330 core

// Fullscreen triangle strip generated from gl_VertexID alone, so no VBO
// or vertex attribute is required. The bound VAO can stay empty.
//
// Mapping (gl_VertexID -> NDC):
//   0 -> (-1, -1)
//   1 -> ( 1, -1)
//   2 -> (-1,  1)
//   3 -> ( 1,  1)

void main() {
    vec2 p = vec2(
        (gl_VertexID & 1) == 0 ? -1.0 : 1.0,
        (gl_VertexID & 2) == 0 ? -1.0 : 1.0
    );

    gl_Position = vec4(p, 0.0, 1.0);
}
