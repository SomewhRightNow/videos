import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='assets/Xbot.glb')
for o in bpy.data.objects: print(o.name, o.type, [m.name for m in getattr(o.data,'materials',[]) or []] if o.type=='MESH' else '', o.dimensions[:])
print('actions', [(a.name, a.frame_range[:]) for a in bpy.data.actions])
print('engines', [e for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys()])
