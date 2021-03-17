import math
import pathlib
import bpy


def constrain_with_copy_transforms(*, control_rig: bpy.types.Armature, game_rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for bone in game_rig.pose.bones:
        bone.location = (0, 0, 0)
        bone.scale = (1, 1, 1)
        bone.rotation_quaternion = (1, 0, 0, 0)
        bone.rotation_mode = "QUATERNION"

        constraint = bone.constraints.new(type="COPY_TRANSFORMS")
        constraint.target = control_rig
        constraint.subtarget = bone.name


def copy_rig(rig: bpy.types.Armature) -> bpy.types.Armature:
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    game_rig = rig.copy()
    game_rig.data = rig.data.copy()
    return game_rig


def disable_stretch_to_constraints_for_spine(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for bone in rig.pose.bones:
        if "spine" in bone.name:
            for constraint in bone.constraints:
                if constraint.type == "STRETCH_TO":
                    constraint.mute = True


def disable_use_deform(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    for bone in rig.data.edit_bones:
        bone.use_deform = False


def enable_all_rig_layers(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for layerNo in range(0, 32):
        rig.data.layers[layerNo] = True


def fix_bone_hierarchy(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    # MakeHuman
    rig.data.edit_bones["DEF-thigh.L"].parent = rig.data.edit_bones["DEF-spine"]
    rig.data.edit_bones["DEF-thigh.R"].parent = rig.data.edit_bones["DEF-spine"]
    rig.data.edit_bones["DEF-pelvis.L"].parent = rig.data.edit_bones["DEF-spine"]
    rig.data.edit_bones["DEF-pelvis.R"].parent = rig.data.edit_bones["DEF-spine"]
    rig.data.edit_bones["DEF-shoulder.L"].parent = rig.data.edit_bones["DEF-spine.005"]
    rig.data.edit_bones["DEF-shoulder.R"].parent = rig.data.edit_bones["DEF-spine.005"]
    rig.data.edit_bones["DEF-upper_arm.L"].parent = rig.data.edit_bones["DEF-deltoid.L"]
    rig.data.edit_bones["DEF-upper_arm.R"].parent = rig.data.edit_bones["DEF-deltoid.R"]
    rig.data.edit_bones["DEF-breast.L"].parent = rig.data.edit_bones["DEF-spine.003"]
    rig.data.edit_bones["DEF-breast.R"].parent = rig.data.edit_bones["DEF-spine.003"]
    # Rigify
    # Everything under 'face' should be parented to the neck keeping offset


def remove_animation_data(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    rig.animation_data_clear()
    rig.data.animation_data_clear()


def remove_bendy_bone_segments(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    for bone in rig.data.edit_bones:
        bone.bbone_segments = 1


def remove_bone_constraints(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for bone in rig.pose.bones:
        for constraint in bone.constraints:
            bone.constraints.remove(constraint)


def remove_drivers(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for driver in rig.animation_data.drivers:
        rig.animation_data.drivers.remove(driver)
    for driver in rig.data.animation_data.drivers:
        rig.data.animation_data.drivers.remove(driver)


def remove_nondeforming_bones(rig: bpy.types.Armature, include=["root"]):
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    for bone in rig.data.edit_bones:
        if bone.use_deform or any(sub in bone.name for sub in include):
            bone.layers[0] = True
            for layerNo in range(1, 32):
                bone.layers[layerNo] = False
        else:
            rig.data.edit_bones.remove(bone)


def reparent_meshes(*, control_rig: bpy.types.Armature, game_rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for child in control_rig.children:
        if child.type == "MESH":
            child.parent = game_rig
            for modifier in [modifier for modifier in child.modifiers if modifier.type == "ARMATURE"]:
                child.modifiers.remove(modifier)
            child.modifiers.new(game_rig.name, game_rig.type)
            child.modifiers[game_rig.name].object = game_rig


def select_active(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    bpy.ops.object.select_all(action="DESELECT")
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig


def select_bones(rig: bpy.types.Armature):
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="DESELECT")
    for bone in rig.data.bones:
        bone.select = True


def set_ik_stretch_to_zero(rig: bpy.types.Armature):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for bone in rig.pose.bones:
        if "IK_Stretch" in bone:
            bone["IK_Stretch"] = 0.0


bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
if bpy.context.object.type == "ARMATURE":
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    for obj in bpy.context.scene.collection.all_objects:
        obj.hide_select = False
        obj.hide_set(False)

    bpy.ops.object.mode_set(mode="POSE", toggle=False)
    bpy.ops.pose.transforms_clear()

    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    control_rig: bpy.types.Armature = bpy.context.object

    game_rig = copy_rig(control_rig)
    bpy.context.collection.objects.link(game_rig)

    select_active(game_rig)
    enable_all_rig_layers(game_rig)
    remove_nondeforming_bones(game_rig)
    remove_drivers(game_rig)
    remove_animation_data(game_rig)
    remove_bone_constraints(game_rig)
    remove_bendy_bone_segments(game_rig)
    fix_bone_hierarchy(game_rig)

    select_active(control_rig)
    disable_use_deform(control_rig)
    enable_all_rig_layers(control_rig)
    remove_bendy_bone_segments(control_rig)
    set_ik_stretch_to_zero(control_rig)
    # TODO: does it mess up makehuman rigs?
    disable_stretch_to_constraints_for_spine(control_rig)

    select_active(game_rig)
    # TODO: To allow squash and stretch one can
    #   - clear all parents, use copy transform
    #   - disconnect all bones (keeping hierachy), use copy location and copy rotation
    constrain_with_copy_transforms(control_rig=control_rig, game_rig=game_rig)
    reparent_meshes(control_rig=control_rig, game_rig=game_rig)

    for nla in control_rig.animation_data.nla_tracks:
        nla: bpy.types.NlaTrack  # type: ignore
        nla.is_solo = False
        nla.mute = True

    for nla in control_rig.animation_data.nla_tracks:
        nla: bpy.types.NlaTrack  # type: ignore
        nla.is_solo = True

        frames = list()
        for strip in nla.strips:
            strip: bpy.types.NlaStrip  # type: ignore
            frames.append(strip.action_frame_start)
            frames.append(strip.action_frame_end)
        if frames:
            first_keyframe = int(min(frames))
            last_keyframe = math.ceil(max(frames))
            select_active(game_rig)
            select_bones(game_rig)
            bpy.ops.nla.bake(
                frame_start=first_keyframe,
                frame_end=last_keyframe,
                step=1,
                only_selected=True,
                visual_keying=True,
                clear_constraints=False,
                clear_parents=True,
                use_current_action=True,
                clean_curves=True,
                bake_types={"POSE"},
            )
            if game_rig.animation_data.action:
                nla_track = game_rig.animation_data.nla_tracks.new()
                nla_track.name = nla.name
                game_rig.animation_data.action.name = f"{nla.name}.baked"
                strip = nla_track.strips.new(
                    nla.name, game_rig.animation_data.action.frame_range[0], game_rig.animation_data.action
                )
                game_rig.animation_data.action = None

    for nla in control_rig.animation_data.nla_tracks:
        nla: bpy.types.NlaTrack  # type: ignore
        nla.is_solo = False
        nla.mute = True

    for nla in game_rig.animation_data.nla_tracks:
        nla: bpy.types.NlaTrack  # type: ignore
        nla.is_solo = False
        nla.mute = False

    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    for bone in game_rig.pose.bones:
        for constraint in bone.constraints:
            constraint: bpy.types.Constraint  # type: ignore
            if constraint.type == "COPY_TRANSFORMS":
                constraint.mute = True

    select_active(game_rig)
    bpy.ops.object.select_grouped(type="CHILDREN_RECURSIVE")
    game_rig.select_set(True)
    bpy.context.view_layer.objects.active = game_rig
    for obj in bpy.context.scene.collection.all_objects:
        if not obj in bpy.context.selected_objects:
            obj.hide_set(True)

    output = pathlib.Path(bpy.data.filepath).with_suffix(".fbx")
    bpy.ops.export_scene.fbx(
        add_leaf_bones=False,
        apply_scale_options="FBX_SCALE_ALL",
        apply_unit_scale=True,
        armature_nodetype="NULL",
        axis_forward="Z",
        axis_up="Y",
        bake_anim_force_startend_keying=False,
        bake_anim_simplify_factor=1.0,
        bake_anim_step=1.0,
        bake_anim_use_all_actions=False,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=True,
        bake_anim=True,
        bake_space_transform=True,
        batch_mode="OFF",
        check_existing=True,
        embed_textures=False,
        filepath=str(output),
        filter_glob="*.fbx",
        global_scale=1.0,
        mesh_smooth_type="OFF",
        object_types={"ARMATURE", "MESH"},
        path_mode="AUTO",
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        use_active_collection=False,
        use_armature_deform_only=True,
        use_batch_own_dir=False,
        use_custom_props=False,
        use_mesh_edges=False,
        use_mesh_modifiers_render=False,
        use_mesh_modifiers=False,
        use_metadata=True,
        use_selection=True,
        use_space_transform=True,
        use_subsurf=False,
        use_tspace=False,
    )
