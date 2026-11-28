# Build a realistic footballer with MPFB2 (MakeHuman, CC0 assets) in Blender, recolour clothes into a kit, rig cmu_mb, save .blend.
# Run: blender -b -P build_player.py -- out.blend '<json spec>'
import bpy, sys, json, os, math
from bl_ext.user_default.mpfb.services.humanservice import HumanService
D = '/root/.config/blender/4.2/extensions/.user/user_default/mpfb/data'
argv = sys.argv[sys.argv.index('--') + 1:]
out, spec = argv[0], json.loads(argv[1])
bpy.ops.wm.read_factory_settings(use_empty=True)
info = HumanService._create_default_human_info_dict()
info['phenotype'].update({'gender': 1.0, 'age': spec.get('age', 0.55), 'muscle': spec.get('muscle', 0.78), 'weight': spec.get('weight', 0.42),
                          'height': spec.get('height', 0.55), 'proportions': 0.8, 'race': spec.get('race', {'caucasian': 0.9, 'african': 0.05, 'asian': 0.05})})
info['skin_mhmat'] = f"{D}/skins/{spec.get('skin', 'young_caucasian_male')}/{spec.get('skin', 'young_caucasian_male')}.mhmat"
info['skin_material_type'] = spec.get('skin_type', 'ENHANCED')
info['eyes'] = f'{D}/eyes/high-poly/high-poly.mhclo'; eb = spec.get('eyebrows', 'eyebrow001'); info['eyebrows'] = f'{D}/eyebrows/{eb}/{eb}.mhclo'; info['eyelashes'] = f'{D}/eyelashes/eyelashes01/eyelashes01.mhclo'
info['hair'] = f"{D}/hair/{spec.get('hair', 'short02')}/{spec.get('hair', 'short02')}.mhclo"
info['eyes_material_settings'] = {}
info['rig'] = 'cmu_mb'
info['clothes'] = [f"{D}/clothes/{c}/{c}.mhclo" for c in ['elvs_crude_t-shirt_male', 'cortu_jeans_shorts', 'shoes05']]
st = HumanService.get_default_deserialization_settings(); st['subdiv_levels'] = 1
basemesh = HumanService.deserialize_from_dict(info, st)
print('HUMAN', basemesh.name)
# kit colours: shirt / shorts / boots
kit = spec.get('kit', {'shirt': [0.02, 0.02, 0.025], 'trim': [0.95, 0.75, 0.0], 'shorts': [0.02, 0.02, 0.025]})
def recolor(obj, rgb, rough=0.6):
    for slot in obj.material_slots:
        m = slot.material
        if not m or not m.use_nodes: continue
        nt = m.node_tree; bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf: continue
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = 1.0
        src = bsdf.inputs['Base Color'].links[0].from_socket if bsdf.inputs['Base Color'].is_linked else None
        # replace base colour with flat kit colour, keep a little of the fabric texture as detail
        rgbn = nt.nodes.new('ShaderNodeRGB'); rgbn.outputs[0].default_value = (*rgb, 1)
        if src:
            hsv = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(src, hsv.inputs[0])
            ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.0; ramp.inputs['From Max'].default_value = 1.0; ramp.inputs['To Min'].default_value = 0.75; ramp.inputs['To Max'].default_value = 1.15
            nt.links.new(hsv.outputs[0], ramp.inputs['Value'])
            nt.links.new(rgbn.outputs[0], mix.inputs['A']); nt.links.new(ramp.outputs[0], mix.inputs['B'])
            nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
        else: nt.links.new(rgbn.outputs[0], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = rough
        if 'Sheen Weight' in bsdf.inputs: bsdf.inputs['Sheen Weight'].default_value = 0.1
for o in bpy.data.objects:
    n = o.name.lower()
    if 't-shirt' in n or 'shirt' in n: recolor(o, kit['shirt'])
    elif 'shorts' in n: recolor(o, kit['shorts'])
    elif 'shoes' in n: recolor(o, kit.get('boots', [0.9, 0.9, 0.92]), 0.35)
print('OBJECTS', [o.name for o in bpy.data.objects])
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print('SAVED', out)
