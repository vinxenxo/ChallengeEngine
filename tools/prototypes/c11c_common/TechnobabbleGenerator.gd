class_name TechnobabbleGenerator
extends RefCounted

## C11-C deterministic geek/cyberpunk/steampunk editorial generator v2.0.
## Isolated integer hash: never touches project RNG streams.

const REVISION: String = "2.0.1"
const ACTIONS: Array[String] = ["Calibrando", "Sincronizando", "Acoplando", "Indexando", "Compilando", "Estabilizando", "Resolviendo", "Modulando", "Mapeando", "Desfasando", "Inyectando", "Decodificando", "Alineando", "Oscilando", "Renderizando", "Interfiriendo", "Refractando", "Trazando", "Reensamblando", "Afinando"]
const CYBER: Array[String] = ["nucleo neural", "stack fantasma", "bus de fotones", "protocolo neon", "matriz de fase", "daemon espectral", "cortafuegos cuantico", "puerto de singularidad", "firmware de realidad", "subrutina nocturna", "terminal psi", "kernel de sombra", "senal fantasma", "relay ionico", "memoria de borde", "nodo black-ice", "puente de datos", "proxy espectral", "buffer de entropia", "interfaz neuroptica", "sandbox fractal", "canal de telemetria", "vector de latencia", "checksum astral"]
const STEAMPUNK: Array[String] = ["engranaje de cobre", "oscilador de laton", "giroscopio de precision", "caldera de fase", "cronometro mecanico", "valvula de eter", "astrolabio de laton", "rotor de bronce", "regulador de vapor", "turbina de vapor", "inductor de mercurio", "reloj de cuarzo mecanico", "bobina de eter", "regulador isocronico", "camara de presion", "embrague de cobre"]
const STATUS: Array[String] = ["NOMINAL", "OPTIMO", "ESTABLE", "ACOPLADO", "SINCRO", "PARALEX", "HYPERDRIVE", "LOCKED", "CRITICO", "EN FASE", "CUANTIZADO", "SINCRONIA", "OVERCLOCK", "PHASE-LOCK", "STEADY", "FOCUS"]
const MODIFIERS: Array[String] = ["sin deriva", "sin perdida de fase", "bajo ruido", "en coherencia", "a maxima nitidez", "sin aliasing", "con fase estable", "en regimen orbital", "en modo stealth", "a baja entropia", "sincronizado al kernel", "con latencia cero", "en sobrecarga controlada", "a entropia minima", "sin jitter", "con señal limpia", "en fase cuantica", "sin desbordamiento", "a frecuencia fantasma"]
const UNITS: Array[String] = ["Hz", "kHz", "rad/s", "ms", "TeV", "Q-bits", "GHz", "iter/s", "cycles/s", "phase"]
const SUBJECTS := {
    "geometric": ["matriz de Lissajous", "interferencia de ondas", "membrana armonica", "malla de fase", "cinta parametrica", "campo de nodos", "plano de interferencia"],
    "fractal": ["fractal de Julia", "trampas de orbita", "ramificaciones de micelio", "filigrana fractal", "tunel dendritico", "mundo recursivo", "sinapsis L-System"],
    "sacred_symmetry": ["astrolabio cuantico", "engranaje planetario", "orrery poligonal", "mandala origami", "carta celeste", "rotor de bronce", "eje de alineacion"],
    "living_particles": ["atractores de Clifford", "nube magnetica", "dinamica de fluidos", "vortice organico", "swarm sintetico", "materia bioluminiscente", "corriente de particulas"],
    "invisible_forces": ["topografia gravitacional", "lineas equipotenciales", "viento solar", "campo dipolar", "cuadrupolo magnetico", "lente gravitacional", "cuenca de potencial"]
}
const TEMPLATES: Array[String] = [
    "{action} {subject}... [{status}] // {actual}",
    "[SYS] {action} {subject} a {value:.1f} {unit} // {modifier} // {actual}",
    "Parametro de {subject}: {value:.1f} {unit} // {status} // {actual}",
    "{subject} {modifier} // {status} // {actual}",
    "Kernel: {cyber} // objetivo: {subject} // {actual}",
    "{steam} // {subject} // {status} // {actual}",
    "TRACE: {subject} // {actual} // {modifier}",
    "SUBRUTINA // {cyber} -> {subject} // {status} // {actual}",
    "DEMONIO: {cyber} // {subject} // {actual}",
    "PROCESO {action} // {subject} // {actual} // {status}",
    "[DECK] {steam} :: {subject} :: {actual}"
]

static func generate_geek_text(family_id: String, seed_value: int, context: Dictionary = {}) -> String:
    var family: String = _canonical_family(family_id)
    var subject_pool: Array = SUBJECTS.get(family, SUBJECTS["geometric"])
    var action: String = ACTIONS[_index(seed_value, 11, ACTIONS.size())]
    var subject: String = str(subject_pool[_index(seed_value, 17, subject_pool.size())])
    var status: String = STATUS[_index(seed_value, 23, STATUS.size())]
    var unit: String = UNITS[_index(seed_value, 29, UNITS.size())]
    var modifier: String = MODIFIERS[_index(seed_value, 31, MODIFIERS.size())]
    var cyber: String = CYBER[_index(seed_value, 37, CYBER.size())]
    var steam: String = STEAMPUNK[_index(seed_value, 41, STEAMPUNK.size())]
    var value: float = 12.0 + 987.0 * _unit(seed_value, 43)
    var actual: String = _actual_phrase(family, context)
    var template: String = TEMPLATES[_index(seed_value, 47, TEMPLATES.size())]
    return template.format({"action": action, "subject": subject, "status": status, "unit": unit, "modifier": modifier, "cyber": cyber, "steam": steam, "value": value, "actual": actual})

static func _actual_phrase(family: String, context: Dictionary) -> String:
    match family:
        "geometric":
            return "WAVE %.2f | MORPH %.2f" % [float(context.get("wave_frequency", 0.0)), float(context.get("morph", 0.0))]
        "fractal":
            return "DETAIL %.2f | BRANCH %.2f" % [float(context.get("detail_scale", 0.0)), float(context.get("branch_density", 0.0))]
        "sacred_symmetry":
            return "N=%d | GEAR %d:%d" % [int(context.get("symmetry_order", 0)), int(context.get("gear_inner", 0)), int(context.get("gear_outer", 0))]
        "living_particles":
            return "PARTICLES %d | COLLISION %.2f" % [int(context.get("particle_count", 0.0)), float(context.get("collision_strength", 0.0))]
        "invisible_forces":
            return "TRACES %d | PULSE %.2f" % [int(context.get("trace_count", 0.0)), float(context.get("pulse_speed", 0.0))]
        _:
            return "SEED %d" % int(context.get("seed", 0))

static func revision() -> String:
    return REVISION

static func _canonical_family(family_id: String) -> String:
    match family_id:
        "c11c_geometric_waves_v1", "geometric", "geometric_waves": return "geometric"
        "c11c_fractal_bloom_v1", "fractal", "fractal_bloom": return "fractal"
        "c11c_sacred_symmetry_v1", "kaleidoscope", "sacred_symmetry": return "sacred_symmetry"
        "c11c_living_particles_v1", "particle_flow", "living_particles": return "living_particles"
        "c11c_invisible_forces_v1", "vector_field", "invisible_forces": return "invisible_forces"
        _: return "geometric"

static func _mixed(seed_value: int, salt: int) -> int:
    var x: int = (int(seed_value) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    return int(x ^ (x >> 16)) & 0x7fffffff

static func _index(seed_value: int, salt: int, size: int) -> int:
    return _mixed(seed_value, salt) % maxi(size, 1)

static func _unit(seed_value: int, salt: int) -> float:
    return float(_mixed(seed_value, salt) % 1000000) / 999999.0
