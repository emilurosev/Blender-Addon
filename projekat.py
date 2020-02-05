bl_info = {
    "name": "Projekat addon",
    "blender": (2, 80, 0),
    "category": "Object"
}

import bpy
import os
import convertcloud as cvc

class Projekat(bpy.types.Operator):
    """Projekat"""
    bl_idname = 'projekat.addon'
    bl_label = 'Projekat'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        converter = cvc.Converter()

        path = input('Enter full path: ')
        if os.path.exists(path):
            if os.path.isdir(path):
                if not path.endswith('/'):
                    path += '/'    
                dirlist = os.listdir(path)
                for file in dirlist:
                    if file.endswith('.xyz'):
                        converter.load_points(path+file)
                        new_file = file[:-3]+'ply'
                        converter.convert(path+new_file)
                        print(file+' converted to '+new_file)
                        bpy.ops.import_mesh.ply(filepath=path+new_file)
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.object.select_all(action='DESELECT')
                    elif file.endswith('.ply'):
                        bpy.ops.import_mesh.ply(filepath=path+file)
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.object.select_all(action='DESELECT')
                    else:
                        print(file+' is not .xyz or .ply file')
                        continue
            else:
                if path.endswith('.xyz'):
                    print('xyz file selected')
                    with open(path, 'r') as f:
                        line = 1
                        for i in f:
                            if line % 100 is 0:
                                xyz = i.split()
                                bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(float(xyz[0]), float(xyz[1]), float(xyz[2])))
                                print('100th coordinate: '+xyz[0]+','+xyz[1]+','+xyz[2])
                            line += 1
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