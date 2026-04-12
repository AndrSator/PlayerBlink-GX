""" GLSL shader registry and loader.

Shader sources live as plain GLSL files under ``resources/shaders/``
(see :data:`src.constants.Constants.SHADERS_DIR`). Each shader is a
pair of files with the same base name:

    <name>.vert    GLSL vertex shader source
    <name>.frag    GLSL fragment shader source

Add a new shader by dropping two files with the same base name in that
directory; nothing in this module needs to change. Use :func:`load_shader`
to read both sources at runtime — it returns a :class:`Shader` dataclass
that callers can hand straight to
``QOpenGLShaderProgram.addShaderFromSourceCode``.
"""
from dataclasses import dataclass

from src.constants import Constants as Const


@dataclass(frozen=True)
class Shader:
    name: str
    vertex: str
    fragment: str


def load_shader(name: str) -> Shader:
    """ Read the vertex and fragment sources for a named shader.

    Raises FileNotFoundError if either file is missing.
    """
    vert_path = Const.SHADERS_DIR / f"{name}.vert"
    frag_path = Const.SHADERS_DIR / f"{name}.frag"

    if not vert_path.is_file():
        raise FileNotFoundError(
            f"Vertex shader not found: {vert_path}")
    if not frag_path.is_file():
        raise FileNotFoundError(
            f"Fragment shader not found: {frag_path}")

    return Shader(
        name=name,
        vertex=vert_path.read_text(encoding="utf-8"),
        fragment=frag_path.read_text(encoding="utf-8"),
    )


def available_shaders() -> list[str]:
    """ Names of all shaders with BOTH a .vert and a .frag in SHADERS_DIR """
    verts = {p.stem for p in Const.SHADERS_DIR.glob("*.vert")}
    frags = {p.stem for p in Const.SHADERS_DIR.glob("*.frag")}
    return sorted(verts & frags)


__all__ = ["Shader", "load_shader", "available_shaders"]
