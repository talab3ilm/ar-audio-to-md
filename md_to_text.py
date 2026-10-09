#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Transforme une transcription Markdown horodatée (sortie de transcribe.py) en texte
# continu sans marques de temps.
#
# Usage :
#   ./md_to_text.py "<fichier>.md"                     # écrit "<fichier>_texte.md" à côté
#   ./md_to_text.py "<fichier>.md" sortie.md           # nom de sortie explicite
#   ./md_to_text.py "<fichier>.md" --pause 3           # nouveau paragraphe si silence > 3 s (défaut 2)
#   ./md_to_text.py "<fichier>.md" --mots 150          # ou dès que le paragraphe atteint 150 mots (défaut 100)
#   ./md_to_text.py "<fichier>.md" --lignes            # un segment par ligne, sans regroupement
import argparse
import os
import re
import sys

# Ligne produite par transcribe.py : **[12.34s -> 56.78s]** texte
TIMESTAMP_RE = re.compile(r"^\*\*\[(?P<start>[\d.]+)s\s*->\s*(?P<end>[\d.]+)s\]\*\*\s*(?P<text>.*)$")

parser = argparse.ArgumentParser(
    description="Transcription Markdown horodatée -> texte seul",
    usage="%(prog)s <fichier_md> [fichier_sortie.md] [--pause S] [--lignes]",
)
parser.add_argument("input_file", metavar="fichier_md", help="fichier .md produit par transcribe.py")
parser.add_argument("output_file", metavar="fichier_sortie", nargs="?", default=None,
                    help="fichier de sortie (défaut : <fichier_md>_texte.md)")
parser.add_argument("--pause", type=float, default=2.0,
                    help="silence (en secondes) entre deux segments à partir duquel on ouvre "
                         "un nouveau paragraphe (défaut : 2)")
parser.add_argument("--mots", type=int, default=100,
                    help="nombre de mots à partir duquel on ouvre un nouveau paragraphe à la "
                         "prochaine frontière de segment (défaut : 100 ; 0 = illimité)")
parser.add_argument("--lignes", action="store_true",
                    help="un segment par ligne, sans regroupement en paragraphes")
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file or os.path.splitext(input_file)[0] + "_texte.md"

if not os.path.exists(input_file):
    sys.exit(f"Erreur : le fichier '{input_file}' n'existe pas.")

title = None
segments = []  # (start, end, text)
with open(input_file, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if title is None and line.startswith("# "):
            title = line
            continue
        m = TIMESTAMP_RE.match(line)
        if not m:
            continue  # en-tête, séparateur, lignes vides
        text = m.group("text").strip()
        if not text:
            continue  # segment vide (silence ou musique)
        segments.append((float(m.group("start")), float(m.group("end")), text))

if not segments:
    sys.exit(f"Erreur : aucun segment horodaté trouvé dans '{input_file}'.")

# Regroupement en paragraphes : on coupe quand le silence entre deux segments dépasse
# --pause, ou quand le paragraphe en cours atteint --mots mots (Whisper produit souvent
# des segments courts, sans ponctuation ni silence, qui donneraient un seul bloc).
paragraphs = []
if args.lignes:
    paragraphs = [[t] for _, _, t in segments]
else:
    current = [segments[0][2]]
    words = len(segments[0][2].split())
    prev_end = segments[0][1]
    for start, end, text in segments[1:]:
        if start - prev_end > args.pause or (args.mots and words >= args.mots):
            paragraphs.append(current)
            current, words = [], 0
        current.append(text)
        words += len(text.split())
        prev_end = end
    paragraphs.append(current)

with open(output_file, "w", encoding="utf-8") as f:
    if title:
        f.write(title + "\n\n")
    for p in paragraphs:
        f.write(" ".join(p) + "\n\n")

print(f"{len(segments)} segments -> {len(paragraphs)} paragraphes : '{output_file}'")
