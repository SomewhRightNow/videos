# Apply a CMU BVH motion to an MPFB cmu_mb rig (same bone names): copy edit-bone rolls, then copy the whole action.
import bpy, os
def apply_bvh(rig, bvh, name, mirror=False, frame_start=1, use_fps_scale=True):
    before = set(bpy.data.objects)
    bpy.ops.import_anim.bvh(filepath=bvh, axis_forward='Y', axis_up='Z', rotate_mode='XYZ', global_scale=1.0,
                            use_fps_scale=use_fps_scale, update_scene_fps=False, update_scene_duration=False, frame_start=frame_start)
    src = [o for o in bpy.data.objects if o not in before][0]
    # scale: match hip heights
    bpy.context.view_layer.objects.active = src; bpy.ops.object.mode_set(mode='EDIT')
    rolls = {b.name: b.roll for b in src.data.edit_bones}; eb = src.data.edit_bones; src_leg = eb['LeftUpLeg'].length + eb['LeftLeg'].length
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode='EDIT')
    for b in rig.data.edit_bones:
        if b.name in rolls: b.roll = rolls[b.name]
    eb = rig.data.edit_bones; dst_leg = eb['LeftUpLeg'].length + eb['LeftLeg'].length
    bpy.ops.object.mode_set(mode='OBJECT')
    act = src.animation_data.action.copy(); act.name = name
    k = dst_leg / max(1e-6, src_leg)
    for fc in act.fcurves:
        if fc.data_path.endswith('location'):
            if 'Hips' not in fc.data_path:
                act.fcurves.remove(fc) if False else None
            v0 = fc.evaluate(fc.range()[0]) if 'Hips' in fc.data_path else 0
            for kp in fc.keyframe_points:
                for arr in (kp.co, kp.handle_left, kp.handle_right): arr[1] = (arr[1] - v0) * k
    for pb in rig.pose.bones: pb.rotation_mode = 'XYZ'
    bpy.data.objects.remove(src, do_unlink=True)
    if mirror:
        # swap Left/Right channels and flip the lateral axis (CMU rig: x lateral in bone space for most bones)
        import re
        for fc in act.fcurves:
            m = re.match(r'pose\.bones\["(.+?)"\]\.(\w+)', fc.data_path)
            if not m: continue
            bn, prop = m.groups()
            if bn.startswith('Left'): nb = 'Right' + bn[4:]
            elif bn.startswith('Right'): nb = 'Left' + bn[5:]
            elif bn.startswith('LHip'): nb = 'RHip' + bn[4:]
            elif bn.startswith('RHip'): nb = 'LHip' + bn[4:]
            elif bn.startswith('LThumb'): nb = 'RThumb'
            elif bn.startswith('RThumb'): nb = 'LThumb'
            else: nb = bn
            fc.data_path = f'pose.bones["{nb}"].{prop}'
        for fc in act.fcurves:
            # mirror across the body's sagittal plane: negate y and z euler components, negate x location
            if fc.data_path.endswith('rotation_euler') and fc.array_index in (1, 2): sgn = -1
            elif fc.data_path.endswith('location') and fc.array_index == 0: sgn = -1
            else: continue
            for kp in fc.keyframe_points: kp.co[1] *= sgn; kp.handle_left[1] *= sgn; kp.handle_right[1] *= sgn
    return act
