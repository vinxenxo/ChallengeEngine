import os
import subprocess
from pathlib import Path

def convert_mp4s_to_gifs(output_dir="./output"):
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ La carpeta {output_dir} no existe.")
        return

    # Buscar todos los ficheros .mp4 en la carpeta output (incluyendo subcarpetas)
    mp4_files = list(output_path.glob("**/*.mp4"))
    
    if not mp4_files:
        print("⚠️ No se encontraron archivos .mp4 en la carpeta output.")
        return

    print(f"🚀 Encontrados {len(mp4_files)} archivos de vídeo. Iniciando conversión a GIF...\n")

    for mp4 in mp4_files:
        gif_output = mp4.with_suffix(".gif")
        print(fn:=f"⏳ Procesando: {mp4.name} -> {gif_output.name}")

        # Comando ffmpeg con optimización de paleta (30fps, 540px de ancho para formato vertical 9:16)
        cmd = [
            "ffmpeg", "-y", "-i", str(mp4),
            "-vf", "fps=30,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            str(gif_output)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ OK: {gif_output.name}")
        except subprocess.CalledProcessError:
            print(f"❌ Error al convertir {mp4.name}")

    print("\n🏁 ¡Conversión masiva completada!")

if __name__ == "__main__":
    convert_mp4s_to_gifs()