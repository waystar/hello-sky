bl_info = {
    "name": "Export CSV",
    "author": "Waylena McCully",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "",
    "description": "Exports location and rotation keyframes of selected object to CSV for use in Digistar scripts.",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}


import bpy
from math import degrees
# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


# need to figure out how to use this as an add-on 

#setup to use camera called FisheyeCamera


def write_to_csv(context, filepath, use_some_setting):
    print("running write_to_csv...")

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['FisheyeCamera'].select_set(True)
    camera = context.active_object
    scene = context.scene
    frame = scene.frame_start
    
    fps = scene.render.fps

    f = open(filepath, 'w', encoding='utf-8')
    # header for Digistar
    f.write("D3, D3Path")
    f.write("\n")
    f.write("XYZHPR, 0x3f, (BITMASK)")
    f.write("\n")
    f.write("Segments, SMOOTH, (SMOOTH or STRAIGHT)")
    f.write("\n")
    f.write(" , Time, X, Y, Z, H, P, R")
    f.write("\n")
    # get locations and rotations (convert rot to degrees)
    while frame <= scene.frame_end:
        scene.frame_set(frame)
        timesec = (frame - 1) / fps        
        x, y, z = camera.location
        rxR, ryR, rzR = camera.rotation_euler
        rx = degrees(rxR)
        ry = degrees(ryR)
        rz = degrees(rzR)  
        f.write("Node Data")
        f.write(", ")
        f.write("%10.4f" % timesec)
        f.write(", ")
        f.write("%5.4f, %5.4f, %5.4f" % (x, y, z))
        f.write(", ")
        f.write("%5.4f, %5.4f, %5.4f" % (rz, rx, ry))
        f.write("\n")
        frame += 1
    f.close()

    return {'FINISHED'}



class ExportCSV(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_csv.data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export CSV"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )



    def execute(self, context):
        return write_to_csv(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportCSV.bl_idname, text="Export Camera to CSV (Digistar)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportCSV)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportCSV)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_csv.data('INVOKE_DEFAULT')
