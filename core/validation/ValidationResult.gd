# res://core/validation/ValidationResult.gd
class_name ValidationResult
extends RefCounted

var is_valid: bool = false

var close_calls: int = 0
var minimum_distance: float = INF
var score: float = 0.0

# Frame ganador relativo al bloque GAME [0, game_frames).
var winning_frame: int = -1

# Frame ganador absoluto dentro del vídeo completo [hook_frames, hook_frames + game_frames).
var absolute_winning_frame: int = -1

# Ventana temporal absoluta permitida para el bloque GAME.
var valid_window_start: int = -1
var valid_window_end_exclusive: int = -1
var winning_frame_in_valid_window: bool = false

var errors: Array[String] = []
var warnings: Array[String] = []