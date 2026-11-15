"""CAPE + HERO FIX — pass 8: darken the hair-cap albedo + re-export.

The red-cap debug (run 5) proved the HairCap DOES render and covers the
crown from the front — but its albedo (0.16,0.11,0.07) renders as light
tan (225,176,114) under the slice scene's bright sun + toon shading
(~5.5x on the sun-facing crown), i.e. the same lightness as the skin,
so the hero reads BALD from the front. Fix at the source: darken the
Hair material in the .blend to (0.07,0.045,0.025) so the crown reads as
dark hair in direct sun while the back (less sun) stays brown, not black.
The HairCards strands texture is already dark brown, so this matches it.
"""
import bpy
import hashlib
import os

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"


def p(*a):
    print("[CAPEFIX8]", *a)


bpy.ops.wm.open_mainfile(filepath=BLEND)
m = bpy.data.materials['Hair']
bsdf = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
assert bsdf is not None
old = tuple(bsdf.inputs['Base Color'].default_value)
bsdf.inputs['Base Color'].default_value = (0.07, 0.045, 0.025, 1.0)
p("Hair base colour %s -> (0.07, 0.045, 0.025)" % (tuple(round(c, 3) for c in old),))
bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
md5 = hashlib.md5(open(GLB_OUT, 'rb').read()).hexdigest()
p("exported %s (%d bytes) md5=%s" % (GLB_OUT, os.path.getsize(GLB_OUT), md5))
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("CAPEFIX8 DONE, saved", BLEND)
