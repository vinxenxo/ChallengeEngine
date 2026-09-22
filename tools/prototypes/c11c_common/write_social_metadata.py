import argparse
import json
from pathlib import Path

HASHTAGS = {
    "geometric": "#GenerativeArt #GeometricWaves #MathematicalArt #ProceduralArt #WaveArt #DigitalArt #TechArt #CyberpunkArt #Lissajous #AbstractArt",
    "fractal": "#GenerativeArt #FractalBloom #FractalArt #MathematicalArt #ProceduralArt #JuliaSet #GenerativeDesign #CyberpunkArt #DigitalArt #InfiniteArt",
    "sacred_symmetry": "#GenerativeArt #SacredSymmetry #MathematicalArt #ProceduralArt #Astrolabe #SteampunkArt #GenerativeDesign #DigitalArt #GeometricArt #CelestialArt",
    "living_particles": "#GenerativeArt #LivingParticles #ProceduralArt #SyntheticLife #FluidArt #ParticleArt #GenerativeDesign #BioArt #DigitalArt #CyberpunkArt",
    "invisible_forces": "#GenerativeArt #InvisibleForces #VectorField #MathematicalArt #PhysicsArt #ProceduralArt #Topography #CyberpunkArt #DigitalArt #GenerativeDesign",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--command', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    out_path = Path(args.output)
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    visual = m.get('visual', {})
    audio = m.get('audio', {})
    editorial = m.get('editorial', {})

    family = str(m.get('family_id', 'geometric'))
    display_name = str(m.get('display_name', family.upper()))
    grammar = str(m.get('grammar', 'UNKNOWN'))
    palette = str(m.get('palette', 'UNKNOWN'))
    seed = int(m.get('seed', 0))
    duration = float(visual.get('duration_seconds', 18.0))
    cycles = int(round(float(visual.get('loop_cycles', 1.0))))
    enabled = bool(audio.get('enabled', True))
    technobabble = str(m.get('technobabble', '')).strip()
    line1 = str(editorial.get('header_line_1', '')).strip()
    line2 = str(editorial.get('header_line_2', '')).strip()

    desc = (
        f"{display_name} — visual loop de arte generativa matemática y procedural. "
        f"Variante {grammar} con paleta {palette}, seed {seed}. "
        f"Duración {duration:.2f}s, {cycles} ciclo(s) completo(s), "
        f"{'audio ambiental determinista' if enabled else 'sin sonido'}. "
        "Diseñado para reproducción continua en bucle."
    )
    text = [
        f"TITLE: {display_name} // {grammar.upper()}",
        "",
        "DESCRIPTION:", desc,
        "",
        f"FAMILY: {family}",
        f"GRAMMAR: {grammar}",
        f"PALETTE: {palette}",
        f"SEED: {seed}",
        f"DURATION: {duration:.2f} s",
        f"FPS: {int(visual.get('fps', 30))}",
        f"FRAMES: {int(visual.get('frame_count', round(duration * 30)))}",
        f"LOOP CYCLES: {cycles}",
        f"LOOP CLOSED: {bool(visual.get('loop_closed', True))}",
        f"AUDIO: {'ON / DEEP AMBIENT' if enabled else 'OFF / SILENT'}",
        f"BACKGROUND: #{visual.get('background', '000000')}",
        "",
        "HEADER:",
        line1,
        line2,
        "",
        "EDITORIAL TRANSITION: deterministic Matrix / airport-board character scramble near midpoint.",
        f"TECHNOBABBLE: {technobabble}",
        "",
        "HASHTAGS:",
        HASHTAGS.get(family, '#GenerativeArt #MathematicalArt #ProceduralArt'),
        "",
        "REPRODUCTION COMMAND:",
        args.command,
        "",
        "CANONICAL MANIFEST:",
        manifest_path.name,
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(text) + '\n', encoding='utf-8')
    if not out_path.exists() or out_path.stat().st_size < 100:
        raise RuntimeError(f"social sidecar was not created: {out_path}")


if __name__ == '__main__':
    main()
