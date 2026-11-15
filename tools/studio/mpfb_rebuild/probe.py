"""Probe MPFB mesh: shape keys, face-related vertex groups, eye landmarks."""
import bpy
from bl_ext.user_default.mpfb.services.humanservice import HumanService

def p(*a):
    print("[PROBE]", *a)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

human = HumanService.create_human()
me = human.data
p("verts:", len(me.vertices), "polys:", len(me.polygons))
me.calc_loop_triangles()
p("tris:", len(me.loop_triangles))
if me.shape_keys:
    p("shape keys:", [(kb.name, round(kb.value, 3)) for kb in me.shape_keys.key_blocks])
else:
    p("shape keys: NONE")
groups = [g.name for g in human.vertex_groups]
face_groups = [g for g in groups if any(k in g.lower() for k in
    ("eye", "head", "neck", "face", "jaw", "chin", "mouth", "nose", "brow", "ear", "scalp"))]
p("face-related groups:", face_groups)

def group_verts(name):
    if name not in human.vertex_groups:
        return []
    gi = human.vertex_groups[name].index
    return [v for v in me.vertices if any(g.group == gi for g in v.groups)]

for gname in ("l-eye", "r-eye", "eye", "head", "neck", "jaw", "chin"):
    vs = group_verts(gname)
    if vs:
        xs = [v.co.x for v in vs]; ys = [v.co.y for v in vs]; zs = [v.co.z for v in vs]
        p(f"group {gname}: n={len(vs)} x=[{min(xs):.3f},{max(xs):.3f}] "
          f"y=[{min(ys):.3f},{max(ys):.3f}] z=[{min(zs):.3f},{max(zs):.3f}] "
          f"center=({sum(xs)/len(xs):.3f},{sum(ys)/len(ys):.3f},{sum(zs)/len(zs):.3f})")

# front-face landmarks by geometry: head region verts with y > 0 (front half)
head = [v for v in me.vertices if v.co.z > 1.42]
front = [v for v in head if v.co.y > 0.0]
p("head verts z>1.42:", len(head), "front (y>0):", len(front))
if front:
    zs = sorted(v.co.z for v in front)
    p("front-face z range:", round(zs[0], 3), round(zs[-1], 3))
# nose tip: front-most vert in head region
nose = max(head, key=lambda v: v.co.y)
p("nose tip:", tuple(round(c, 3) for c in nose.co))
# eye line guess: front verts near z 1.55-1.60
eye_band = [v for v in front if 1.55 < v.co.z < 1.60]
if eye_band:
    xs = [v.co.x for v in eye_band]
    p("eye band z 1.55-1.60: n=", len(eye_band), "x range:", round(min(xs), 3), round(max(xs), 3))
p("DONE")
