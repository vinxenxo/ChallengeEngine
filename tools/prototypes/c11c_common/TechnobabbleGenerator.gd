class_name TechnobabbleGenerator
extends RefCounted

## C11-C editorial layer — deterministic geek / technobabble text.
## Prototype-only utility. No engine RNG stream is touched.
## Same family + same seed => same text, forever within this generator revision.

const ACTIONS := [
    "Calibrando",
    "Sincronizando",
    "Estabilizando",
    "Iterando",
    "Modulando",
    "Resolviendo",
    "Ajustando",
    "Compilando",
    "Acoplando",
    "Desfasando",
    "Mapeando",
    "Extrapolando"
]

const STATUSES := [
    "NOMINAL",
    "ESTABLE",
    "OPTIMO",
    "ACOPLADO",
    "CONVERGENTE",
    "EN FASE",
    "BAJA ENTROPIA",
    "SINGULAR"
]

const SUBJECTS := {
    "geometric": [
        "matriz de Lissajous",
        "interferencia de ondas",
        "grilla de Voronoi",
        "nodos armonicos",
        "resonancia poligonal",
        "fase geometrica",
        "malla de amplitud",
        "simetria de onda"
    ],
    "fractal": [
        "fractal de Julia",
        "ramificaciones de micelio",
        "trampas de orbita",
        "sinapsis L-System",
        "campo complejo",
        "nucleo recursivo",
        "zoom analitico",
        "iteracion fractal"
    ],
    "kaleidoscope": [
        "astrolabio cuantico",
        "simetria radial",
        "ejes de rotacion",
        "teselaciones",
        "engranaje polar",
        "nucleo orbital",
        "anillo equiponderado",
        "mecanismo celeste"
    ],
    "particle_flow": [
        "atractores de Clifford",
        "dinamica de fluidos",
        "densidad magnetica",
        "vortice principal",
        "campo de Curl Noise",
        "nube de particulas",
        "pozo gravitacional",
        "flujo tangencial"
    ],
    "vector_field": [
        "topografia gravitacional",
        "flujo de viento solar",
        "lineas equipotenciales",
        "campo vectorial",
        "frente de presion",
        "pozo de potencial",
        "corriente termica",
        "gradiente de fuerza"
    ]
}

const UNITS := {
    "geometric": ["Hz", "rad/s", "ciclos/s", "px/frame"],
    "fractal": ["iter/s", "Hz", "rad/s", "niveles"],
    "kaleidoscope": ["Hz", "rad/s", "vueltas/s", "grados"],
    "particle_flow": ["u/s", "Hz", "m/s", "densidades"],
    "vector_field": ["Hz", "rad/s", "u/s", "tesla*eq"]
}

const TEMPLATES := [
    "%s %s... [%s]",
    "[SYS] %s %s a %.1f %s",
    "Parametro de %s: %.1f %s // Estado: %s",
    "PROTOCOLO // %s // %s // %s",
    "OBSERVADOR: %s -> %s // %.1f %s",
    "TRACE %03d // %s // %s"
]

static func generate_geek_text(family_id: String, seed_value: int) -> String:
    var canonical_family: String = _canonical_family(family_id)
    var family_salt: int = _family_salt(canonical_family)
    var action: String = str(ACTIONS[_index(seed_value, family_salt + 11, ACTIONS.size())])
    var subjects: Array = SUBJECTS.get(canonical_family, SUBJECTS["geometric"])
    var subject: String = str(subjects[_index(seed_value, family_salt + 17, subjects.size())])
    var status: String = str(STATUSES[_index(seed_value, family_salt + 23, STATUSES.size())])
    var units: Array = UNITS.get(canonical_family, UNITS["geometric"])
    var unit: String = str(units[_index(seed_value, family_salt + 29, units.size())])
    var fake_value: float = float(lerpf(12.0, 999.9, _unit(seed_value, family_salt + 31)))
    var trace: int = int(_index(seed_value, family_salt + 37, 1000))
    var template_id: int = int(_index(seed_value, family_salt + 41, TEMPLATES.size()))

    match template_id:
        0:
            return "%s %s... [%s]" % [action, subject, status]
        1:
            return "[SYS] %s %s a %.1f %s" % [action, subject, fake_value, unit]
        2:
            return "Parametro de %s: %.1f %s // Estado: %s" % [subject, fake_value, unit, status]
        3:
            return "PROTOCOLO // %s // %s // %s" % [action.to_upper(), subject.to_upper(), status]
        4:
            return "OBSERVADOR: %s -> %s // %.1f %s" % [subject, status, fake_value, unit]
        5:
            return "TRACE %03d // %s // %s" % [trace, action, subject]
        _:
            return "Generando %s..." % subject

static func generate_geek_text_for_seed(family_id: String, seed_value: int) -> String:
    return generate_geek_text(family_id, seed_value)

static func _canonical_family(family_id: String) -> String:
    match family_id:
        "c11c_geometric_waves_v1", "geometric", "geometric_waves":
            return "geometric"
        "c11c_fractal_bloom_v1", "fractal", "fractal_bloom":
            return "fractal"
        "c11c_sacred_symmetry_v1", "kaleidoscope", "sacred_symmetry":
            return "kaleidoscope"
        "c11c_living_particles_v1", "particle_flow", "living_particles":
            return "particle_flow"
        "c11c_invisible_forces_v1", "vector_field", "invisible_forces":
            return "vector_field"
        _:
            return "geometric"

static func _family_salt(family_id: String) -> int:
    var value := 2166136261
    for byte in family_id.to_utf8_buffer():
        value = int((value ^ int(byte)) * 16777619) & 0x7fffffff
    return value

static func _mixed(seed_value: int, salt: int) -> int:
    var x := (int(seed_value) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    return int(x ^ (x >> 16)) & 0x7fffffff

static func _index(seed_value: int, salt: int, size: int) -> int:
    return _mixed(seed_value, salt) % maxi(size, 1)

static func _unit(seed_value: int, salt: int) -> float:
    return float(_mixed(seed_value, salt) % 1000000) / 999999.0
