#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Récupère les pièces jointes (PDF des cours) de la plateforme de l'académie.
#
# 1. Liste : soit le fichier attachments/attachments.json déjà exporté (défaut), soit l'API
#    de la plateforme avec un jeton (port du script get_attachements.js) :
#       ./get_attachments.py --fetch --api https://<domaine>/api --token <ACCESS_TOKEN> [--level 1]
# 2. Téléchargement de chaque URL (S3 public, pas d'authentification) dans
#       attachments/pdf/<niveau>/<matière>/<id> - <titre>.pdf
#    Les fichiers déjà présents et complets ne sont pas retéléchargés. Un index
#    attachments/index.tsv est écrit (id, matière, niveau, titre, activé, date de déblocage, fichier).
#
# Usage :
#   ./get_attachments.py                       # télécharge tout ce qui a une URL (238 documents)
#   ./get_attachments.py --enabled-only        # seulement les documents activés sur la plateforme
#   ./get_attachments.py --dry-run             # affiche sans télécharger
#   ./get_attachments.py --subject الفقه       # une matière seulement
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATT = ROOT / "attachments"
JSON_FILE = ATT / "attachments.json"
PDF_DIR = ATT / "pdf"
INDEX = ATT / "index.tsv"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ar-audio-to-md"}


def fetch_all(api, token, level, limit=100):
    """Port de get_attachements.js : pagine /attachments?level=&page=&limit= avec un Bearer token."""
    page, data, total = 1, [], None
    while True:
        url = f"{api.rstrip('/')}/attachments?level={level}&page={page}&limit={limit}"
        req = urllib.request.Request(url, headers={**UA, "Authorization": f"Bearer {token}",
                                                   "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            js = json.load(r)
        items = js.get("data") or []
        data.extend(items)
        total = js.get("total", total)
        print(f"  page {page} : {len(items)} éléments ({len(data)}/{total})")
        if not items or (total is not None and len(data) >= total):
            break
        page += 1
    return {"data": data, "total": len(data)}


def safe_name(s):
    s = re.sub(r"[\\/:*?\"<>|]+", "-", s)       # caractères interdits sous Windows
    s = re.sub(r"\s+", " ", s).strip(" .")
    return s[:150]


def target_path(item):
    subj = item.get("task", {}).get("subject", {}) or {}
    level = (subj.get("level") or {}).get("name") or "niveau inconnu"
    subject = subj.get("title") or "matière inconnue"
    ext = Path(urllib.parse.urlparse(item["url"]).path).suffix.lower() or ".pdf"
    return PDF_DIR / safe_name(level) / safe_name(subject) / f"{item['id']} - {safe_name(item['title'])}{ext}"


def download(url, target, retries=3):
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                expected = int(r.headers.get("Content-Length") or 0)
                tmp = target.with_suffix(target.suffix + ".part")
                with open(tmp, "wb") as f:
                    while chunk := r.read(1 << 16):
                        f.write(chunk)
            if expected and tmp.stat().st_size != expected:
                raise IOError(f"taille {tmp.stat().st_size} != {expected}")
            tmp.rename(target)
            return target.stat().st_size
        except Exception as e:
            if attempt == retries:
                raise
            print(f"    nouvel essai ({e})")
            time.sleep(2 * attempt)


def main():
    ap = argparse.ArgumentParser(description="Télécharge les PDF des cours listés par la plateforme")
    ap.add_argument("--fetch", action="store_true", help="récupérer la liste depuis l'API (sinon attachments.json)")
    ap.add_argument("--api", help="base de l'API, ex. https://plateforme.exemple/api")
    ap.add_argument("--token", help="jeton Bearer de la plateforme")
    ap.add_argument("--level", type=int, default=1)
    ap.add_argument("--enabled-only", action="store_true")
    ap.add_argument("--subject", help="limiter à cette matière (titre exact)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.fetch:
        if not (args.api and args.token):
            sys.exit("--fetch exige --api et --token")
        print("Récupération de la liste depuis l'API …")
        js = fetch_all(args.api, args.token, args.level)
        JSON_FILE.write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{js['total']} éléments enregistrés dans {JSON_FILE}")
    items = json.load(open(JSON_FILE, encoding="utf-8"))["data"]

    todo = [i for i in items if i.get("url")]
    skipped_nourl = len(items) - len(todo)
    if args.enabled_only:
        todo = [i for i in todo if not i.get("isDisabled")]
    if args.subject:
        todo = [i for i in todo if (i.get("task", {}).get("subject") or {}).get("title") == args.subject]
    print(f"{len(todo)} document(s) à traiter ({skipped_nourl} sans URL ignoré(s)).")

    rows, n_new, n_skip, n_err, total_bytes = [], 0, 0, 0, 0
    for k, item in enumerate(todo, 1):
        target = target_path(item)
        subj = item.get("task", {}).get("subject", {}) or {}
        row = [str(item["id"]), subj.get("title", ""), (subj.get("level") or {}).get("name", ""),
               item["title"], "oui" if not item.get("isDisabled") else "non", item.get("unlockDate") or "",
               str(target.relative_to(ROOT))]
        if target.exists() and target.stat().st_size > 0:
            n_skip += 1
        elif args.dry_run:
            print(f"  [dry-run] {k:3d}/{len(todo)} {target.relative_to(PDF_DIR)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                size = download(item["url"], target)
                total_bytes += size
                n_new += 1
                print(f"  {k:3d}/{len(todo)} {size // 1024:5d} Ko  {target.relative_to(PDF_DIR)}")
            except Exception as e:
                n_err += 1
                row[6] = f"ERREUR {e}"
                print(f"  {k:3d}/{len(todo)} ÉCHEC {item['id']} {item['title']} : {e}")
        rows.append(row)

    if not args.dry_run:
        INDEX.write_text("id\tmatière\tniveau\ttitre\tactivé\tdéblocage\tfichier\n" +
                         "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
    print(f"\nTéléchargés : {n_new} ({total_bytes / 1e6:.1f} Mo), déjà présents : {n_skip}, échecs : {n_err}. Index : {INDEX}")


if __name__ == "__main__":
    main()
