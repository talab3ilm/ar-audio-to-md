#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Lit sources.txt, traite ce qui est nouveau et dépose le résultat dans secondBrain/raw/.
#
# Usage :
#   ./pull_sources.py                 # traite toutes les sources nouvelles
#   ./pull_sources.py --dry-run       # affiche ce qui serait fait, sans rien lancer
#   ./pull_sources.py --max-new 3     # au plus 3 vidéos nouvelles par passage (utile pour une chaîne)
#   ./pull_sources.py --force URL     # retraite une source même si elle est dans le registre
#   ./pull_sources.py --list          # état de chaque source (nouvelle / faite / en erreur)
#
# Registre : sources.done.tsv (une ligne par source traitée : date, type, id, chemin produit).
# Une vidéo est considérée faite si son id figure dans le registre OU si un dossier
# "… [<id>]" existe déjà dans secondBrain/raw/youtube/ (cas des 3 premiers cours).
import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv" / "bin"
SOURCES = ROOT / "sources.txt"
DONE = ROOT / "sources.done.tsv"
AUDIO = ROOT / "audio"
RAW = ROOT / "secondBrain" / "raw"
RAW_YT = RAW / "youtube"
RAW_PDF = RAW / "pdfs"

YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
COOKIES = ROOT / "cookies.txt"          # export du navigateur connecté, pour les vidéos privées (hors git)
# ytdl.py : yt-dlp sans le mode restreint imposé par le DNS du réseau
YTDLP_BASE = [str(ROOT / "ytdl.py"), "--extractor-args", "youtube:player_client=android"] + \
             (["--cookies", str(COOKIES)] if COOKIES.exists() else [])


# ----------------------------------------------------------------------------- registre
def load_done():
    done = {}
    if DONE.exists():
        for line in DONE.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 3 and not (len(parts) >= 5 and parts[4].startswith("ERREUR")):
                done[(parts[1], parts[2])] = parts
    return done


def mark_done(kind, ident, path, note=""):
    new = not DONE.exists()
    with DONE.open("a", encoding="utf-8") as f:
        if new:
            f.write("# date\ttype\tid\tchemin\tnote\n")
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M}\t{kind}\t{ident}\t{path}\t{note}\n")


def youtube_folder_for(video_id):
    """Dossier raw/youtube/… [id] déjà existant, ou None."""
    if not RAW_YT.exists():
        return None
    for d in RAW_YT.iterdir():
        if d.is_dir() and d.name.endswith(f"[{video_id}]"):
            return d
    return None


# ----------------------------------------------------------------------------- lecture de sources.txt
def parse_sources():
    items = []
    for raw in SOURCES.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        url, _, opts = line.partition("|")
        url = url.strip()
        options = {}
        for opt in opts.split("|"):
            if "=" in opt:
                k, v = opt.split("=", 1)
                options[k.strip()] = v.strip()
        items.append((url, options))
    return items


def classify(url):
    u = urlparse(url)
    host = u.netloc.lower()
    if "youtu.be" in host:
        return "video", u.path.strip("/").split("/")[0]
    if "youtube.com" in host:
        qs = parse_qs(u.query)
        if "list" in qs and "playlist" in u.path:
            return "playlist", qs["list"][0]
        if "v" in qs:
            return "video", qs["v"][0]
        if u.path.startswith("/@") or "/channel/" in u.path or "/c/" in u.path:
            return "channel", u.path.strip("/")
        m = re.match(r"^/(shorts|live)/([A-Za-z0-9_-]{11})", u.path)
        if m:
            return "video", m.group(2)
    if "turath.io" in host:
        m = re.search(r"/book/(\d+)", u.path)
        return ("book", m.group(1)) if m else ("unknown", url)
    if "aljam3.com" in host:
        return "aljam3", url          # accepté mais non traité : le même scan est atteint via turath
    return "unknown", url


def process_book(book_id, options, dry_run=False):
    """Livre turath -> raw/pdfs/<catégorie>/<ouvrage>/ via turath_to_md.py (TXT des scans téléchargés
    automatiquement depuis Hugging Face pour le tashkeel et les notes)."""
    categorie = options.get("catégorie", options.get("categorie", options.get("matière", options.get("matiere", "غير مصنف"))))
    cmd = [ROOT / "turath_to_md.py", book_id, "--categorie", categorie]
    if options.get("ouvrage"):
        cmd += ["--ouvrage", options["ouvrage"]]
    if options.get("pdf", "").lower() in ("oui", "yes", "1", "true"):
        cmd.append("--pdf")
    if dry_run:
        print("  [dry-run]", " ".join(str(c) for c in cmd))
        return None
    res = run(cmd, capture_output=True, text=True)
    print("  " + res.stdout.strip().replace("\n", "\n  "))
    written = [l.split("->", 1)[1].strip() for l in res.stdout.splitlines() if "->" in l]
    return Path(written[0]).parent if written else None


def expand_list(url):
    """Playlist ou chaîne -> liste d'ids de vidéos (sans téléchargement)."""
    out = subprocess.run(
        YTDLP_BASE + ["--flat-playlist", "--print", "%(id)s", url],
        capture_output=True, text=True)
    ids = [l.strip() for l in out.stdout.splitlines() if YT_ID.match(l.strip())]
    if out.returncode != 0 and not ids:
        print(f"  ! yt-dlp n'a pas pu lire {url} : {out.stderr.strip().splitlines()[-1] if out.stderr else ''}")
    return ids


# ----------------------------------------------------------------------------- traitement d'une vidéo
def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd))
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def process_video(video_id, options, dry_run=False):
    url = f"https://www.youtube.com/watch?v={video_id}"
    if dry_run:
        print(f"  [dry-run] grab + transcribe + md_to_text -> raw/youtube/… [{video_id}]")
        return None
    AUDIO.mkdir(exist_ok=True)
    # 1. audio (grab_audio.sh écrit dans le dossier courant -> on se place dans audio/)
    res = run([ROOT / "grab_audio.sh", url], cwd=AUDIO, capture_output=True, text=True)
    flac = Path(res.stdout.strip().splitlines()[-1])
    base = flac.stem
    # 2. transcription + 3. texte continu
    transcript = flac.with_suffix(".md")
    run([ROOT / "transcribe.py", flac, transcript])
    texte = flac.with_name(base + "_texte.md")
    run([ROOT / "md_to_text.py", transcript, texte])
    # 4. dépôt dans raw/youtube/<base>/
    dest = RAW_YT / base
    dest.mkdir(parents=True, exist_ok=True)
    transcript.rename(dest / "transcript.md")
    texte.rename(dest / "texte.md")
    write_meta(dest, video_id, options)
    return dest


def write_meta(dest, video_id, options):
    out = subprocess.run(
        YTDLP_BASE + ["--skip-download",
         "--print", "%(title)s\t%(channel)s\t%(channel_url)s\t%(duration)s\t%(release_timestamp,timestamp)s\t%(webpage_url)s",
         f"https://www.youtube.com/watch?v={video_id}"],
        capture_output=True, text=True)
    title, channel, churl, dur, ts, url = (out.stdout.strip().split("\t") + [""] * 6)[:6]
    speaker = re.sub(r".*[|｜]\s*", "", title)
    try:
        dur = int(float(dur)); hms = f"{dur // 3600:02d}:{dur % 3600 // 60:02d}:{dur % 60:02d}"
    except ValueError:
        hms = ""
    try:
        date = dt.datetime.fromtimestamp(int(float(ts))).strftime("%Y-%m-%d")
    except ValueError:
        date = ""
    matiere = options.get("matière", options.get("matiere", ""))
    (dest / "meta.md").write_text(f"""---
source: youtube
id: {video_id}
url: {url}
title: "{title}"
channel: "{channel}"
channel_url: {churl}
speaker: "{speaker}"
series: "{matiere}"
date: {date}
duration: {hms}
transcription: faster-whisper large-v3 (beam 5, VAD) + tashkeel CATT (encodeur-décodeur)
transcribed: {dt.date.today():%Y-%m-%d}
validated: false
---

Dossier produit par le pipeline. `transcript.md` = segments horodatés avec tashkeel ; `texte.md` = texte continu.
Validation : copier `texte.md` en `texte-ok.md`, corriger, puis passer `validated` à true.
""", encoding="utf-8")


# ----------------------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description="Traite les sources nouvelles de sources.txt")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-new", type=int, default=0, help="nombre max de vidéos nouvelles par passage (0 = illimité)")
    ap.add_argument("--force", action="append", default=[], metavar="URL", help="retraiter cette URL même si déjà faite")
    ap.add_argument("--list", action="store_true", help="afficher l'état de chaque source et sortir")
    args = ap.parse_args()

    done = load_done()
    forced = set()
    for u in args.force:
        kind, ident = classify(u)
        forced.add(ident)

    # 1. Développer sources.txt en une liste de vidéos et de livres
    videos, books = [], []
    for url, options in parse_sources():
        kind, ident = classify(url)
        if kind == "video":
            videos.append((ident, options, url))
        elif kind in ("playlist", "channel"):
            print(f"Lecture de la {kind} {ident} …")
            for vid in expand_list(url):
                videos.append((vid, options, f"https://www.youtube.com/watch?v={vid}"))
        elif kind == "book":
            books.append((ident, options))
        elif kind == "aljam3":
            print(f"  (aljam3 ignoré : indiquer le lien turath du même livre) {url}")
        else:
            print(f"! URL non reconnue, ignorée : {url}")

    # 2. État
    todo_videos = []
    for vid, options, url in videos:
        existing = youtube_folder_for(vid)
        is_done = (("video", vid) in done) or existing is not None
        if existing is not None and ("video", vid) not in done:
            mark_done("video", vid, existing.relative_to(ROOT), "déjà présent dans raw/ (ajouté au registre)")
            done[("video", vid)] = True
        if args.list:
            print(f"{'fait   ' if is_done else 'nouveau'}  vidéo  {vid}  {url}")
        if (not is_done) or vid in forced:
            todo_videos.append((vid, options))
    for ident, options in books:
        is_done = ("book", ident) in done
        if args.list:
            print(f"{'fait   ' if is_done else 'nouveau'}  livre  turath {ident}  {options}")
    if args.list:
        return

    # 3. Vidéos
    if args.max_new:
        todo_videos = todo_videos[: args.max_new]
    print(f"{len(todo_videos)} vidéo(s) à traiter.")
    for vid, options in todo_videos:
        print(f"\n=== vidéo {vid}")
        try:
            dest = process_video(vid, options, dry_run=args.dry_run)
            if dest is not None:
                mark_done("video", vid, dest.relative_to(ROOT))
                print(f"  -> {dest.relative_to(ROOT)}")
        except subprocess.CalledProcessError as e:
            print(f"  ! échec : {e}")
            mark_done("video", vid, "", f"ERREUR {e.returncode}")

    # 4. Livres turath -> raw/pdfs/
    new_books = [(i, o) for i, o in books if ("book", i) not in done or i in forced]
    print(f"\n{len(new_books)} livre(s) à convertir.")
    for ident, options in new_books:
        print(f"\n=== livre turath {ident}")
        try:
            dest = process_book(ident, options, dry_run=args.dry_run)
            if dest is not None:
                mark_done("book", ident, dest.relative_to(ROOT) if dest.is_absolute() else dest)
                print(f"  -> {dest}")
        except subprocess.CalledProcessError as e:
            print(f"  ! échec : {e}\n{(e.stderr or '')[-800:]}")
            mark_done("book", ident, "", f"ERREUR {e.returncode}")

    print("\nTerminé. Prochaine étape : relire texte.md -> texte-ok.md, puis draft_lesson.py et /ingest.")


if __name__ == "__main__":
    main()
