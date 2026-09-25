import argparse
import json
import re
import unicodedata
from pathlib import Path

FIXED_HASHTAGS = ["#GenerativeArt", "#GodotEngine", "#LoopArt", "#OddlySatisfying"]
FAMILY_HASHTAGS = {
    "geometric": ["#GeometricWaves", "#WaveArt", "#MathematicalArt", "#ProceduralArt", "#DigitalArt", "#TechArt"],
    "fractal": ["#FractalBloom", "#FractalArt", "#MathematicalArt", "#ProceduralArt", "#JuliaSet", "#DigitalArt"],
    "sacred_symmetry": ["#SacredSymmetry", "#GeometricArt", "#Astrolabe", "#CelestialArt", "#ProceduralArt", "#DigitalArt"],
    "living_particles": ["#LivingParticles", "#ParticleArt", "#FluidArt", "#OrganicArt", "#ProceduralArt", "#DigitalArt"],
    "invisible_forces": ["#InvisibleForces", "#VectorField", "#PhysicsArt", "#TopographicArt", "#ProceduralArt", "#DigitalArt"],
}
DRILL_HASHTAGS = {
    "tracking": ["#VisualDrill", "#Tracking", "#SmoothPursuit", "#VisualChallenge", "#Perception", "#ProceduralArt"],
    "saccade": ["#VisualDrill", "#Saccade", "#VisualChallenge", "#SpatialPrecision", "#Perception", "#ProceduralArt"],
    "pursuit": ["#VisualDrill", "#Pursuit", "#SmoothPursuit", "#FovealAttention", "#VisualChallenge", "#ProceduralArt"],
    "peripheral_scan": ["#VisualDrill", "#PeripheralScan", "#PeripheralVision", "#VisualChallenge", "#Perception", "#ProceduralArt"],
}


def clean_text(value: str) -> str:
    cleaned = []
    for c in str(value):
        category = unicodedata.category(c)
        if ord(c) in (0xFE0F, 0x200D) or category in {"So", "Sk"}:
            continue
        cleaned.append(c)
    return ''.join(cleaned)


def grammar_hashtag(grammar: str) -> str:
    words = [w for w in re.split(r'[^A-Za-z0-9]+', grammar.strip()) if w]
    return '#' + ''.join(w[:1].upper() + w[1:] for w in words) if words else ''


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--command', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    out_path = Path(args.output)
    m = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    visual = m.get('visual', {})
    audio = m.get('audio', {})
    editorial = m.get('editorial', {})

    family = str(m.get('family_id', 'geometric'))
    display_name = clean_text(m.get('display_name', family.upper()))
    grammar = clean_text(m.get('grammar', 'UNKNOWN'))
    palette = clean_text(m.get('palette', 'UNKNOWN'))
    seed = int(m.get('seed', 0))
    duration = float(visual.get('duration_seconds', 18.0))
    cycles = int(round(float(visual.get('loop_cycles', 1.0))))
    enabled = bool(audio.get('enabled', True))
    audio_profile = clean_text(audio.get('profile_id', 'FAMILY_MUSIC_V4'))
    line2 = clean_text(editorial.get('header_line_2', '')).strip()
    loop_hook = line2 or '¿Puedes notar dónde termina el bucle?'

    base_tags = FIXED_HASHTAGS[:]
    if family in DRILL_HASHTAGS:
        own_tags = DRILL_HASHTAGS[family]
        title_prefix = 'Visual drill'
    else:
        own_tags = FAMILY_HASHTAGS.get(family, ['#ProceduralArt', '#DigitalArt'])
        title_prefix = 'Visual loop'
    tags = list(dict.fromkeys(base_tags + own_tags + ([grammar_hashtag(grammar)] if family not in DRILL_HASHTAGS else [])))
    hashtag_line = ' '.join(tags)

    desc = (
        f'{loop_hook}\n\n'
        f'**{display_name}** — {title_prefix} de arte generativa matemática y procedural.\n\n'
        f'- **Variante:** {grammar}\n'
        f'- **Paleta:** {palette}\n'
        f'- **Seed:** {seed}\n'
        f'- **Detalles:** Duración {duration:.2f}s, {cycles} ciclo(s) completo(s), '
        f'{"música ambiental determinista" if enabled else "sin sonido"}.\n\n'
        f'Diseñado en código con #GodotEngine para reproducción continua en bucle.'
    )

    text = [
        desc,
        '',
        'TITLE:', f'{display_name} — {grammar.upper()}',
        '',
        'DESCRIPTION:', desc,
        '',
        f'FAMILY: {family}',
        f'GRAMMAR: {grammar}',
        f'PALETTE: {palette}',
        f'SEED: {seed}',
        f'DURATION: {duration:.2f} s',
        f'FPS: {int(visual.get("fps", 30))}',
        f'FRAMES: {int(visual.get("frame_count", round(duration * 30)))}',
        f'LOOP CYCLES: {cycles}',
        f'LOOP CLOSED: {bool(visual.get("loop_closed", True))}',
        f'AUDIO: {"ON / " + audio_profile if enabled else "OFF / SILENT"}',
        f'AUDIO PROFILE: {audio_profile}',
        '',
        'HEADER HOOK:', loop_hook,
        '',
        'HASHTAGS:', hashtag_line,
        '',
        'REPRODUCTION COMMAND:', args.command,
        '',
        'CANONICAL MANIFEST:', manifest_path.name,
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(text) + '\n', encoding='utf-8')
    if not out_path.exists() or out_path.stat().st_size < 100:
        raise RuntimeError(f'social sidecar was not created: {out_path}')


if __name__ == '__main__':
    main()
