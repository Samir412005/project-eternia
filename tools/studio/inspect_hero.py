import bpy
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/blender-sources/project-eternia/hero/Warrior_Anime.blend')

def bounds(obj):
    me = obj.data
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

face = bpy.data.objects['Face']
fb = bounds(face)
print('FACE bounds x', round(fb[0],3), round(fb[1],3), ' y', round(fb[2],3), round(fb[3],3), ' z', round(fb[4],3), round(fb[5],3))
print('FACE centre', tuple(round((a+b)/2,3) for a,b in [(fb[0],fb[1]),(fb[2],fb[3]),(fb[4],fb[5])]))

# head surface: for a few (x,y) columns, max z of Face verts near that column
me = face.data
def surf_z(x0, y0, r=0.06):
    zs = [v.co.z for v in me.vertices if abs(v.co.x-x0)<r and abs(v.co.y-y0)<r]
    return round(max(zs),3) if zs else None
for (x,y) in [(0,-0.30),(0,-0.25),(0,-0.20),(0,0.0),(0,0.30),(0,0.35),(0.2,-0.2),(-0.2,-0.2),(0.25,0.1),(-0.25,0.1),(0,0.45)]:
    print('surf_z x=%.2f y=%.2f -> %s' % (x, y, surf_z(x,y)))
# forehead front surface y at given z (front of head)
def surf_y_front(z0, r=0.05):
    ys = [v.co.y for v in me.vertices if abs(v.co.z-z0)<r and abs(v.co.x)<0.1]
    return round(min(ys),3) if ys else None
for z in [2.55,2.6,2.65,2.7,2.75,2.8,2.85]:
    print('front y at z=%.2f -> %s' % (z, surf_y_front(z)))
def surf_y_back(z0, r=0.05):
    ys = [v.co.y for v in me.vertices if abs(v.co.z-z0)<r and abs(v.co.x)<0.1]
    return round(max(ys),3) if ys else None
for z in [2.55,2.6,2.65,2.7,2.75,2.8,2.85]:
    print('back y at z=%.2f -> %s' % (z, surf_y_back(z)))

# cape weights: which groups carry weight, sample verts top/mid/hem
cape = bpy.data.objects['Cape']
me = cape.data
print('CAPE groups:', [g.name for g in cape.vertex_groups])
from collections import Counter
cnt = Counter()
for v in me.vertices:
    for g in v.groups:
        if g.weight > 0.01:
            cnt[cape.vertex_groups[g.group].name] += 1
print('CAPE weight counts:', dict(cnt))
# sample specific verts: top row (z max), hem (z min), mid
verts = sorted(me.vertices, key=lambda v: v.co.z)
for label, v in [('top', verts[-1]), ('mid', verts[len(verts)//2]), ('hem', verts[0])]:
    print('CAPE', label, tuple(round(c,3) for c in v.co),
          [(cape.vertex_groups[g.group].name, round(g.weight,2)) for g in v.groups if g.weight>0.01])

# hair cards: per-vertex z histogram in crown region + which verts are high
hair = bpy.data.objects['HairCards']
hme = hair.data
print('HAIR groups:', [g.name for g in hair.vertex_groups])
hi = [(i, tuple(round(c,3) for c in v.co)) for i,v in enumerate(hme.vertices) if v.co.z > 2.80]
print('HAIR verts z>2.80:', len(hi))
for i, co in hi[:40]:
    print('  v%d %s' % (i, co))
# hair card polys: centroid + normal for first poly of each card region
for p in hme.polygons[:0]:
    pass
# group hair verts by z bands
import collections
bands = collections.Counter()
for v in hme.vertices:
    bands[round(v.co.z,1)] += 1
print('HAIR z bands:', dict(sorted(bands.items())))
