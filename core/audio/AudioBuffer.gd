# core/audio/AudioBuffer.gd
class_name AudioBuffer
extends RefCounted

const SAMPLE_RATE = 44100
const CHANNELS = 1

var sample_rate: int
var channels: int
var data: PackedFloat32Array

func _init(p_sample_rate: int = SAMPLE_RATE, p_channels: int = CHANNELS):
	sample_rate = p_sample_rate
	channels = p_channels
	data = PackedFloat32Array()

# Conversión PCM16 canónica con cuantización simétrica y clamping obligatorio
func get_pcm16_bytes() -> PackedByteArray:
	var bytes = PackedByteArray()
	bytes.resize(data.size() * 2) # 2 bytes por muestra (Int16)
	
	for i in range(data.size()):
		# 1. Clamping estricto al rango normalizado [-1.0, 1.0]
		var sample = clampf(data[i], -1.0, 1.0)
		
		# 2. Cuantización simétrica a Signed 16-bit [-32768, 32767]
		var pcm_val = 0
		if sample < 0.0:
			pcm_val = int(sample * 32768.0)
		else:
			pcm_val = int(sample * 32767.0)
			
		pcm_val = clampi(pcm_val, -32768, 32767)
		
		# 3. Empaquetado explícito Little-Endian (2 bytes)
		var low_byte = pcm_val & 0xFF
		var high_byte = (pcm_val >> 8) & 0xFF
		bytes[i * 2] = low_byte
		bytes[(i * 2) + 1] = high_byte
		
	return bytes

# Hash criptográfico canónico sobre la representación de bytes exactos (SHA-256)
func get_canonical_hash() -> String:
	var raw_bytes = get_pcm16_bytes()
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(raw_bytes)
	var hash_bytes = ctx.finish()
	return hash_bytes.hex_encode()