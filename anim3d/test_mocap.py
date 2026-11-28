import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(bpy.data.filepath))
from mocap import apply_bvh
from mathutils import Vector
sc = bpy.context.scene; rig = bpy.data.objects['Human.rig']
act = apply_bvh(rig, '/home/user/tools/cmu/data/010/10_01.bvh', 'kick')
rig.animation_data_create(); rig.animation_data.action = act
fr = [int(x) for x in sys.argv[sys.argv.index('--') + 1].split(',')]
print('RANGE', act.frame_range[:])
cam = bpy.data.cameras.new('c'); co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co; cam.lens = 28
l = bpy.data.lights.new('sun', 'SUN'); l.energy = 4; lo = bpy.data.objects.new('sun', l); lo.rotation_euler = (0.7, 0.2, 0.6); sc.collection.objects.link(lo)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.3, 0.35, 0.4, 1)
bpy.ops.mesh.primitive_plane_add(size=40); bpy.context.object.data.materials.append(bpy.data.materials.new('g')); bpy.context.object.active_material.diffuse_color = (0.1, 0.4, 0.1, 1)
sc.render.engine = 'BLENDER_EEVEE_NEXT' if os.environ.get('EEVEE') else 'CYCLES'; sc.cycles.samples = 16; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 480, 640
for f in fr:
    sc.frame_set(f); hip = rig.matrix_world @ rig.pose.bones['Hips'].head
    co.location = hip + Vector((0, -6, 0.5)); d = hip - co.location; co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f'/home/user/Filmler/anim3d/m_{f}.png'; bpy.ops.render.render(write_still=True)
