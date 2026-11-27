import sys, math
sys.argv = ['x', 'ref', '/tmp/none', '9999']
import bpy
src = open('scene.py').read().split('# ------------------------------------------------------------------ render')[0]
exec(compile(src, 'scene', 'exec'))
r = sc.render; r.engine = 'CYCLES'; sc.cycles.samples = 4; r.resolution_x, r.resolution_y, r.resolution_percentage = 1080, 1920, 30
for f in (112, 124, 140):
    sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); m = MAD.evaluated_get(dg)
    print(f, [round(math.degrees(v)) for v in m.matrix_world.to_euler()], [o.name for o in MAD.children][:3])
    r.filepath = f'/home/user/Filmler/ref2/test/p_{f}.jpg'; bpy.ops.render.render(write_still=True)
