# Penalty replay scene (Blender/Cycles): MPFB humans + CMU mocap kick (mirrored -> left foot), keeper dive, stadium, crowd, floodlights.
# Run: blender -b grimaldo.blend -P scene.py -- <shot: kick|celebrate> <out_prefix> [frames a-b] [res_pct]
import bpy, sys, os, math, random
from mathutils import Vector, Euler
sys.path.insert(0, os.path.dirname(bpy.data.filepath))
from mocap import apply_bvh
args = sys.argv[sys.argv.index('--') + 1:]
SHOT, OUT = args[0], args[1]
FR = args[2] if len(args) > 2 else None
sc = bpy.context.scene; sc.render.fps = 24
random.seed(7)
HERE = os.path.dirname(bpy.data.filepath)
# ---------- materials helpers ----------
def mat(name, col, rough=0.6, emit=None, strength=0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = strength
    return m
def add(obj, m=None):
    sc.collection.objects.link(obj)
    if m: obj.data.materials.append(m)
    return obj
# ---------- pitch ----------
bpy.ops.mesh.primitive_plane_add(size=1); pitch = bpy.context.object; pitch.scale = (105, 68, 1)
pm = bpy.data.materials.new('pitch'); pm.use_nodes = True; nt = pm.node_tree; b = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(HERE, 'pitch.png')); tex.interpolation = 'Cubic'
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 900; noise.inputs['Detail'].default_value = 6
mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 0.35
nt.links.new(tex.outputs['Color'], mul.inputs['A']); nt.links.new(noise.outputs['Color'], mul.inputs['B']); nt.links.new(mul.outputs['Result'], b.inputs['Base Color'])
bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25; nt.links.new(noise.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
b.inputs['Roughness'].default_value = 0.85; pitch.data.materials.append(pm)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.01)); ap = bpy.context.object; ap.scale = (150, 110, 1); ap.data.materials.append(mat('apron', (0.13, 0.3, 0.12), 0.9))
# ---------- goal (+x end) ----------
GX = 52.5; white = mat('post', (0.95, 0.95, 0.95), 0.25)
def cyl(p1, p2, r=0.06, m=white):
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(p1 + p2) / 2, vertices=24)
    o = bpy.context.object; o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); o.data.materials.append(m); return o
cyl((GX, -3.66, 0), (GX, -3.66, 2.44)); cyl((GX, 3.66, 0), (GX, 3.66, 2.44)); cyl((GX, -3.72, 2.44), (GX, 3.72, 2.44))
netm = mat('net', (0.92, 0.92, 0.92), 0.6)
def net_plane(verts, nx, ny, name):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=nx, y_subdivisions=ny, size=1); o = bpy.context.object; o.name = name
    me = o.data
    for v in me.vertices:
        u, w = v.co.x + 0.5, v.co.y + 0.5
        a, b2, c, d2 = [Vector(p) for p in verts]
        v.co = a.lerp(b2, u).lerp(d2.lerp(c, u), w)
    wf = o.modifiers.new('wf', 'WIREFRAME'); wf.thickness = 0.012; o.data.materials.append(netm); return o
D = 1.9
back = net_plane([(GX + D, -3.66, 0), (GX + D, 3.66, 0), (GX + D * 0.75, 3.66, 2.44), (GX + D * 0.75, -3.66, 2.44)], 70, 24, 'netback')
net_plane([(GX, -3.66, 2.44), (GX, 3.66, 2.44), (GX + D * 0.75, 3.66, 2.44), (GX + D * 0.75, -3.66, 2.44)], 70, 12, 'nettop')
for z in (-3.66, 3.66): net_plane([(GX, z, 0), (GX + D, z, 0), (GX + D * 0.75, z, 2.44), (GX, z, 2.44)], 18, 24, 'netside')
# net bulge: lattice-free shape key on the back net driven by keyframes
back.shape_key_add(name='base'); sk = back.shape_key_add(name='bulge'); IMPACT = Vector((GX + D, 3.0, 0.4))
for i, v in enumerate(back.data.vertices):
    dist = (Vector((v.co.x, v.co.y, v.co.z)) - IMPACT); w = math.exp(-(dist.y ** 2 + dist.z ** 2) / 1.2)
    sk.data[i].co = v.co + Vector((0.85 * w, 0, 0))
# ---------- stands + crowd ----------
seat = mat('seat', (0.03, 0.22, 0.1), 0.7)
crowd_cols = [(0.9, 0.92, 0.9), (0.04, 0.42, 0.18), (0.05, 0.55, 0.22), (0.95, 0.95, 0.95), (0.08, 0.08, 0.09), (0.7, 0.75, 0.72), (0.6, 0.08, 0.06), (0.1, 0.15, 0.35)]
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, segments=10, ring_count=6); headp = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.55, vertices=10, location=(0, 0, -0.35)); bodyp = bpy.context.object
headp.select_set(True); bodyp.select_set(True); bpy.context.view_layer.objects.active = headp; bpy.ops.object.join(); fan = bpy.context.object; fan.name = 'fanproto'
fm = bpy.data.materials.new('fan'); fm.use_nodes = True; fnt = fm.node_tree; oi = fnt.nodes.new('ShaderNodeObjectInfo'); ramp = fnt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.interpolation = 'CONSTANT'; els = ramp.color_ramp.elements
for i, c in enumerate(crowd_cols):
    e = els[i] if i < 2 else els.new(i / len(crowd_cols)); e.position = i / len(crowd_cols); e.color = (*c, 1)
fnt.links.new(oi.outputs['Random'], ramp.inputs['Fac']); fnt.links.new(ramp.outputs['Color'], fnt.nodes['Principled BSDF'].inputs['Base Color']); fm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
fan.data.materials.append(fm); fan.hide_render = True; fan.hide_viewport = True
coll = bpy.data.collections.new('crowd'); sc.collection.children.link(coll)
def stand(cx, cy, rot, length, rows=24):
    for r in range(rows):
        bpy.ops.mesh.primitive_cube_add(size=1); st = bpy.context.object; st.scale = (length + r * 1.2, 0.85, 0.5)
        off = Vector((0, -(4 + r * 0.85), 0.6 + r * 0.5)); off.rotate(Euler((0, 0, rot))); st.location = Vector((cx, cy, 0)) + off; st.rotation_euler = (0, 0, rot); st.data.materials.append(seat)
        n = int(length / 0.62)
        for k in range(n):
            if random.random() < 0.12: continue
            p = Vector((-length / 2 + k * 0.62 + random.uniform(-0.1, 0.1), -(4 + r * 0.85), 0.6 + r * 0.5 + 0.25 + 0.55 + random.uniform(-0.05, 0.08)))
            p.rotate(Euler((0, 0, rot))); inst = bpy.data.objects.new('f', fan.data); inst.location = Vector((cx, cy, 0)) + p; inst.rotation_euler = (0, 0, rot); coll.objects.link(inst)
# stands behind the goal and along the near/far touchlines around the box
stand(GX + 4, 0, math.pi / 2, 64); stand(30, 34 + 2, 0, 60); stand(30, -34 - 2, math.pi, 60)
print('CROWD', len(coll.objects))
# LED boards
led = mat('led', (0.02, 0.1, 0.05), 0.4, (0.1, 0.9, 0.35), 2.5)
for (x, y, rot, L) in [(GX + 3.2, 0, math.pi / 2, 60), (30, 35.5, 0, 50), (30, -35.5, 0, 50)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.45)); o = bpy.context.object; o.scale = (L, 0.12, 0.9); o.rotation_euler = (0, 0, rot); o.data.materials.append(led)
# ---------- lights / world ----------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1); bg.inputs[1].default_value = 1.0
def area(loc, tgt, energy, size, col=(1, 0.97, 0.92)):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = energy; l.size = size; l.color = col; o = bpy.data.objects.new('a', l); o.location = loc
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); sc.collection.objects.link(o)
for loc in [(10, -45, 32), (60, -45, 32), (10, 45, 32), (60, 45, 32)]: area(loc, (44, 0, 0), 120000, 14)
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 1.2; sun.angle = 0.2; so = bpy.data.objects.new('sun', sun); so.rotation_euler = (0.9, 0.1, 2.2); sc.collection.objects.link(so)
lamp = mat('lamp', (1, 1, 1), 0.2, (1, 0.97, 0.9), 60)
for (x, y) in [(10, -45), (60, -45), (10, 45), (60, 45)]:
    for i in range(10):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x - 6 + (i % 5) * 3, y, 30 + (i // 5) * 1.6)); o = bpy.context.object; o.scale = (2.2, 0.3, 1.2); o.data.materials.append(lamp)
# ---------- players ----------
rig = bpy.data.objects['Human.rig']; grim_objs = [o for o in bpy.data.objects if o.name.startswith('Human')]
with bpy.data.libraries.load(os.path.join(HERE, 'keeper.blend')) as (src, dst): dst.objects = [n for n in src.objects if n.startswith('Human')]
for o in dst.objects: sc.collection.objects.link(o)
krig = next(o for o in dst.objects if o.type == 'ARMATURE')
# Grimaldo kick (mirrored CMU 10_01 -> left foot), contact at frame K of the action
act = apply_bvh(rig, '/home/user/tools/cmu/data/010/10_01.bvh', 'kick', mirror=True)
rig.animation_data_create(); rig.animation_data.action = act
K_ACT = 113; SPOT = Vector((41.5, 0, 0.11))
sc.frame_set(K_ACT - 2); f0 = rig.matrix_world @ rig.pose.bones['LeftFoot'].tail
sc.frame_set(K_ACT); f1 = rig.matrix_world @ rig.pose.bones['LeftFoot'].tail
vel = (f1 - f0); vel.z = 0; ang = math.atan2(vel.y, vel.x)
rig.rotation_euler.z -= ang - math.radians(4)  # kick direction -> towards goal, slightly to the right corner
sc.frame_set(K_ACT); foot = rig.matrix_world @ rig.pose.bones['LeftFoot'].tail
rig.location += Vector((SPOT.x - 0.12 - foot.x, SPOT.y - 0.05 - foot.y, 0))
# timeline: scene frame T maps to action frame; shot starts 60 frames before contact
START = K_ACT - 62; K = 62 + 1  # scene frame of contact
act_offset = START - 1
for fc in act.fcurves:
    for kp in fc.keyframe_points: kp.co[0] -= act_offset; kp.handle_left[0] -= act_offset; kp.handle_right[0] -= act_offset
# keeper on the line, facing the taker; dives to his right (towards -y) after contact
krig.location = (GX - 0.3, 0.1, 0); krig.rotation_euler = (0, 0, math.pi / 2)
kb = krig.pose.bones
for pb in kb: pb.rotation_mode = 'XYZ'
def key_keeper(f, loc, rot, arms):
    krig.location = loc; krig.rotation_euler = rot; krig.keyframe_insert('location', frame=f); krig.keyframe_insert('rotation_euler', frame=f)
    for side, s in (('Left', 1), ('Right', -1)):
        b = kb[side + 'Arm']; b.rotation_euler = (0, 0, s * arms); b.keyframe_insert('rotation_euler', frame=f)
        b = kb[side + 'UpLeg']; b.rotation_euler = (0, 0, s * 0.15); b.keyframe_insert('rotation_euler', frame=f)
key_keeper(1, (GX - 0.3, 0.1, 0), (0, 0, math.pi / 2), 0.5)
key_keeper(K - 6, (GX - 0.3, -0.05, 0), (0, 0, math.pi / 2), 0.6)
key_keeper(K + 3, (GX - 0.35, -0.6, 0.15), (0, -0.35, math.pi / 2), 1.2)
key_keeper(K + 12, (GX - 0.4, -2.2, 0.55), (0, -1.15, math.pi / 2), 1.5)
key_keeper(K + 22, (GX - 0.4, -2.9, 0.05), (0, -1.5, math.pi / 2), 1.4)
# ---------- ball ----------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, segments=48, ring_count=24, location=SPOT); ball = bpy.context.object
bm = bpy.data.materials.new('ball'); bm.use_nodes = True; bnt = bm.node_tree; vor = bnt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 6
cr = bnt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.12; cr.color_ramp.elements[0].color = (0.05, 0.05, 0.06, 1); cr.color_ramp.elements[1].position = 0.14; cr.color_ramp.elements[1].color = (0.96, 0.96, 0.96, 1)
bnt.links.new(vor.outputs['Distance'], cr.inputs['Fac']); bnt.links.new(cr.outputs['Color'], bnt.nodes['Principled BSDF'].inputs['Base Color']); bnt.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.35
ball.data.materials.append(bm); bpy.ops.object.shade_smooth()
TGT = Vector((GX + 0.3, 3.05, 0.35))
ball.location = SPOT; ball.keyframe_insert('location', frame=K)
ball.location = SPOT.lerp(TGT, 0.5) + Vector((0, 0, 0.18)); ball.keyframe_insert('location', frame=K + 5)
ball.location = TGT; ball.keyframe_insert('location', frame=K + 10)
ball.location = Vector((GX + 1.6, 2.9, 0.4)); ball.keyframe_insert('location', frame=K + 14)
ball.location = Vector((GX + 1.3, 2.7, 0.11)); ball.keyframe_insert('location', frame=K + 24)
ball.rotation_euler = (0, 0, 0); ball.keyframe_insert('rotation_euler', frame=K); ball.rotation_euler = (12, 3, 0); ball.keyframe_insert('rotation_euler', frame=K + 14)
kbu = back.data.shape_keys.key_blocks['bulge']
for f, v in [(K + 10, 0), (K + 13, 1), (K + 18, 0.45), (K + 24, 0.7), (K + 34, 0.15)]: kbu.value = v; kbu.keyframe_insert('value', frame=f)
# ---------- camera ----------
cam = bpy.data.cameras.new('cam'); co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
cam.lens = 32; cam.dof.use_dof = True; cam.dof.aperture_fstop = 2.8
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); cam.dof.focus_object = tgt
tr = co.constraints.new('TRACK_TO'); tr.target = tgt; tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
def camkey(f, loc, look):
    co.location = loc; co.keyframe_insert('location', frame=f); tgt.location = look; tgt.keyframe_insert('location', frame=f)
camkey(1, (33.5, -5.5, 2.2), (44, -0.8, 1.0))
camkey(K - 10, (36.6, -2.6, 1.55), (43, -0.2, 0.9))
camkey(K + 2, (37.4, -2.0, 1.45), (47, 0.8, 0.8))
camkey(K + 14, (38.2, -0.9, 1.4), (GX, 2.6, 0.6))
camkey(K + 34, (39.0, 0.2, 1.5), (GX, 2.4, 0.8))
for o in (co, tgt):
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'; kp.easing = 'EASE_IN_OUT'
# ---------- render settings ----------
sc.frame_start, sc.frame_end = 1, K + 36
if FR: a, bb = FR.split('-'); sc.frame_start, sc.frame_end = int(a), int(bb)
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 20)); sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
sc.render.use_motion_blur = bool(int(os.environ.get('MB', 0))); sc.render.motion_blur_shutter = 0.4
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = int(os.environ.get('RES', 66))
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = OUT
print('K', K, 'frames', sc.frame_start, sc.frame_end)
if os.environ.get('STILLS'):
    for f in [int(x) for x in os.environ['STILLS'].split(',')]:
        sc.frame_set(f); sc.render.filepath = f'{OUT}{f:04d}.png'; bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
