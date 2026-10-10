#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Extrait la couche texte d'un PDF (pdftotext) page par page, au format "PAGE_SEPARATOR" utilisé
# par txt_to_md.py / pdf_to_md.py (--txt). Sert de second avis fiable à la réconciliation quand le
# PDF a un vrai texte (même stocké en formes de présentation arabes, normalisées ici).
#
# Usage :
#   ./pdf_text_layer.py livre.pdf [--out livre.txt] [--pages 9-95]
#   ./pdf_text_layer.py livre.pdf --evaluer        # affiche seulement la part de pages avec du texte arabe
import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

PAGE_SEP = "PAGE_SEPARATOR"
BIDI = re.compile(r"[‎‏‪-‮⁦-⁩﻿]")
ARABIC = re.compile(r"[؀-ۿ]")
LATIN_RUN = re.compile(r"(?<![A-Za-z])[A-Za-z]{1,3}(?:\s+[A-Za-z]{1,3}){2,}(?![A-Za-z])")   # glyphes d'une police coranique sans Unicode


def page_count(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 0


def extract_page(pdf, n):
    out = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), str(pdf), "-"], capture_output=True, text=True).stdout
    t = unicodedata.normalize("NFKC", out)
    t = BIDI.sub("", t)
    t = LATIN_RUN.sub(" ﴿…﴾ ", t)            # citation coranique illisible dans la couche texte
    lines = [re.sub(r"\s+", " ", l).strip() for l in t.splitlines()]
    return "\n".join(l for l in lines if l)


def arabic_words(t):
    return sum(1 for w in t.split() if ARABIC.search(w))


def main():
    ap = argparse.ArgumentParser(description="Couche texte d'un PDF -> TXT paginé (PAGE_SEPARATOR)")
    ap.add_argument("pdf")
    ap.add_argument("--out")
    ap.add_argument("--pages", help="a-b (1-based)")
    ap.add_argument("--evaluer", action="store_true")
    args = ap.parse_args()
    pdf = Path(args.pdf)
    n = page_count(pdf)
    a, b = 1, n
    if args.pages:
        x, _, y = args.pages.partition("-"); a, b = int(x), int(y or x)
    pages = [extract_page(pdf, i) for i in range(a, b + 1)]
    with_text = sum(1 for p in pages if arabic_words(p) >= 40)
    share = with_text / max(1, len(pages))
    if args.evaluer:
        print(f"{with_text}/{len(pages)} pages avec au moins 40 mots arabes ({share:.0%})")
        sys.exit(0 if share >= 0.3 else 1)
    out = Path(args.out) if args.out else pdf.with_suffix(".txt")
    # les pages sont écrites avec leur index 1-based en dernière ligne, comme les TXT aljam3
    out.write_text(("\n" + PAGE_SEP + "\n").join(f"{p}\n{i}" for i, p in zip(range(a, b + 1), pages)) + "\n", encoding="utf-8")
    print(f"{len(pages)} pages, {with_text} avec texte arabe ({share:.0%}) -> {out}")


if __name__ == "__main__":
    main()
