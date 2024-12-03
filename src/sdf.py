import taichi as ti
from taichi.math import length, vec2, vec3, min, max, dot, normalize
from enum import IntEnum

from .dataclass import Transform, SDFObject
from .config import MAX_DIS


class SHAPE(IntEnum):
    NONE = 0
    SPHERE = 1
    BOX = 2


@ti.func
def sd_none(_: vec3, __: vec3) -> float:
    return MAX_DIS


@ti.func
def sd_sphere(p: vec3, r: vec3) -> float:
    return length(p) - r.x


@ti.func
def sd_box(p: vec3, b: vec3) -> float:
    q = abs(p) - b
    return length(max(q, 0)) + min(q.max(), 0) - 0.03


SHAPE_FUNC = {
    SHAPE.NONE: sd_none,
    SHAPE.SPHERE: sd_sphere,
    SHAPE.BOX: sd_box,
}


@ti.func
def transform(t: Transform, p: vec3) -> vec3:
    p -= t.position
    p = t.matrix @ p
    return p


@ti.func
def calc_pos_scale(obj: SDFObject, p: vec3) -> tuple[vec3, vec3]:
    pos = transform(obj.transform, p)
    return pos, obj.transform.scale


@ti.func
def normal(shape: ti.template(), obj: SDFObject, p: vec3) -> vec3:
    pos, scale = calc_pos_scale(obj, p)
    n, h = vec3(0), 0.5773 * 0.005

    for i in ti.static(range(4)):
        e = 2.0*vec3((((i+3) >> 1) & 1), ((i >> 1) & 1), (i & 1))-1.0
        n += e*SHAPE_FUNC[shape](pos+e*h, scale)

    return normalize(n)
