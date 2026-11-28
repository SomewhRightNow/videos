import bpy
for o in bpy.data.objects:
    if 'short04' in o.name or o.name=='Human':
        for s in o.material_slots:
            m=s.material; print(o.name, m.name, [ (n.type, n.name) for n in m.node_tree.nodes][:14])
