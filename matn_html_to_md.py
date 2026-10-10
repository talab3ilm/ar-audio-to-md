#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Métn versifié publié en HTML (takw.in/reader.php?matn=…) -> Markdown, même format que poem_ocr.py :
# tableau | رقم | الشطر الأول | الشطر الثاني |, titres en ##. Texte saisi et vocalisé, sans OCR.
#
# Usage :
#   ./matn_html_to_md.py "https://takw.in/reader.php?matn=…" --categorie "السيرة النبوية" --ouvrage "الأرجوزة المئية"
#   ./matn_html_to_md.py page.html --categorie … --ouvrage …
import argparse
import html
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import txt_to_md as T  # noqa: E402

ROOT = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ar-audio-to-md"}


def fetch(src):
    if re.match(r"^https?://", src):
        req = urllib.request.Request(src, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="ignore")
    return Path(src).read_text(encoding="utf-8", errors="ignore")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_takwin(h):
    """Renvoie (titre, blocs) ; blocs = ("h", texte) | ("p", texte) | ("v", "", sadr, ajiz).
    Gère les métons versifiés (div.bayt) et en prose (lignes séparées par <br>, titres en <center>,
    termes en <b> rendus en gras)."""
    title = strip_tags(re.search(r"<title>(.*?)</title>", h, re.S).group(1)) if "<title>" in h else ""
    body = h.split('<div id="cont">', 1)[1] if '<div id="cont">' in h else h
    body = body.split("<footer", 1)[0]
    body = re.sub(r'<span class="indenter"></span>', "", body)
    blocks = []
    # découpage en éléments de premier niveau, dans l'ordre
    pattern = re.compile(r'<center>(.*?)</center>|<div class="bayt">(.*?)</div>\s*</div>|<div class="basmalah">(.*?)</div>|((?:<(?!center|div|br)[^>]*>)*[^<]+(?:<(?!center|div|br)[^>]*>[^<]*)*)(?:<br\s*/?>|$)', re.S)
    for m in pattern.finditer(body):
        if m.group(1) is not None:
            t = strip_tags(m.group(1))
            if t:
                blocks.append(("h", t))
        elif m.group(2) is not None:
            sadr = re.search(r'class="bayt-sadr">(.*?)</div>', m.group(2), re.S)
            ajiz = re.search(r'class="bayt-ajiz">(.*?)(?:</div>|$)', m.group(2), re.S)
            blocks.append(("v", "", strip_tags(sadr.group(1)) if sadr else "", strip_tags(ajiz.group(1)) if ajiz else ""))
        elif m.group(3) is not None:
            blocks.append(("p", strip_tags(m.group(3))))
        elif m.group(4) is not None:
            frag = re.sub(r"</?b>", "**", m.group(4))
            t = html.unescape(re.sub(r"<[^>]+>", "", frag)).strip()
            t = re.sub(r"\*\*\s*:", "**:", t)
            if t:
                blocks.append(("p", t))
    return title, blocks


def render(blocks, ouvrage, source):
    out = [f"---\ntitle: \"{ouvrage}\"\nsource: {source}\ntashkeel: texte saisi (source HTML)\n---\n", f"# {ouvrage}\n"]
    n = 0
    in_table = False
    for b in blocks:
        if b[0] == "v":
            if not in_table:
                out.append("| | الشطر الأول | الشطر الثاني |\n|---|---|---|")
                in_table = True
            n += 1
            out.append(f"| {T.to_ar_digits(str(n))} | {b[2]} | {b[3]} |")
        else:
            if in_table:
                out.append("")
                in_table = False
            out.append(("## " + b[1]) if b[0] == "h" else b[1])
            out.append("")
    return "\n".join(out).rstrip() + "\n", n


def main():
    ap = argparse.ArgumentParser(description="Métn HTML (takw.in) -> Markdown")
    ap.add_argument("source", help="URL takw.in ou fichier HTML")
    ap.add_argument("--categorie", required=True)
    ap.add_argument("--ouvrage", required=True)
    ap.add_argument("--tome", type=int, default=1)
    ap.add_argument("--out-dir", default=str(ROOT / "secondBrain" / "raw" / "pdfs"))
    args = ap.parse_args()
    h = fetch(args.source)
    title, blocks = parse_takwin(h)
    md, n = render(blocks, args.ouvrage, args.source)
    written = T.write_book(md, None, args.out_dir, args.categorie, args.ouvrage, args.tome)
    print(f"{title} : {n} vers, {sum(1 for b in blocks if b[0] == 'h')} titres")
    for w in written:
        print(" ->", w)


if __name__ == "__main__":
    main()
