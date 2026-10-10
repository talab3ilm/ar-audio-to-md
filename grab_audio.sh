#!/usr/bin/env bash
# Télécharge l'audio d'une vidéo YouTube en FLAC 16 kHz mono (sans perte, plus petit
# qu'un WAV), prêt pour transcribe.py.
#
# Usage :
#   ./grab_audio.sh mxWq9pEKBTs                      # ID de vidéo
#   ./grab_audio.sh "https://youtu.be/mxWq9pEKBTs"   # ou URL complète
#
# Le fichier est écrit dans le dossier courant sous la forme
#   "yyyy-mm-dd-hh-mm <titre> [<id>].flac"
# où la date est celle de diffusion (release_timestamp, début du direct), sinon celle
# de mise en ligne (timestamp). L'heure est dans le fuseau du système (UTC sous WSL) ;
# pour l'heure locale :  TZ=Europe/Paris ./grab_audio.sh <id>
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage : $0 <ID_YouTube | URL>" >&2
    exit 1
fi

INPUT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YTDLP="$SCRIPT_DIR/ytdl.py"   # lanceur yt-dlp qui contourne le mode restreint imposé par le DNS

if [[ ! -x "$YTDLP" ]]; then
    echo "yt-dlp introuvable : lancez d'abord  $SCRIPT_DIR/.venv/bin/pip install yt-dlp  (et vérifiez ytdl.py)" >&2
    exit 1
fi

# Un ID YouTube fait 11 caractères [A-Za-z0-9_-] ; sinon on suppose une URL.
if [[ "$INPUT" =~ ^[A-Za-z0-9_-]{11}$ ]]; then
    URL="https://www.youtube.com/watch?v=$INPUT"
else
    URL="$INPUT"
fi

YTDLP_ARGS=(--extractor-args "youtube:player_client=android")
# Vidéos privées ou réservées : exporter les cookies du navigateur connecté (extension
# "Get cookies.txt LOCALLY") dans cookies.txt à côté de ce script ; il est ignoré par git.
if [[ -f "$SCRIPT_DIR/cookies.txt" ]]; then
    YTDLP_ARGS+=(--cookies "$SCRIPT_DIR/cookies.txt")
fi

# 1. Métadonnées : horodatage de diffusion, sinon de mise en ligne ("NA" si absent)
read -r REL_TS UP_TS < <("$YTDLP" "${YTDLP_ARGS[@]}" --skip-download \
    --print "%(release_timestamp)s %(timestamp)s" "$URL")
TS="$REL_TS"
[[ "$TS" == "NA" || -z "$TS" ]] && TS="$UP_TS"
if [[ "$TS" == "NA" || -z "$TS" ]]; then
    echo "Avertissement : aucune date trouvée, préfixe 0000-00-00-00-00" >&2
    PREFIX="0000-00-00-00-00"
else
    PREFIX="$(date -d "@$TS" +%Y-%m-%d-%H-%M)"
fi

# 2. Téléchargement + conversion ; affiche le chemin du fichier produit
"$YTDLP" "${YTDLP_ARGS[@]}" \
    -x --audio-format flac \
    --postprocessor-args "ExtractAudio:-ar 16000 -ac 1" \
    -o "$PREFIX %(title)s [%(id)s].%(ext)s" \
    --print after_move:filepath \
    --no-simulate \
    "$URL"
