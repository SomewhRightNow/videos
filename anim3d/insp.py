import bpy
for o in bpy.data.objects:
    for s in o.material_slots:
        m=s.material
        if m and m.use_nodes: print(o.name, m.name, [n.type+':'+n.name for n in m.node_tree.nodes][:12])
