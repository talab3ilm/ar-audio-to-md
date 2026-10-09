#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Transcription audio arabe -> Markdown (faster-whisper large-v3, GPU) avec tashkeel.
#
# Usage :
#   ./transcribe.py "<fichier audio>"                     # écrit "<fichier audio>.md" à côté, voyelles ajoutées (CATT)
#   ./transcribe.py "<fichier audio>" sortie.md           # nom de sortie explicite
#   ./transcribe.py "<fichier audio>" --tashkeel ichkil   # autre modèle de vocalisation
#   ./transcribe.py "<fichier audio>" --tashkeel none     # texte brut, sans voyelles
#   ./transcribe.py "<fichier audio>" --model large-v3-turbo   # plus rapide, un peu moins précis
import os
import sys
import ctypes
import glob
import site

# Précharge cuBLAS / cuDNN installés via pip (nvidia-cublas-cu12, nvidia-cudnn-cu12)
# pour que ctranslate2 les trouve sans LD_LIBRARY_PATH (nécessaire sous WSL).
for _pat in (
    "nvidia/cublas/lib/libcublas.so.*",
    "nvidia/cublas/lib/libcublasLt.so.*",
    "nvidia/cudnn/lib/libcudnn.so.*",
):
    for _sp in site.getsitepackages():
        for _lib in glob.glob(os.path.join(_sp, _pat)):
            ctypes.CDLL(_lib, mode=ctypes.RTLD_GLOBAL)

import argparse
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser(
    description="Transcription audio arabe -> Markdown (faster-whisper + tashkeel)",
    usage="%(prog)s <fichier_audio> [fichier_sortie.md] [--tashkeel catt|ichkil|none] [--model ...]",
)
parser.add_argument("audio_file", metavar="fichier_audio", help="fichier audio (flac, wav, mp3, m4a...)")
parser.add_argument("output_file", metavar="fichier_sortie", nargs="?", default=None,
                    help="fichier Markdown de sortie (défaut : <fichier_audio>.md)")
parser.add_argument("--tashkeel", choices=["catt", "ichkil", "none"], default="catt",
                    help="Modèle de vocalisation (الشكل) appliqué au texte transcrit. "
                         "catt : transformer encodeur-décodeur (Apache 2.0, GPU), le plus précis. "
                         "ichkil : petit modèle ONNX CPU (MIT). none : texte brut. Défaut : catt.")
parser.add_argument("--model", default="large-v3",
                    help="Modèle Whisper (défaut : large-v3 ; large-v3-turbo est plus rapide)")
args = parser.parse_args()
audio_file = args.audio_file
output_file = args.output_file or os.path.splitext(audio_file)[0] + ".md"

if not os.path.exists(audio_file):
    sys.exit(f"Erreur : le fichier audio '{audio_file}' n'existe pas.")


# --- Vocalisation (tashkeel) en post-traitement : Whisper ne produit pas de voyelles. ---
def load_vocalizer(name):
    """Renvoie une fonction list[str] -> list[str], ou None."""
    if name == "none":
        return None
    if name == "catt":
        try:
            from catt_tashkeel import CATTEncoderDecoder
        except ImportError:
            sys.exit("--tashkeel catt : installez d'abord  .venv/bin/pip install catt-tashkeel")
        catt = CATTEncoderDecoder()
        return lambda texts: catt.do_tashkeel_batch(texts, verbose=False)
    if name == "ichkil":
        try:
            import ichkil
        except ImportError:
            sys.exit("--tashkeel ichkil : installez d'abord  .venv/bin/pip install ichkil")
        return lambda texts: [ichkil.diacritize(t) for t in texts]


vocalize = load_vocalizer(args.tashkeel)

# Option GPU (carte NVIDIA) : device="cuda", compute_type="float16"
model = WhisperModel(args.model, device="cuda", compute_type="float16")
# Option CPU : device="cpu", compute_type="int8"
# model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=4)

print(f"Début de la transcription ({args.model})...")

segments, info = model.transcribe(
    audio_file,
    language="ar",
    beam_size=5,
    vad_filter=True,       # Filtre les silences pour accélérer le traitement
    chunk_length=30,       # Traite l'audio par morceaux de 30 s pour limiter la RAM
    word_timestamps=False, # Désactive le découpage mot par mot
)

print(f"Langue détectée : {info.language} (probabilité : {info.language_probability:.2f})")

# 1. Transcription : on consomme le générateur en affichant la progression
rows = []
for segment in segments:
    text = segment.text.strip()
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {text}")
    rows.append((segment.start, segment.end, text))

# 2. Tashkeel par lots (bien plus rapide que segment par segment)
if vocalize and rows:
    print(f"\nVocalisation ({args.tashkeel}) de {len(rows)} segments...")
    texts = [r[2] for r in rows]
    BATCH = 64
    vocalized = []
    for i in range(0, len(texts), BATCH):
        vocalized.extend(vocalize(texts[i:i + BATCH]))
    rows = [(s, e, v) for (s, e, _), v in zip(rows, vocalized)]

# 3. Écriture du Markdown
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# Transcription: {os.path.basename(audio_file)}\n\n")
    f.write(f"Modèle : {args.model} · Tashkeel : {args.tashkeel}\n\n")
    f.write("---\n\n")
    for start, end, text in rows:
        f.write(f"**[{start:.2f}s -> {end:.2f}s]** {text}\n\n")

print(f"\nTerminé ! Votre fichier '{output_file}' est prêt ({len(rows)} segments).")
