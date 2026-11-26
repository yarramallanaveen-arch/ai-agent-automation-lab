
import bpy
import math
from mathutils import Vector

# ==========================================
# AI AGENT AUTOMATION LAB
# Project: Blender Scene Generator
# Version: 1.0
# ==========================================

# 1. RESET BLENDER SCENE
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 2. CREATE MATERIALS
def create_material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

    return mat


cube_material = create_material(
    "Robot Blue",
    (0.02, 0.3, 0.9),
    0.4,
    0.25
)

floor_material = create_material(
    "Dark Floor",
    (0.025, 0.025, 0.04),
    0.1,
    0.7
)

# 3. CREATE FLOOR
bpy.ops.mesh.primitive_plane_add(
    size=20,
    location=(0, 0, -1)
)

floor = bpy.context.object
floor.name = "Ground"
floor.data.materials.append(floor_material)

# 4. CREATE ANIMATED CUBE
bpy.ops.mesh.primitive_cube_add(
    size=2,
    location=(0, 0, 1)
)

cube = bpy.context.object
cube.name = "AI_Animated_Cube"
cube.data.materials.append(cube_material)

# Smooth edges
bevel = cube.modifiers.new("Rounded Edges", "BEVEL")
bevel.width = 0.15
bevel.segments = 4

cube.modifiers.new("Weighted Normals", "WEIGHTED_NORMAL")

# 5. ANIMATION
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 24

cube.rotation_mode = 'XYZ'

# Starting position
cube.location = (0, 0, 1)
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=1)
cube.keyframe_insert(data_path="rotation_euler", frame=1)

# Middle animation
cube.location = (0, 0, 3)
cube.rotation_euler = (
    math.radians(180),
    0,
    math.radians(180)
)
cube.keyframe_insert(data_path="location", frame=60)
cube.keyframe_insert(data_path="rotation_euler", frame=60)

# Ending animation
cube.location = (0, 0, 1)
cube.rotation_euler = (
    math.radians(360),
    0,
    math.radians(360)
)
cube.keyframe_insert(data_path="location", frame=120)
cube.keyframe_insert(data_path="rotation_euler", frame=120)

# 6. CREATE CAMERA
bpy.ops.object.camera_add(
    location=(8, -12, 7)
)

camera = bpy.context.object
camera.name = "AI_Camera"

direction = Vector((0, 0, 1)) - camera.location
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

camera.data.lens = 50
scene.camera = camera

# 7. CREATE LIGHTING
bpy.ops.object.light_add(
    type='AREA',
    location=(2, -4, 7)
)

light = bpy.context.object
light.name = "Main_Light"
light.data.energy = 1500
light.data.shape = 'DISK'
light.data.size = 6

# 8. WORLD BACKGROUND
world = scene.world
world.color = (0.015, 0.015, 0.03)

# 9. RENDER SETTINGS
scene.render.engine = 'BLENDER_EEVEE_NEXT'

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = 'PNG'

# 10. SET ANIMATION PREVIEW
scene.frame_set(1)

# 11. SAVE BLENDER PROJECT
output_path = bpy.path.abspath("//ai_agent_scene.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("================================")
print("AI AGENT AUTOMATION LAB")
print("Scene generated successfully!")
print("Animation: 120 frames")
print("Duration: 5 seconds")
print("================================")
