# YOU'RE THE REF ep.1 (3D test): 2026 UCL final, extra time, Nuno Mendes challenge from behind on Noni Madueke in the box.
# Referee Daniel Siebert waved play on, VAR checked and cleared (ESPN, SI, TNT, GiveMeSport). Our own 3D reconstruction (Mixamo X Bot
# mannequins via three.js examples), positions illustrative. Usage: blender-python scene.py <cam: ref|low> <out_dir> [frame_step]
import bpy, math, sys, os, random
from mathutils import Vector, Euler
CAM = sys.argv[-3] if len(sys.argv) > 3 else 'ref'; OUT = sys.argv[-2] if len(sys.argv) > 3 else '/tmp/r'; STEP = int(sys.argv[-1]) if len(sys.argv) > 3 else 1
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30; N = 180   # 6.0 s of play
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = N
def mat(name, rgb, rough=0.6, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = emit
    return m
def srgb(c): return tuple((v / 255) ** 2.2 for v in c)
# ------------------------------------------------------------------ pitch (x: towards goal at x=0, y: across). Goal line at x=0.
bpy.ops.mesh.primitive_plane_add(size=1, location=(-25, 0, 0)); pitch = bpy.context.object; pitch.scale = (80, 90, 1)
pm = bpy.data.materials.new('pitch'); pm.use_nodes = True; nt = pm.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.85
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mth = nt.nodes.new('ShaderNodeMath'); mth.operation = 'SINE'
mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = math.pi / 5.5
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
ramp.color_ramp.elements[0].color = (*srgb((56, 122, 52)), 1); ramp.color_ramp.elements[1].position = 0.5; ramp.color_ramp.elements[1].color = (*srgb((66, 140, 60)), 1)
noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 900; mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['Factor'].default_value = 0.08
nt.links.new(tc.outputs['Object'], sep.inputs[0]); nt.links.new(sep.outputs['X'], mul.inputs[0]); nt.links.new(mul.outputs[0], mth.inputs[0])
mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -1; nt.links.new(mth.outputs[0], mr.inputs['Value']); nt.links.new(mr.outputs[0], ramp.inputs[0])
nt.links.new(ramp.outputs[0], mix.inputs[6]); nt.links.new(noi.outputs['Color'], mix.inputs[7]); nt.links.new(mix.outputs[2], b.inputs['Base Color'])
pitch.data.materials.append(pm)
# object coords of the scaled plane span -0.5..0.5 -> stripe frequency set via SINE(x*k): fix by applying scale
bpy.ops.object.transform_apply(scale=True)
LW = mat('line', (0.92, 0.94, 0.92), 0.5)
def line(x0, y0, x1, y1, w=0.12):
    L = math.hypot(x1 - x0, y1 - y0); bpy.ops.mesh.primitive_plane_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, 0.006))
    o = bpy.context.object; o.scale = (L if L else w, w, 1); o.rotation_euler[2] = math.atan2(y1 - y0, x1 - x0); o.data.materials.append(LW)
line(0, -40, 0, 40); line(0, -20.16, -16.5, -20.16); line(0, 20.16, -16.5, 20.16); line(-16.5, -20.16, -16.5, 20.16)
line(0, -9.16, -5.5, -9.16); line(0, 9.16, -5.5, 9.16); line(-5.5, -9.16, -5.5, 9.16)
pts = [(-11 - 9.15 * math.cos(a), 9.15 * math.sin(a)) for a in [(-0.93 + 1.86 * k / 24) for k in range(25)]]
for a, c in zip(pts, pts[1:]):
    if a[0] < -16.5 or c[0] < -16.5: line(a[0], a[1], c[0], c[1])
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.01, location=(-11, 0, 0.006)); bpy.context.object.data.materials.append(LW)
# goal
WH = mat('post', (0.95, 0.95, 0.95), 0.3)
for y in (-3.66, 3.66):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.44, location=(0, y, 1.22)); bpy.context.object.data.materials.append(WH)
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=7.44, location=(0, 0, 2.44), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(WH)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=14, size=1, location=(1.0, 0, 1.2), rotation=(0, math.pi / 2 - 0.35, 0))
net = bpy.context.object; net.scale = (2.5, 7.3, 1); m = bpy.data.objects[net.name].modifiers.new('w', 'WIREFRAME'); m.thickness = 0.015; net.data.materials.append(WH)
# stadium: stands as big tilted planes with a crowd-like noise, ad boards, floodlight glow
crowd = bpy.data.materials.new('crowd'); crowd.use_nodes = True; cn = crowd.node_tree; cb = cn.nodes['Principled BSDF']
vor = cn.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 1400; cr = cn.nodes.new('ShaderNodeValToRGB')
E = cr.color_ramp.elements; E[0].color = (0.003, 0.003, 0.006, 1); E[1].position = 1.0; E[1].color = (0.55, 0.52, 0.5, 1)
for pos, col in ((0.62, (0.006, 0.006, 0.01, 1)), (0.72, (0.30, 0.03, 0.04, 1)), (0.8, (0.06, 0.06, 0.12, 1))): e = E.new(pos); e.color = col
cn.links.new(vor.outputs['Color'], cr.inputs[0]); cn.links.new(cr.outputs[0], cb.inputs['Base Color'])
cb.inputs['Roughness'].default_value = 1; cb.inputs['Emission Strength'].default_value = 0.25; cn.links.new(cr.outputs[0], cb.inputs['Emission Color'])
def stand(loc, rot, sx, sy):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = (sx, sy, 1); o.data.materials.append(crowd)
stand((9, 0, 9), (0, math.radians(-55), 0), 16, 120); stand((-25, 47, 9), (math.radians(55), 0, 0), 120, 16); stand((-25, -47, 9), (math.radians(-55), 0, 0), 120, 16)
stand((-75, 0, 9), (0, math.radians(55), 0), 16, 120)
ADS = mat('ads', srgb((20, 60, 150)), 0.4, 2.5)
for (lx, ly, rz, ln) in [(4.5, 0, math.pi / 2, 90), (-25, 41, 0, 110), (-25, -41, 0, 110)]:
    bpy.ops.mesh.primitive_plane_add(size=1, location=(lx, ly, 0.45), rotation=(math.pi / 2, 0, rz)); o = bpy.context.object; o.scale = (ln, 0.9, 1); o.data.materials.append(ADS)
FL = mat('flood', (1, 0.97, 0.9), 0.2, 30)
for (lx, ly, rz, ln) in [(16, 0, math.pi / 2, 70), (-25, 55, 0, 90), (-25, -55, 0, 90)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(lx, ly, 22), rotation=(0, 0, rz)); o = bpy.context.object; o.scale = (ln, 0.6, 0.6); o.data.materials.append(FL)
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; world.node_tree.nodes['Background'].inputs[0].default_value = (0.01, 0.012, 0.02, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0
for (lx, ly) in [(10, 45), (10, -45), (-60, 45), (-60, -45)]:
    bpy.ops.object.light_add(type='AREA', location=(lx, ly, 40)); L = bpy.context.object; L.data.energy = 14000; L.data.size = 14
    L.rotation_euler = (Vector((-20, 0, 0)) - Vector((lx, ly, 40))).to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.light_add(type='SUN', location=(0, 0, 30)); s = bpy.context.object; s.data.energy = 2.0; s.rotation_euler = (math.radians(35), 0, math.radians(30))
# ------------------------------------------------------------------ players
ARS = srgb((210, 20, 30)); PSG = srgb((18, 28, 70)); GK = srgb((230, 200, 30)); SKIN = srgb((60, 45, 40))
def player(name, kit, keys, anim='run', fall=None):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, 'assets/Xbot.glb'))
    new = [o for o in bpy.data.objects if o not in before]; arm = [o for o in new if o.type == 'ARMATURE'][0]
    for o in new:
        if o.type == 'MESH' and o.name.startswith('Icosphere'): bpy.data.objects.remove(o, do_unlink=True)
    for o in [o for o in bpy.data.objects if o.parent == arm and o.type == 'MESH']:
        o.data.materials.clear(); o.data.materials.append(mat(name + o.name, kit if 'Surface' in o.name else (0.9, 0.9, 0.9) if kit == PSG else (0.95, 0.95, 0.95), 0.55))
    arm.name = name; arm.scale = (0.01 * 1.0, 0.01, 0.01) if arm.dimensions.z > 50 else arm.scale
    act = bpy.data.actions.get(anim) or [a for a in bpy.data.actions if a.name.startswith(anim)][0]
    arm.animation_data_create(); tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new(anim, 1, act)
    try: st.action_slot = act.slots[0]
    except Exception as e: print('slot', e)
    st.repeat = 30; st.scale = 1.0; arm.animation_data.action = None
    arm.rotation_mode = 'XYZ'
    # path keys: (frame, x, y)
    for i, (f, x, y) in enumerate(keys):
        arm.location = (x, y, 0); arm.keyframe_insert('location', frame=f)
        nx, ny = (keys[i + 1][1:] if i + 1 < len(keys) else (x + (x - keys[i - 1][1]), y + (y - keys[i - 1][2])))
        arm.rotation_euler = (0, 0, math.atan2(ny - y, nx - x) + math.pi / 2); arm.keyframe_insert('rotation_euler', frame=f)
    if fall:  # (frame_start, frame_end): pitch forward onto the turf
        f0, f1 = fall; sc.frame_set(f0); r = list(arm.rotation_euler); r[2] = arm.rotation_euler[2]
        for fc in [fc for fc in (arm.animation_data.action.fcurves if arm.animation_data.action and hasattr(arm.animation_data.action, 'fcurves') else [])]: pass
        arm.keyframe_delete('rotation_euler', frame=keys[-1][0]); arm.rotation_euler = r; arm.keyframe_insert('rotation_euler', frame=f0)
        arm.rotation_euler = (r[0] + math.radians(80), r[1], r[2]); arm.keyframe_insert('rotation_euler', frame=f1)
        z = arm.location.copy(); arm.location = (z.x, z.y, 0.15); arm.keyframe_insert('location', frame=f1)
        st.action_frame_end = st.action_frame_start + (f1 - 1) * 0.8
    return arm
CONTACT = 112
MAD = player('MADUEKE', ARS, [(1, -24, -17), (60, -19.5, -13.0), (100, -16.2, -10.4), (CONTACT, -15.2, -9.7), (CONTACT + 16, -14.5, -9.25)], fall=(CONTACT, CONTACT + 16))
MEN = player('MENDES', PSG, [(1, -26.8, -16.0), (60, -21.4, -13.4), (100, -17.2, -11.0), (CONTACT, -15.8, -10.1), (150, -14.4, -9.4)])
player('D2', PSG, [(1, -14, -2), (CONTACT, -12.6, -4.6), (180, -12.0, -5.5)]); player('D3', PSG, [(1, -13, 6), (CONTACT, -11.5, 2.0), (180, -11.0, 1.0)])
player('A2', ARS, [(1, -20, 4), (CONTACT, -14.0, 1.5), (180, -12.5, 0.5)]); player('GKP', GK, [(1, -2.5, 0), (CONTACT, -3.4, -2.2), (180, -3.0, -2.0)], anim='idle')
# ball: at Madueke's feet until contact, then rolls on
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(0, 0, 0.11)); ball = bpy.context.object; ball.data.materials.append(mat('ball', (0.95, 0.95, 0.95), 0.3))
for f in range(1, N + 1, 3):
    if f <= CONTACT:
        bpy.context.scene.frame_set(f + 3); q = MAD.matrix_world.translation.copy(); bpy.context.scene.frame_set(f); p = MAD.matrix_world.translation.copy()
        d = (q - p); d.z = 0; d = (d.normalized() if d.length > 1e-4 else Vector((1, 0.6, 0)).normalized()) * (0.75 + 0.25 * math.sin(f * 0.35))
        ball.location = (p.x + d.x, p.y + d.y, 0.11)
    else:
        u = (f - CONTACT) / (N - CONTACT); ball.location = (-14.4 + 3.0 * u, -9.1 + 2.0 * u, 0.11)
    ball.keyframe_insert('location', frame=f)
# ------------------------------------------------------------------ camera
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
if CAM == 'ref':  # referee eye-line, jogging behind and to the side of the play, slight bob
    cam.data.lens = 42
    for f in range(1, N + 1, 2):
        u = f / N; bx = -27 + 7 * u; by = -3.5 - 2.5 * u
        cam.location = (bx, by, 1.72 + 0.03 * math.sin(f * 0.9)); cam.keyframe_insert('location', frame=f)
        sc.frame_set(f); tgt = (MAD.matrix_world.translation + MEN.matrix_world.translation) / 2 + Vector((0, 0, 0.9))
        cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=f)
else:  # low replay angle from the goal line side
    cam.data.lens = 45
    for f in range(1, N + 1, 2):
        cam.location = (-6, -19, 1.1); sc.frame_set(f); tgt = (MAD.matrix_world.translation + MEN.matrix_world.translation) / 2 + Vector((0, 0, 0.7))
        cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=f)
# ------------------------------------------------------------------ render
r = sc.render; r.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SPP', '16')); sc.cycles.use_denoising = True
r.resolution_x, r.resolution_y, r.resolution_percentage = 1080, 1920, int(os.environ.get('PCT', '100')); r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 92
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.use_motion_blur = True
os.makedirs(OUT, exist_ok=True)
import json
from bpy_extras.object_utils import world_to_camera_view
pos = {}
for f in range(1, N + 1):
    sc.frame_set(f); pos[f] = {}
    for nm, o in (('MADUEKE', MAD), ('MENDES', MEN)):
        v = world_to_camera_view(sc, cam, o.matrix_world.translation + Vector((0, 0, 2.05))); pos[f][nm] = (v.x, 1 - v.y, v.z)
json.dump(pos, open(os.path.join(OUT, 'pos.json'), 'w'))
for f in range(1, N + 1, STEP):
    sc.frame_set(f); r.filepath = os.path.join(OUT, f'f_{f:04d}.jpg'); bpy.ops.render.render(write_still=True)
