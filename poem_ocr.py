#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# OCR d'un متن versifié (PDF mis en page sur deux colonnes d'hémistiches) -> Markdown.
#
# marker/pdftotext mélangent les hémistiches des poèmes. Ici on utilise Surya (le moteur OCR de
# marker) pour obtenir chaque ligne avec ses coordonnées, puis on reconstruit l'ordre :
# même hauteur = même vers, colonne de droite = premier hémistiche (avec le numéro), colonne de
# gauche = second. Les lignes qui traversent la page sont des titres ou de la prose.
#
# Usage :
#   ./poem_ocr.py livre.pdf --categorie "السيرة النبوية" --ouvrage "الأرجوزة المئية" [--pages 2-6]
#   ./poem_ocr.py livre.pdf ... --surya-json resultats.json      # réutiliser une sortie surya_ocr
#
# Sortie : raw/pdfs/<catégorie>/<ouvrage>/<ouvrage> - ج1.md, un tableau | رقم | الشطر الأول | الشطر الثاني |
# par section, titres en ##, marqueurs <!-- ص N -->.
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import txt_to_md as T  # noqa: E402

ROOT = Path(__file__).resolve().parent
SURYA = Path.home() / ".local" / "bin" / "surya_ocr"
NUM = re.compile(r"^\s*[\(\[]?\s*([0-9٠-٩۰-۹]{1,3})\s*[\)\]\-–.ـ]*\s*")
TAGS = re.compile(r"</?(b|i|u|sup|sub)>")
JUNK = re.compile(r"[\U0001F300-\U0001FAFF<>\\]")


def run_surya(pdf, pages, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [str(SURYA), str(pdf), "--output_dir", str(out_dir)]
    if pages:
        cmd += ["--page_range", pages]
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return next(out_dir.glob("*/results.json"))


def clean(t):
    t = JUNK.sub("", TAGS.sub("", t))
    return re.sub(r"\s+", " ", t).strip()


def is_number_only(t):
    return bool(re.fullmatch(r"[\s\(\)\[\]\-–.ـ0-9\u0660-\u0669\u06F0-\u06F9]+", t)) and re.search(r"[0-9\u0660-\u0669\u06F0-\u06F9]", t)


def split_merged(line):
    """Une boîte OCR qui contient les deux hémistiches : couper au plus grand espace entre mots
    (mots triés de droite à gauche), s'il est nettement plus large que les autres."""
    words = [w for w in line.get("words", []) if clean(w.get("text", ""))]
    if len(words) < 4:
        return None
    words.sort(key=lambda w: -w["bbox"][2])
    gaps = [(words[i]["bbox"][0] - words[i + 1]["bbox"][2], i) for i in range(len(words) - 1)]
    g, i = max(gaps)
    med = sorted(x for x, _ in gaps)[len(gaps) // 2]
    if g < 2.5 * max(med, 1) or i < 1 or i > len(words) - 3:
        # pas d'espace net : couper au milieu de la boîte (mots à droite du centre = premier hémistiche)
        cx = (line["bbox"][0] + line["bbox"][2]) / 2
        right = [w for w in words if (w["bbox"][0] + w["bbox"][2]) / 2 >= cx]
        left = [w for w in words if (w["bbox"][0] + w["bbox"][2]) / 2 < cx]
        if len(right) < 2 or len(left) < 2:
            return None
        return (" ".join(clean(w["text"]) for w in right), " ".join(clean(w["text"]) for w in left))
    return (" ".join(clean(w["text"]) for w in words[: i + 1]), " ".join(clean(w["text"]) for w in words[i + 1:]))


def group_rows(lines, tol):
    """Regroupe les lignes OCR par hauteur (centre vertical à tol pixels près)."""
    rows = []
    for l in sorted(lines, key=lambda l: (l["bbox"][1] + l["bbox"][3]) / 2):
        cy = (l["bbox"][1] + l["bbox"][3]) / 2
        if rows and abs(rows[-1]["cy"] - cy) <= tol:
            rows[-1]["lines"].append(l)
            rows[-1]["cy"] = (rows[-1]["cy"] + cy) / 2
        else:
            rows.append({"cy": cy, "lines": [l]})
    return rows


def page_to_blocks(page, min_conf=0.0):
    """Une page Surya -> liste de blocs ("h", texte) | ("p", texte) | ("v", num, hém1, hém2).

    Un vers est reconnu par sa géométrie : les vers d'une page partagent les mêmes colonnes
    (boîte de droite et boîte de gauche aux mêmes abscisses). On repère d'abord le motif de
    deux colonnes le plus fréquent sur la page ; les lignes qui s'y conforment sont des vers,
    ainsi que les lignes numérotées. Le reste est titre (ligne courte) ou prose."""
    W, H = page["image_bbox"][2], page["image_bbox"][3]
    lines = [l for l in page["text_lines"] if clean(l["text"]) and l.get("confidence", 1) >= min_conf
             and 0.07 * H < (l["bbox"][1] + l["bbox"][3]) / 2 < 0.95 * H]
    heights = sorted(l["bbox"][3] - l["bbox"][1] for l in lines) or [20]
    tol = max(6, heights[len(heights) // 2] * 0.45)
    rows = group_rows(lines, tol)

    def prep(row):
        ls = sorted(row["lines"], key=lambda l: -l["bbox"][2])      # de droite à gauche
        texts = [clean(l["text"]) for l in ls]
        num = ""
        if texts and is_number_only(texts[0]):
            num = T.to_ar_digits(re.sub(r"\D", "", T.to_ar_digits(texts[0]))); ls, texts = ls[1:], texts[1:]
        elif texts and re.fullmatch(r"[\s\(\)\[\]\-–.ـ*]+", texts[0]):
            num = "?"; ls, texts = ls[1:], texts[1:]
        if texts:
            m = NUM.match(texts[0])
            if m and not num:
                num = T.to_ar_digits(m.group(1)); texts[0] = NUM.sub("", texts[0], count=1)
        return ls, texts, num

    split_rows = []
    for r in rows:
        if len(r["lines"]) >= 4:
            ls = sorted(r["lines"], key=lambda l: (l["bbox"][1] + l["bbox"][3]) / 2)
            mid = len(ls) // 2
            split_rows.append({"cy": r["cy"], "lines": ls[:mid]}); split_rows.append({"cy": r["cy"], "lines": ls[mid:]})
        else:
            split_rows.append(r)
    prepared = [prep(r) for r in split_rows]
    # motif de deux colonnes dominant : (centre boîte droite, centre boîte gauche) arrondis à 5 % de la largeur
    from collections import Counter
    def key2(ls):
        return (round((ls[0]["bbox"][0] + ls[0]["bbox"][2]) / 2 / W * 20), round((ls[1]["bbox"][0] + ls[1]["bbox"][2]) / 2 / W * 20))
    cnt = Counter(key2(ls) for ls, _, _ in prepared if len(ls) == 2)
    pattern, n_pat = (cnt.most_common(1)[0] if cnt else (None, 0))
    if n_pat < 3:
        pattern = None
    # largeur typique d'une ligne de vers fusionnée (les deux hémistiches dans une boîte)
    merged_span = None
    if pattern:
        spans = [(ls[0]["bbox"][2] - ls[1]["bbox"][0]) / W for ls, _, _ in prepared if len(ls) == 2 and key2(ls) == pattern]
        merged_span = sorted(spans)[len(spans) // 2]

    blocks = []
    for ls, texts, num in prepared:
        if not texts:
            continue
        span = (ls[0]["bbox"][2] - ls[-1]["bbox"][0]) / W
        two_col = len(ls) == 2 and pattern is not None and key2(ls) == pattern
        if two_col or (num and len(ls) >= 2 and span > 0.5):
            blocks.append(("v", num, texts[0], " ".join(texts[1:])))
            continue
        if len(ls) == 1 and (num or (merged_span and abs(span - merged_span) < 0.12 and len(texts[0]) > 25)):
            parts = split_merged(ls[0])
            if parts:
                blocks.append(("v", num, parts[0], parts[1])); continue
            if num:
                blocks.append(("v", num, texts[0], "")); continue
        txt = " ".join(texts)
        center = (ls[0]["bbox"][2] + ls[-1]["bbox"][0]) / 2 / W
        centered = abs(center - 0.5) < 0.08
        if len(txt) <= 60 and span < 0.7 and centered and not num:   # titre : court et centré
            blocks.append(("h", txt))
        elif blocks and blocks[-1][0] == "p":
            blocks[-1] = ("p", blocks[-1][1] + " " + txt)     # prose : lignes consécutives -> paragraphe
        else:
            blocks.append(("p", txt))
    return blocks


def renumber(pages_blocks):
    """Les vers sont numérotés en séquence. Les numéros lus par l'OCR sont peu fiables (٥ lu 0,
    ٦ lu 7…) : on numérote séquentiellement, et on ne suit un saut de l'OCR que si deux vers
    consécutifs le confirment (bit sauté par l'OCR, signalé par une ligne « سقط »). Un * marque
    un numéro OCR différent du numéro attribué."""
    tr = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    verses = [(pi, i) for pi, blocks in enumerate(pages_blocks) for i, b in enumerate(blocks) if b[0] == "v"]
    def ocr_num(b):
        try:
            return int(T.to_ar_digits(b[1]).translate(tr)) if b[1] and b[1] != "?" else None
        except ValueError:
            return None
    expected = 1
    for k, (pi, i) in enumerate(verses):
        b = pages_blocks[pi][i]
        n = ocr_num(b)
        nxt = ocr_num(pages_blocks[verses[k + 1][0]][verses[k + 1][1]]) if k + 1 < len(verses) else None
        if n is not None and 0 < n - expected <= 3 and nxt == n + 1:
            # saut confirmé : des vers manquent dans l'OCR
            pages_blocks[pi].insert(i, ("p", f"(سقط {n - expected} بيت في التعرف الضوئي : الأبيات {T.to_ar_digits(str(expected))}–{T.to_ar_digits(str(n - 1))})"))
            verses = [(p2, j + 1 if p2 == pi and j >= i else j) for p2, j in verses]
            i += 1
            expected = n
        pages_blocks[pi][i] = ("v", T.to_ar_digits(str(expected)) + ("" if n in (None, expected) else "*"), b[2], b[3])
        expected += 1
    return pages_blocks


def render(pages_blocks, ouvrage, first_page=1):
    out = [f"# {ouvrage}\n"]
    in_table = False
    for idx, blocks in enumerate(pages_blocks, start=first_page):
        out.append(f"\n<!-- ص {T.to_ar_digits(str(idx))} -->\n")
        for b in blocks:
            if b[0] == "v":
                if not in_table:
                    out.append("| | الشطر الأول | الشطر الثاني |\n|---|---|---|")
                    in_table = True
                out.append(f"| {b[1]} | {b[2]} | {b[3]} |")
            else:
                if in_table:
                    out.append("")
                    in_table = False
                out.append(("## " + b[1].rstrip(":")) if b[0] == "h" else b[1])
                out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="PDF de poème (deux colonnes) -> Markdown via Surya")
    ap.add_argument("pdf")
    ap.add_argument("--categorie", required=True)
    ap.add_argument("--ouvrage", required=True)
    ap.add_argument("--tome", type=int, default=1)
    ap.add_argument("--pages", help="pages 1-based, ex. 2-6 (défaut : toutes)")
    ap.add_argument("--surya-json", help="résultats.json d'un surya_ocr déjà exécuté")
    ap.add_argument("--min-conf", type=float, default=0.0, help="ignorer les lignes sous cette confiance")
    ap.add_argument("--out-dir", default=str(ROOT / "secondBrain" / "raw" / "pdfs"))
    ap.add_argument("--copier-pdf", action="store_true")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    first = 1
    page_range = None
    if args.pages:
        a, _, b = args.pages.partition("-")
        first = int(a)
        page_range = f"{int(a) - 1}-{int(b or a) - 1}"
    res = Path(args.surya_json) if args.surya_json else run_surya(pdf, page_range, ROOT / "temp" / "surya" / pdf.stem)
    d = json.load(open(res, encoding="utf-8"))
    pages = d[next(iter(d))]
    pages_blocks = renumber([page_to_blocks(p, args.min_conf) for p in pages])
    md = render(pages_blocks, args.ouvrage, first)
    written = T.write_book(md, None, args.out_dir, args.categorie, args.ouvrage, args.tome,
                           original=str(pdf) if args.copier_pdf else None)
    n_v = sum(1 for bl in pages_blocks for b in bl if b[0] == "v")
    n_h = sum(1 for bl in pages_blocks for b in bl if b[0] == "h")
    print(f"{len(pages)} pages, {n_v} vers, {n_h} titres")
    for w in written:
        print(" ->", w)


if __name__ == "__main__":
    main()
