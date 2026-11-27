import sys, runpy, math
sys.argv = ['x', 'ref', '/tmp/none', '9999']
import bpy
src = open('scene.py').read().split('# ------------------------------------------------------------------ render')[0]
exec(compile(src, 'scene', 'exec'))
for f in (100, 112, 120, 128, 140, 160):
    sc.frame_set(f); print(f, [round(math.degrees(v)) for v in MAD.rotation_euler], [round(v, 2) for v in MAD.location], MAD.matrix_world.to_euler()[:])
ad = MAD.animation_data; print('action', ad.action, [t.name for t in ad.nla_tracks])
