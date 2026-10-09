#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Livre de turath.io (texte saisi, table des matières, pagination de l'imprimé) -> Markdown.
# Option : récupération du tashkeel de l'édition et des notes de bas de page depuis le TXT
# aljam3 (OCR de la même édition), par alignement mot à mot, sans modèle de langue.
#
# Usage :
#   ./turath_to_md.py 133357 --categorie "علوم القرآن"                       # texte turath seul
#   ./turath_to_md.py https://app.turath.io/book/133357 --categorie "علوم القرآن" \
#        --txt 1="temp/… - 01_70102.txt" --txt 2="temp/… - 02_70103.txt"    # + tashkeel et notes
#   ./turath_to_md.py 133357 --categorie … --txt-dir temp                  # fichiers "…0N_….txt" trouvés par tome
#   ./turath_to_md.py 133357 --categorie … --vol 1 --pages 55-65             # test
#
# Sortie dans secondBrain/raw/pdfs/<catégorie>/<ouvrage>/ (mêmes fichiers que txt_to_md.py) :
#   <ouvrage> - جN.md, <ouvrage> - الحواشي - جN.md, الحواشي.md
import argparse
import difflib
import json
import re
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import txt_to_md as T  # noqa: E402

ROOT = Path(__file__).resolve().parent
JSON_URL = "https://files.turath.io/books-v3/{id}.json"
# Les scans référencés par turath (meta.files) sont publiés sur Hugging Face par ieasybooks ;
# aljam3.com sert exactement ces fichiers. TXT = OCR de l'imprimé (avec son tashkeel et ses notes).
HF_URL = "https://huggingface.co/datasets/ieasybooks-org/shamela-waqfeya-library/resolve/main/{kind}/{root}/{name}"
HARAKAT = re.compile(r"[ً-ْٰ]")
TITLE_SPAN = re.compile(r'<span data-type="title" id=toc-(\d+)>(.*?)</span>', re.S)
WORD = re.compile(r"[؀-ۿݐ-ݿ]+")


# ----------------------------------------------------------------------------- turath
def download(url, target):
    """files.turath.io refuse le User-Agent par défaut de Python : on en envoie un de navigateur."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ar-audio-to-md"})
    with urllib.request.urlopen(req, timeout=300) as r, open(target, "wb") as f:
        shutil.copyfileobj(r, f)


def load_book(ident):
    m = re.search(r"(\d+)", ident)
    book_id = m.group(1)
    cache = ROOT / "temp" / "turath" / f"{book_id}.json"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        print(f"Téléchargement {JSON_URL.format(id=book_id)} …")
        download(JSON_URL.format(id=book_id), cache)
    d = json.loads(cache.read_text(encoding="utf-8"))
    meta_raw = d.get("ً", {})
    struct = d.get("٘", {})
    meta = {"id": book_id, "title": meta_raw.get("ٍ", book_id), "info": meta_raw.get("ّ", ""),
            "files": meta_raw.get("ِ", {})}
    toc = struct.get("ٚ", [])                 # [{title, level, page(index 1-based)}]
    return meta, toc, d["pages"]


def bare(w):
    return HARAKAT.sub("", w)


def fetch_scan_files(meta, kinds=("txt",)):
    """Télécharge depuis Hugging Face les fichiers de scan listés par turath (hors couverture).
    Renvoie {kind: [Path, …]} ; les fichiers déjà présents dans temp/turath/<id>/ ne sont pas retéléchargés."""
    files = meta.get("files") or {}
    root, names = files.get("root"), files.get("files", [])
    out = {k: [] for k in kinds}
    if not root or not names:
        return out
    dest = ROOT / "temp" / "turath" / meta["id"]
    dest.mkdir(parents=True, exist_ok=True)
    for entry in names:
        name, _, label = entry.partition("|")
        if label.strip() == "الغلاف":
            continue
        for kind in kinds:
            fname = Path(name).with_suffix("." + kind).name
            target = dest / fname
            if not target.exists():
                url = HF_URL.format(kind=kind, root=urllib.parse.quote(root), name=urllib.parse.quote(fname))
                try:
                    print(f"  téléchargement {kind} {fname} …")
                    download(url, target)
                except Exception as e:  # fichier absent du dépôt, on continue sans
                    print(f"  ! {kind} {fname} indisponible ({e})")
                    continue
            out[kind].append(target)
    return out


def assign_txt_to_volumes(txt_paths, pages, vols):
    """Associe chaque TXT au tome turath dont les pages lui ressemblent le plus."""
    assignment = {}
    samples = {v: [p for p in pages if p["vol"] == str(v)][20:80:5] for v in vols}
    for path in txt_paths:
        txt_pages = [p.strip() for p in T.split_pages(path.read_text(encoding="utf-8"))]
        scores = {v: best_offset(pages, txt_pages, samples[v])[1] for v in vols if samples[v]}
        v = max(scores, key=scores.get)
        if scores[v] >= 0.25 and v not in assignment:
            assignment[v] = path
        else:
            print(f"  ! {path.name} : aucun tome convaincant (meilleur {v} à {scores[v]:.2f}), ignoré")
    return assignment


# ----------------------------------------------------------------------------- tashkeel
def transfer_tashkeel(text, donor_text):
    """Reporte sur `text` (turath, peu vocalisé) le tashkeel des mots de `donor_text` (OCR de
    l'imprimé) alignés par leur forme nue. Un mot n'est modifié que si sa forme nue est identique."""
    if not donor_text:
        return text, 0
    tokens = list(WORD.finditer(text))
    src = [bare(t.group(0)) for t in tokens]
    donors = WORD.findall(donor_text)
    dst = [bare(w) for w in donors]
    sm = difflib.SequenceMatcher(a=src, b=dst, autojunk=False)
    repl = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            continue
        for k in range(i2 - i1):
            dw = donors[j1 + k]
            if HARAKAT.search(dw):
                repl[i1 + k] = dw
    if not repl:
        return text, 0
    out, last = [], 0
    for idx, t in enumerate(tokens):
        if idx in repl:
            out.append(text[last:t.start()]); out.append(repl[idx]); last = t.end()
    out.append(text[last:])
    return "".join(out), len(repl)


def best_offset(tpages, txt_pages, vol_pages_sample):
    """Décalage index-TXT <-> page imprimée : on teste -8..8 sur quelques pages et on garde
    celui qui maximise le recouvrement de mots."""
    best, best_score = 0, -1
    for off in range(-8, 9):
        score = 0
        for p in vol_pages_sample:
            i = p["page"] + off
            if 0 <= i < len(txt_pages):
                a = set(bare(w) for w in WORD.findall(p["text"]))
                b = set(bare(w) for w in WORD.findall(txt_pages[i]))
                if a and b:
                    score += len(a & b) / len(a | b)
        if score > best_score:
            best, best_score = off, score
    return best, best_score / max(1, len(vol_pages_sample))


# ----------------------------------------------------------------------------- conversion
NOTE_SEP = re.compile(r"\n_{5,}\s*\n")
# "١ texte", "(١) texte" ou numérotation continue "٣٧٢ - texte"
TURATH_NOTE = re.compile(r"^\s*\(?([٠-٩0-9]{1,4})\)?\s*[-–ـ]?\s+(\S.*)$")
# appel de note turath : chiffre arabe collé à la fin d'un mot ou d'une ponctuation ("المرسلة١ أخرجاه")
TURATH_CALL = re.compile(r"(?<=[؀-ۿ»\)\]\.،:؟!])([٠-٩]{1,4})(?=[\s،.:؟!»\)]|$)")


def split_turath_notes(text):
    """Page turath -> (corps, [(n, note)]) quand les notes du محقق sont présentes (séparateur _____)."""
    m = NOTE_SEP.search(text)
    if not m:
        return text, []
    body, tail = text[:m.start()], text[m.end():]
    notes, current = [], None
    for ln in tail.splitlines():
        mm = TURATH_NOTE.match(ln)
        if mm:
            if current:
                notes.append(current)
            n = int(T.to_ar_digits(mm.group(1)).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
            current = [n, mm.group(2).strip()]
        elif current and ln.strip():
            current[1] += " " + ln.strip()
    if current:
        notes.append(current)
    return body, notes


def page_to_blocks(text, toc_levels):
    """Texte d'une page turath -> lignes Markdown (titres via la table des matières)."""
    lines = []
    for raw in text.split("\n"):
        s = raw.strip()
        if not s:
            continue
        m = TITLE_SPAN.search(s)
        if m:
            level = toc_levels.get(int(m.group(1)), 2)
            title = m.group(2).strip().rstrip(".:")
            before = s[:m.start()].strip()
            after = s[m.end():].strip(" .")
            if before:
                lines.append(before)
            lines.append("#" * (level + 1) + " " + title)     # niveau 1 -> ##, niveau 2 -> ###
            if after:
                lines.append(after)
        else:
            lines.append(s)
    return lines


def convert_volume(meta, toc_levels, pages, vol, txt_pages, offset, ouvrage, categorie, page_filter=None):
    main_name = f"{ouvrage} - ج{vol}"
    notes_name = f"{ouvrage} - الحواشي - ج{vol}"
    edition = meta["info"].splitlines()[0] if meta["info"] else ""
    tashkeel_src = "aljam3 (OCR de l'édition, transfert mot à mot)" if txt_pages else "turath (texte saisi)"
    out = [f"---\ntitle: \"{ouvrage}\"\nvolume: {vol}\nsource: turath.io/book/{meta['id']}\n"
           f"edition: \"{edition}\"\ntashkeel: {tashkeel_src}\ncategorie: \"{categorie}\"\n---\n",
           f"# {ouvrage} — الجزء {T.to_ar_digits(str(vol))}\n",
           "ترقيم الصفحات موافق للمطبوع. " + meta["info"].replace("\n", " · ") + "\n"]
    notes_out = [f"# {ouvrage} — حواشي الجزء {T.to_ar_digits(str(vol))}\n",
                 f"حواشي المحقق منقولة من النسخة المصورة، مرتبة حسب صفحات [[{main_name}]].\n"]
    n_words_tashkeel, n_notes, n_pages = 0, 0, 0
    for p in pages:
        if p["vol"] != str(vol):
            continue
        if page_filter and p["page"] not in page_filter:
            continue
        label = T.to_ar_digits(str(p["page"]))
        # notes du محقق : celles de turath (texte saisi) si présentes, sinon celles du TXT du scan (OCR)
        text, notes = split_turath_notes(p["text"])
        inline_calls = bool(notes)
        donor, txt_notes = "", []
        if txt_pages is not None:
            i = p["page"] + offset
            if 0 <= i < len(txt_pages):
                lines = [l for l in txt_pages[i].splitlines() if l.strip()]
                if lines and T.PAGE_NUM_LINE.match(lines[-1]):
                    lines.pop()
                body, txt_notes = T.extract_notes(lines)
                donor = "\n".join(body)
        if not notes:
            notes = txt_notes
        text, k = transfer_tashkeel(text, donor)
        n_words_tashkeel += k
        n_pages += 1
        if inline_calls:
            text = TURATH_CALL.sub(lambda m: f" [[{notes_name}#ص {label}|({m.group(1)})]]", text)
        out.append(f"\n<!-- ص {label} -->\n")
        for ln in page_to_blocks(text, toc_levels):
            out.append(ln + "\n")
        if notes and not inline_calls:
            out.append(f"حواشي الصفحة: [[{notes_name}#ص {label}|({T.to_ar_digits(str(len(notes)))})]]\n")
        if notes:
            n_notes += len(notes)
            notes_out.append(f"\n## ص {label}\n")
            for n, t in notes:
                notes_out.append(f"- ({T.to_ar_digits(str(n))}) {t}")
    main_md = "\n".join(out).rstrip() + "\n"
    notes_md = ("\n".join(notes_out).rstrip() + "\n") if n_notes else None
    return main_md, notes_md, n_pages, n_words_tashkeel, n_notes


def main():
    ap = argparse.ArgumentParser(description="Livre turath.io -> Markdown (+ tashkeel et notes depuis le TXT aljam3)")
    ap.add_argument("book", help="id turath ou URL app.turath.io/book/<id>")
    ap.add_argument("--categorie", required=True)
    ap.add_argument("--ouvrage", help="nom de l'ouvrage (défaut : titre turath)")
    ap.add_argument("--txt", action="append", default=[], metavar="VOL=FICHIER", help="TXT aljam3 du tome VOL")
    ap.add_argument("--txt-dir", help="dossier contenant les TXT aljam3, repérés par '0<vol>_' dans le nom")
    ap.add_argument("--sans-auto-txt", action="store_true",
                    help="ne pas télécharger les TXT des scans depuis Hugging Face (par défaut : téléchargés et "
                         "associés aux tomes automatiquement, s'ils existent)")
    ap.add_argument("--pdf", action="store_true", help="télécharger aussi les PDF des scans dans le dossier de l'ouvrage (hors git)")
    ap.add_argument("--vol", type=int, action="append", help="limiter à ce(s) tome(s)")
    ap.add_argument("--pages", help="limiter aux pages imprimées a-b (test)")
    ap.add_argument("--out-dir", default=str(ROOT / "secondBrain" / "raw" / "pdfs"))
    args = ap.parse_args()

    meta, toc, pages = load_book(args.book)
    ouvrage = args.ouvrage or meta["title"]
    toc_levels = {i + 1: t.get("level", 2) for i, t in enumerate(toc)}
    vols = sorted({int(p["vol"]) for p in pages})
    print(f"{meta['title']} : {len(pages)} pages, tomes {vols}, {len(toc)} titres")

    txt_files = {}
    for spec in args.txt:
        v, _, f = spec.partition("=")
        txt_files[int(v)] = Path(f)
    if args.txt_dir:
        for f in Path(args.txt_dir).glob("*.txt"):
            m = re.search(r"\b0?(\d)_\d+\.txt$", f.name) or re.search(r"\b0?(\d)\b.*\.txt$", f.name)
            if m and int(m.group(1)) in vols and int(m.group(1)) not in txt_files:
                txt_files[int(m.group(1))] = f
    if not txt_files and not args.sans_auto_txt:
        got = fetch_scan_files(meta, kinds=("txt", "pdf") if args.pdf else ("txt",))
        if got["txt"]:
            txt_files = assign_txt_to_volumes(got["txt"], pages, vols)
            print("TXT associés aux tomes :", {v: p.name for v, p in sorted(txt_files.items())})
        else:
            print("Aucun TXT de scan disponible : texte turath seul, sans tashkeel ni notes du محقق")
        if args.pdf and got.get("pdf"):
            folder = Path(args.out_dir) / args.categorie / ouvrage
            folder.mkdir(parents=True, exist_ok=True)
            for p in got["pdf"]:
                if not (folder / p.name).exists():
                    shutil.copy2(p, folder / p.name)
    page_filter = None
    if args.pages:
        a, _, b = args.pages.partition("-")
        page_filter = set(range(int(a), int(b or a) + 1))

    for vol in vols:
        if args.vol and vol not in args.vol:
            continue
        txt_pages, offset = None, 0
        if vol in txt_files:
            txt_pages = [p.strip() for p in T.split_pages(txt_files[vol].read_text(encoding="utf-8"))]
            sample = [p for p in pages if p["vol"] == str(vol)][20:60:4]
            offset, sim = best_offset(pages, txt_pages, sample)
            print(f"tome {vol} : TXT {txt_files[vol].name}, {len(txt_pages)} pages, décalage {offset:+d}, similarité {sim:.2f}")
            if sim < 0.3:
                print("  ! similarité faible : vérifier que le TXT correspond bien à ce tome")
        main_md, notes_md, n_pages, n_tk, n_notes = convert_volume(
            meta, toc_levels, pages, vol, txt_pages, offset, ouvrage, args.categorie, page_filter)
        written = T.write_book(main_md, notes_md, args.out_dir, args.categorie, ouvrage, vol)
        print(f"tome {vol} : {n_pages} pages, {n_tk} mots vocalisés transférés, {n_notes} notes")
        for w in written:
            print("  ->", w)


if __name__ == "__main__":
    main()
