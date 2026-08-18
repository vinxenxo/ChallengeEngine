# DOMAIN_MODEL.md — Modelo de dominio y contratos de datos

## 1. Contrato JSON Declarativo (Entrada Capa 0)

```json
{
  "id": "CHALLENGE_001",
  "engine_version": "0.1",
  "mechanic": "key",
  "mechanic_version": "1.0",
  "video": {
    "fps": 60,
    "hook_duration": 3.0,
    "game_duration": 7.0,
    "cta_duration": 1.0
  },
  "difficulty": {
    "level": 5,
    "tolerance": {
      "rotation_deg": 4.5
    }
  },
  "generation": {
    "seed": 193847
  },
  "assets": {
    "background_path": "res://assets/families/fam_001/bg.png",
    "target_path": "res://assets/families/fam_001/target.png",
    "object_path": "res://assets/families/fam_001/key.png"
  },
  "content": {
    "hook": "¡SOLO EL 1% LLEGA AL CENTRO!",
    "cta": "¡INTÉNTALO TÚ TAMBIÉN!"
  }
}