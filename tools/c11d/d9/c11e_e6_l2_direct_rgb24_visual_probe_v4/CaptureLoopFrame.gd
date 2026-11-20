extends SceneTree

const SOURCE_SCENE_PATH := "res://tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.tscn"
const WIDTH := 720
const HEIGHT := 1280
const SEED := 100006
const GRAMMAR := "radial_bloom"

func _initialize() -> void:
    call_deferred("_capture_once")

func _fail(code: String) -> void:
    print("C11E_L2_CAPTURE=BLOCKED/" + code)
    quit(2)

func _capture_once() -> void:
    var output_root := OS.get_environment("C11E_L2_CAPTURE_ROOT").strip_edges()
    if output_root.is_empty():
        _fail("OUTPUT_ROOT_MISSING")
        return
    var scene_resource := load(SOURCE_SCENE_PATH) as PackedScene
    if scene_resource == null:
        _fail("SOURCE_SCENE_LOAD_FAILED")
        return
    # Use a render target with explicit pixel dimensions. Window dimensions are
    # affected by Windows DPI scaling and are not a valid pixel contract.
    var capture_viewport := SubViewport.new()
    capture_viewport.name = "C11E_L2_FixedCaptureViewport"
    capture_viewport.size = Vector2i(WIDTH, HEIGHT)
    capture_viewport.disable_3d = true
    capture_viewport.transparent_bg = false
    capture_viewport.render_target_clear_mode = SubViewport.CLEAR_MODE_ALWAYS
    capture_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    root.add_child(capture_viewport)
    var scene_instance := scene_resource.instantiate()
    if scene_instance == null:
        _fail("SOURCE_SCENE_INSTANTIATE_FAILED")
        return
    capture_viewport.add_child(scene_instance)
    # _ready() sets seed/grammar, initializes renderer and original frame zero.
    # Disable the source root process before the first post-draw readback.
    scene_instance.set_process(false)
    scene_instance.set_physics_process(false)
    var resolved_seed := int(scene_instance.get("_seed"))
    var variation: Dictionary = scene_instance.get("_variation")
    var resolved_grammar := str(variation.get("grammar_name", ""))
    if resolved_seed != SEED or resolved_grammar != GRAMMAR:
        _fail("SCENE_SELECTOR_IDENTITY_MISMATCH")
        return
    if scene_instance.get_viewport() != capture_viewport:
        _fail("SCENE_NOT_IN_FIXED_CAPTURE_SUBVIEWPORT")
        return
    await RenderingServer.frame_post_draw
    var viewport_size := capture_viewport.size
    if int(viewport_size.x) != WIDTH or int(viewport_size.y) != HEIGHT:
        _fail("SUBVIEWPORT_DIMENSIONS_MISMATCH:%sx%s" % [str(viewport_size.x), str(viewport_size.y)])
        return
    var image: Image = capture_viewport.get_texture().get_image()
    if image == null or image.is_empty():
        _fail("SUBVIEWPORT_IMAGE_EMPTY")
        return
    if image.get_width() != WIDTH or image.get_height() != HEIGHT:
        _fail("SUBVIEWPORT_IMAGE_DIMENSIONS_MISMATCH:%sx%s" % [str(image.get_width()), str(image.get_height())])
        return
    if image.get_format() != Image.FORMAT_RGBA8:
        _fail("IMAGE_FORMAT_NOT_RGBA8:%s" % str(image.get_format()))
        return
    var rgba := image.get_data()
    if rgba.size() != WIDTH * HEIGHT * 4:
        _fail("RGBA_BYTE_COUNT_MISMATCH")
        return
    var rgb := PackedByteArray()
    rgb.resize(WIDTH * HEIGHT * 3)
    var src := 0
    var dst := 0
    while src < rgba.size():
        if rgba[src + 3] != 255:
            _fail("NON_OPAQUE_ALPHA_FOUND")
            return
        rgb[dst] = rgba[src]
        rgb[dst + 1] = rgba[src + 1]
        rgb[dst + 2] = rgba[src + 2]
        src += 4
        dst += 3
    if rgb.size() != WIDTH * HEIGHT * 3:
        _fail("RGB24_BYTE_COUNT_MISMATCH")
        return
    var dir_error := DirAccess.make_dir_recursive_absolute(output_root)
    if dir_error != OK:
        _fail("OUTPUT_DIRECTORY_CREATE_FAILED:%s" % str(dir_error))
        return
    var rgb_path := output_root.path_join("source_frame.rgb24")
    var rgb_file := FileAccess.open(rgb_path, FileAccess.WRITE)
    if rgb_file == null:
        _fail("RGB24_OUTPUT_OPEN_FAILED")
        return
    rgb_file.store_buffer(rgb)
    rgb_file.flush()
    rgb_file.close()
    var png_path := output_root.path_join("source_frame.png")
    var png_error := image.save_png(png_path)
    if png_error != OK:
        _fail("SOURCE_PREVIEW_PNG_WRITE_FAILED:%s" % str(png_error))
        return
    var hash_context := HashingContext.new()
    var hash_error := hash_context.start(HashingContext.HASH_SHA256)
    if hash_error != OK:
        _fail("SHA256_INIT_FAILED")
        return
    hash_context.update(rgb)
    var rgb_sha256 := hash_context.finish().hex_encode()
    var metadata := {
        "schema": "C11E-E6-L2-DIRECT-RGB24-CAPTURE-V4",
        "status": "PASS_CAPTURED_ONE_DIRECT_RGB24_FRAME",
        "source_scene": SOURCE_SCENE_PATH,
        "source_origin": "C11C_SCENE_DIRECT_VIEWPORT_RECAPTURE_NOT_HISTORICAL_MP4_FRAME",
        "selector_id": "E6-L-01",
        "family_id": "fractal_bloom",
        "grammar_id": GRAMMAR,
        "gameplay_seed": SEED,
        "frame_index": 0,
        "viewport_source": "FIXED_SUBVIEWPORT_NO_WINDOW_DPI_DEPENDENCY",
        "viewport_width": WIDTH,
        "viewport_height": HEIGHT,
        "source_image_format": "RGBA8",
        "source_rgba_bytes": rgba.size(),
        "alpha_all_opaque": true,
        "rgb_pixel_format": "RGB24",
        "rgb_stride_bytes": WIDTH * 3,
        "rgb_bytes": rgb.size(),
        "rgb_sha256": rgb_sha256,
        "color_space": "UNDECLARED",
        "color_primaries": "UNDECLARED",
        "color_transfer": "UNDECLARED",
        "color_transform_applied": false,
        "channel_operation": "BYTE_EXACT_RGBA8_TO_RGB24_CHANNEL_EXTRACTION_ALPHA_VERIFIED_OPAQUE",
        "historical_mp4_consumed": false,
        "audio_generated": false,
        "ffmpeg_invoked": false,
        "ffprobe_invoked": false,
        "mux_invoked": false
    }
    var metadata_path := output_root.path_join("capture_metadata.json")
    var metadata_file := FileAccess.open(metadata_path, FileAccess.WRITE)
    if metadata_file == null:
        _fail("METADATA_OUTPUT_OPEN_FAILED")
        return
    metadata_file.store_string(JSON.stringify(metadata, "\t") + "\n")
    metadata_file.flush()
    metadata_file.close()
    print("C11E_L2_CAPTURE=PASS/ONE_FRAME")
    print("VIEWPORT_CAPTURE=FIXED_SUBVIEWPORT_720x1280")
    print("SOURCE_SELECTOR=E6-L-01; GAMEPLAY_SEED=100006; GRAMMAR=radial_bloom; FRAME=0")
    print("SOURCE_PIXELS=RGBA8_OPAQUE; RGB24_BYTES=2764800; STRIDE=2160")
    print("RGB24_SHA256=" + rgb_sha256)
    print("HISTORICAL_MP4_CONSUMED=FALSE; COLOR_TRANSFORM=NONE")
    print("AUDIO=OFF; FFMPEG=OFF; FFPROBE=OFF; MUX=OFF")
    capture_viewport.render_target_update_mode = SubViewport.UPDATE_DISABLED
    quit(0)
