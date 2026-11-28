import bpy, sys, os
sys.path.insert(0, os.path.dirname(bpy.data.filepath))
from mocap import apply_bvh
sc = bpy.context.scene; sc.render.fps = 24
rig = bpy.data.objects['Human.rig']
mir = os.environ.get('MIRROR') == '1'
act = apply_bvh(rig, '/home/user/tools/cmu/data/010/10_01.bvh', 'kick', mirror=mir)
rig.animation_data_create(); rig.animation_data.action = act
prev = None; best = (0, 0)
for f in range(6, int(act.frame_range[1])):
    sc.frame_set(f)
    lf = rig.matrix_world @ rig.pose.bones['LeftFoot'].tail; rf = rig.matrix_world @ rig.pose.bones['RightFoot'].tail
    if prev:
        vl = (lf - prev[0]).length; vr = (rf - prev[1]).length
        if max(vl, vr) > best[1]: best = (f, max(vl, vr), 'L' if vl > vr else 'R', tuple(round(x, 2) for x in (lf if vl > vr else rf)))
    prev = (lf.copy(), rf.copy())
print('CONTACT', mir, best)
