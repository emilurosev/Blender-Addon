bl_info = {
    "name": "Projekat addon",
    "blender": (2, 80, 0),
    "category": "Object"
}

import bpy
import os

class Projekat(bpy.types.Operator):
    """Projekat"""
    bl_idname = 'projekat.addon'
    bl_label = 'Projekat'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        path = input('Enter full path: ')
        if os.path.exists(path):
            if os.path.isdir(path):
                if not path.endswith('/'):
                    path += '/'    
                dirlist = os.listdir(path)
                for file in dirlist:
                    if file.endswith('.xyz'):
                        with open(path+file, 'r') as f:
                            for i in f:
                                xyz = i.split()
                                print(xyz[0]+','+xyz[1]+','+xyz[2])
                    elif file.endswith('.ply'):
                        bpy.ops.import_mesh.ply(filepath=path+file)
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.object.select_all(action='DESELECT')
                    else:
                        continue
            else:
                if path.endswith('.xyz'):
                    print('xyz file selected')
                    with open(path, 'r') as f:
                        for i in f:
                            xyz = i.split()
                            print(xyz[0]+','+xyz[1]+','+xyz[2])
                elif path.endswith('.ply'):
                    print('ply file selected')
                    bpy.ops.import_mesh.ply(filepath=path+file)
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.convex_hull()
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.object.select_all(action='DESELECT')
                else:
                    print('invalid file type')
        else:
            print('invalid path')
               
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(Projekat.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(Projekat)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(Projekat.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(Projekat)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()