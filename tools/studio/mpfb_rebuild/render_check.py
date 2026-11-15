"""Render a quick side + back check of the MPFB hero (body + hair + cape)."""
import bpy, os
from mathutils import Vector

OUT = "/home/hatch/workspace/mpfb_hero/checks"
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend")

scene = bpy.context.scene
# force the active action (Idle_Weapon), not the NLA stack: with use_nla=True
# all 7 strips play blended and the pose is a tangle (verified 11:33)
rig = bpy.data.objects['Human.rig']
rig.animation_data.use_nla = False
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
if bpy.data.actions['Idle_Weapon'].slots:
    rig.animation_data.action_slot = bpy.data.actions['Idle_Weapon'].slots[0]
scene.frame_set(1)  # deterministic idle pose (Idle_Weapon frame 1)
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 480
scene.render.resolution_y = 480
scene.cycles.device = 'CPU'
scene.cycles.samples = 16
scene.cycles.max_bounces = 2
scene.cycles.use_denoising = False

# light the scene a bit
sun = bpy.data.objects.get("Sun")
if not sun:
    sun_data = bpy.data.lights.new(name="Sun", type='SUN')
    sun_data.energy = 3.0
    sun = bpy.data.objects.new("Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (0.9, 0.0, 0.6)

def shot(name, loc, target=(0, 0, 0.9)):
    cam_data = bpy.data.cameras.new(name="Cam")
    cam_data.lens = 50
    cam = bpy.data.objects.new("Cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = Vector(loc)
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    print("CHECK SHOT:", name)

shot("cape_side.png", (2.2, -0.4, 1.0))
shot("cape_back.png", (0.0, 2.2, 1.0))
shot("hero_front.png", (0.0, -2.2, 1.1))
print("CHECKS DONE")
