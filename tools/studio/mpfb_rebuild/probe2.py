"""Probe 2: face orientation + eye/jaw/mouth landmarks (correct group names)."""
import bpy
from bl_ext.user_default.mpfb.services.humanservice import HumanService

def p(*a):
    print("[PROBE2]", *a)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

human = HumanService.create_human()
me = human.data

def group_center(name):
    if name not in human.vertex_groups:
        return None
    gi = human.vertex_groups[name].index
    vs = [v for v in me.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups)]
    if not vs:
        return None
    n = len(vs)
    return (n, tuple(round(sum(v.co[i] for v in vs) / n, 3) for i in range(3)),
            tuple(round(min(v.co[i] for v in vs), 3) for i in range(3)),
            tuple(round(max(v.co[i] for v in vs), 3) for i in range(3)))

for g in ("joint-l-eye", "joint-r-eye", "joint-head", "joint-jaw",
          "joint-mouth", "joint-neck", "joint-head-2", "ears", "scalp"):
    c = group_center(g)
    p(g, "->", c)

# eye sockets: verts very close to the eye group centers, find their y sign
# face direction: compare mean y of eye groups vs ears group
le = group_center("joint-l-eye")
re_ = group_center("joint-r-eye")
ea = group_center("ears")
if le and re_ and ea:
    p("eye mean y:", round((le[1][1] + re_[1][1]) / 2, 3), "ears mean y:", round(ea[1][1], 3))
    p("FACE IS", "+Y" if (le[1][1] + re_[1][1]) / 2 > ea[1][1] else "-Y")
p("DONE")
