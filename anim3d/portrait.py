import bpy, math, sys
from mathutils import Vector
out = sys.argv[sys.argv.index('--') + 1]
sc = bpy.context.scene
rig = bpy.data.objects['Human.rig']
cam = bpy.data.cameras.new('c'); co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
cam.lens = 50
import os
if os.environ.get('FACE'): cam.lens = 70; co.location = (0, -1.05, 1.56); co.rotation_euler = (math.radians(90), 0, 0)
else: co.location = (0, -3.4, 1.35); co.rotation_euler = (math.radians(88), 0, 0)
def light(name, loc, energy, size, col=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = col; o = bpy.data.objects.new(name, l); o.location = loc
    sc.collection.objects.link(o); d = Vector((0, 0, 1.2)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
light('key', (-2, -2.5, 2.6), 900, 2); light('rim', (2, 2, 2.4), 700, 1.5, (0.85, 0.9, 1)); light('fill', (2.5, -2, 1.2), 250, 3)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.05, 0.07, 0.1, 1)
sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = True; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y = 720, 1280; sc.render.filepath = out; sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -1.3
print('OBJS', [o.name for o in bpy.data.objects])
bpy.ops.render.render(write_still=True)
