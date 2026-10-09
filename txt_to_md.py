#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Convertit le texte d'un livre (export aljam3/turath, pages séparées par PAGE_SEPARATOR)
# en Markdown structuré : hiérarchie de titres, paragraphes reconstitués, marqueurs de page,
# notes de bas de page déplacées dans un fichier séparé relié par [[wikilinks]].
#
# Usage :
#   ./txt_to_md.py "<livre>.txt" --categorie "علوم القرآن" --ouvrage "أحكام القرآن لابن الفرس" --tome 1
#   ./txt_to_md.py "<livre>.txt" ... --out-dir secondBrain/raw/pdfs      # défaut
#   ./txt_to_md.py "<livre>.txt" ... --garder-notes-inline               # notes en fin de page, pas de fichier séparé
#
# Produit dans <out-dir>/<catégorie>/<ouvrage>/ :
#   <ouvrage> - ج<tome>.md            texte principal
#   <ouvrage> - الحواشي - ج<tome>.md   notes de bas de page, une section "## ص N" par page
#   الحواشي.md                         page centrale listant les fichiers de notes de l'ouvrage
# Le même moteur est utilisé par pdf_to_md.py (import des fonctions ci-dessous).
import argparse
import re
import shutil
from pathlib import Path

PAGE_SEP = "PAGE_SEPARATOR"

# Chiffres : latins, arabes-indiens (٠-٩), persans (۰-۹)
DIG = "0-9٠-٩۰-۹"
AR_DIGITS = {**{str(i): chr(0x0660 + i) for i in range(10)},
             **{chr(0x06F0 + i): chr(0x0660 + i) for i in range(10)}}

NOTE_START = re.compile(rf"^\s*\(?([{DIG}]{{1,2}})\)\s*(\S.*)$")       # "(١) texte de la note"
INLINE_NOTE = re.compile(rf"\(\s*([{DIG}]{{1,2}})\s*\)")                 # "(٣)" dans le corps
PAGE_NUM_LINE = re.compile(rf"^\s*[{DIG}]{{1,4}}\s*$")                   # ligne = numéro de page
JUNK_LINE = re.compile(rf"^\s*([{DIG}]{{1,2}}\)?|\(?[{DIG}]{{1,2}}\)?\.?|[،,.:;·•\-_=*!«»\"'()\[\]]+)\s*$")
SENTENCE_END = re.compile(r"[.؟!:»\]﴾]\s*$")
AYAH_HEAD = re.compile(r"^(?:[-–•]\s*)?(?:و)?(قول[هُ]?\s*تعالى\s*:?\s*.*?\[[^\]]{2,40}\]\s*\.?)\s*(.*)$")
HEAD_WORDS = re.compile(r"^(سورة|باب|فصل|كتاب|مسألة|المسألة|فائدة|تنبيه|خاتمة|مقدمة|تقديم|ترجمة|المبحث|المطلب|الفرع|القسم|النوع)\b")
NUMBERED_HEAD = re.compile(rf"^\s*[{DIG}]{{1,2}}\s*[ـ\-–.)]\s+\S")       # "١ ـ النسخة الأولى:"
STAR_HEAD = re.compile(r"^\s*[\*#]\s+\S")                               # "* النسخ المعتمدة"


def to_ar_digits(s):
    return "".join(AR_DIGITS.get(c, c) for c in s)


def split_pages(text):
    return [p.strip("\n") for p in text.split(PAGE_SEP)]


def extract_notes(lines):
    """Sépare le corps des notes de bas de page. Les notes = du dernier '(١) texte' jusqu'à la fin,
    si les numéros qui suivent sont croissants."""
    start = None
    for i in range(len(lines) - 1, -1, -1):
        m = NOTE_START.match(lines[i])
        if m and to_ar_digits(m.group(1)) == "١":
            start = i
            break
    if start is None:
        return lines, []
    body, notes_lines = lines[:start], lines[start:]
    # Plusieurs notes peuvent être collées sur une même ligne : "(٢) … (٣) … (٤) …" -> les séparer
    split_lines = []
    for ln in notes_lines:
        parts = re.split(rf"(?=\(\s*[{DIG}]{{1,2}}\s*\)\s*\S)", ln)
        split_lines.extend(p for p in parts if p.strip())
    notes_lines = split_lines
    # Regrouper les lignes de notes : une note peut s'étaler sur plusieurs lignes
    notes, current = [], None
    expected = 1
    for ln in notes_lines:
        m = NOTE_START.match(ln)
        if m:
            n = int(to_ar_digits(m.group(1)).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
            if n == expected or (current is None and n == 1):
                if current:
                    notes.append(current)
                current = [n, m.group(2).strip()]
                expected = n + 1
                continue
        if current:
            current[1] += " " + ln.strip()
        else:
            body.append(ln)
    if current:
        notes.append(current)
    return body, notes


def clean_body_lines(lines):
    out = []
    for ln in lines:
        s = ln.strip()
        if not s or JUNK_LINE.match(s):
            continue
        out.append(s)
    return out


def strip_tashkeel(s):
    return re.sub(r"[ً-ْٰـ]", "", s)


def classify_line(s):
    """Renvoie (niveau, titre, reste) si la ligne commence un titre, sinon None.
    La reconnaissance se fait sur une copie sans tashkeel, la sortie garde l'original."""
    starred = bool(STAR_HEAD.match(s))                      # titre signalé par marker ("* …")
    core = re.sub(r"^\s*[\*#]\s+", "", s) if starred else s
    plain = re.sub(r"^[\s﴿(\-–•]+", "", strip_tashkeel(core))   # ignorer la ponctuation parasite en tête
    if HEAD_WORDS.match(plain) and len(plain) <= 60 and not SENTENCE_END.search(plain[:-1] if plain.endswith(":") else plain):
        return 2 if plain.startswith("سورة") else 3, core.rstrip(":"), ""
    m = AYAH_HEAD.match(plain)
    if m and len(m.group(1)) <= 160 and "." not in m.group(1)[:-2]:
        # couper l'original après la référence [سورة : آية]
        cut = core.find("]") + 1
        head, rest = core[:cut], core[cut:]
        head = re.sub(r"^[\s﴿(\-–•]+", "", head)
        rest = re.sub(r"^\s*\.?\s*", "", rest)
        return 3, head, rest
    if starred and len(core) <= 80:
        return 4, core.rstrip(":"), ""
    if NUMBERED_HEAD.match(s) and len(s) <= 60 and (s.endswith(":") or len(s.split()) <= 6):
        return 4, s.rstrip(":"), ""
    return None


PAGE_MARK = "\x00PAGE\x00"   # ligne spéciale insérée entre les pages


def build_paragraphs(lines):
    """Reconstitue paragraphes et titres. `lines` couvre tout le livre, avec des lignes
    PAGE_MARK + label entre les pages : un paragraphe coupé par un changement de page
    continue, le marqueur de page est inséré dans le texte."""
    blocks = []   # ("h", niveau, texte) | ("p", texte) | ("page", label)
    buf = []

    def flush():
        if buf:
            blocks.append(("p", " ".join(buf)))
            buf.clear()

    for s in lines:
        if s.startswith(PAGE_MARK):
            label = s[len(PAGE_MARK):]
            if buf:
                buf.append(f"<!-- ص {label} -->")
            else:
                blocks.append(("page", label))
            continue
        c = classify_line(s)
        if c:
            flush()
            level, title, rest = c
            blocks.append(("h", level, title))
            if rest:
                buf.append(rest)
            continue
        buf.append(s)
        if SENTENCE_END.search(s):
            flush()
    flush()
    return blocks


def link_notes(text, notes_file, page):
    """Remplace (٣) dans le corps par un wikilink vers la section de la page dans le fichier de notes."""
    def repl(m):
        n = to_ar_digits(m.group(1))
        return f"[[{notes_file}#ص {page}|({n})]]"
    return INLINE_NOTE.sub(repl, text)


def convert(text, ouvrage, tome, notes_inline=False):
    """Renvoie (markdown_principal, markdown_notes)."""
    main_name = f"{ouvrage} - ج{tome}"
    notes_name = f"{ouvrage} - الحواشي - ج{tome}"
    out = [f"# {ouvrage} — الجزء {to_ar_digits(str(tome))}\n"]
    notes_out = [f"# {ouvrage} — حواشي الجزء {to_ar_digits(str(tome))}\n",
                 f"الحواشي مرتبة حسب صفحات [[{main_name}]].\n"]
    pages = split_pages(text)
    all_lines = []            # corps de tout le livre, pages séparées par PAGE_MARK
    notes_by_page = {}        # label -> [(n, texte)]
    for idx, page in enumerate(pages, start=1):
        lines = [l for l in page.splitlines()]
        # numéro de page imprimé : dernière (ou première) ligne composée uniquement de chiffres
        printed = None
        while lines and not lines[-1].strip():
            lines.pop()
        if lines and PAGE_NUM_LINE.match(lines[-1]):
            printed = to_ar_digits(lines.pop().strip())
        elif lines and PAGE_NUM_LINE.match(lines[0]):
            printed = to_ar_digits(lines.pop(0).strip())
        page_label = printed or to_ar_digits(str(idx))
        body, notes = extract_notes(lines)
        body = clean_body_lines(body)
        if not body and not notes:
            continue
        all_lines.append(PAGE_MARK + page_label)
        # les appels de note du corps sont liés à la page où ils apparaissent
        all_lines.extend(b if notes_inline else link_notes(b, notes_name, page_label) for b in body)
        if notes:
            notes_by_page[page_label] = notes

    current_page = None
    for b in build_paragraphs(all_lines):
        if b[0] == "page":
            if notes_inline and current_page in notes_by_page:
                out.append("")
                for n, t in notes_by_page[current_page]:
                    out.append(f"> ({to_ar_digits(str(n))}) {t}")
            current_page = b[1]
            out.append(f"\n<!-- ص {current_page} -->\n")
        elif b[0] == "h":
            out.append("#" * b[1] + " " + b[2] + "\n")
        else:
            out.append(b[1] + "\n")
            for m in re.finditer(r"<!-- ص (\S+) -->", b[1]):
                current_page = m.group(1)
    if not notes_inline:
        for label, notes in notes_by_page.items():
            notes_out.append(f"\n## ص {label}\n")
            for n, t in notes:
                notes_out.append(f"- ({to_ar_digits(str(n))}) {t}")
    main_md = "\n".join(out).rstrip() + "\n"
    notes_md = None if notes_inline else "\n".join(notes_out).rstrip() + "\n"
    return main_md, notes_md


def write_book(main_md, notes_md, out_dir, categorie, ouvrage, tome, original=None):
    folder = Path(out_dir) / categorie / ouvrage
    folder.mkdir(parents=True, exist_ok=True)
    main_path = folder / f"{ouvrage} - ج{tome}.md"
    main_path.write_text(main_md, encoding="utf-8")
    written = [main_path]
    if notes_md:
        notes_path = folder / f"{ouvrage} - الحواشي - ج{tome}.md"
        notes_path.write_text(notes_md, encoding="utf-8")
        written.append(notes_path)
        # page centrale des notes de l'ouvrage
        central = folder / "الحواشي.md"
        entries = sorted(p.stem for p in folder.glob(f"{ouvrage} - الحواشي - ج*.md"))
        central.write_text(f"# {ouvrage} — الحواشي\n\nفهرس ملفات الحواشي، جزءا جزءا :\n\n" +
                           "\n".join(f"- [[{e}]]" for e in entries) + "\n", encoding="utf-8")
        written.append(central)
    if original:
        dest = folder / Path(original).name
        if not dest.exists():
            shutil.copy2(original, dest)
    return written


def main():
    ap = argparse.ArgumentParser(description="Texte de livre (PAGE_SEPARATOR) -> Markdown structuré")
    ap.add_argument("input")
    ap.add_argument("--categorie", required=True, help="matière / catégorie (nom du sous-dossier)")
    ap.add_argument("--ouvrage", required=True, help="nom de l'ouvrage (sous-dossier et préfixe des fichiers)")
    ap.add_argument("--tome", type=int, default=1)
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parent / "secondBrain" / "raw" / "pdfs"))
    ap.add_argument("--garder-notes-inline", action="store_true", help="notes en citation sous chaque page")
    ap.add_argument("--copier-original", action="store_true", help="copier le .txt d'origine dans le dossier")
    args = ap.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    main_md, notes_md = convert(text, args.ouvrage, args.tome, notes_inline=args.garder_notes_inline)
    written = write_book(main_md, notes_md, args.out_dir, args.categorie, args.ouvrage, args.tome,
                         original=args.input if args.copier_original else None)
    n_pages = main_md.count("<!-- ص ")
    n_heads = sum(1 for l in main_md.splitlines() if l.startswith("#"))
    n_notes = notes_md.count("\n- (") if notes_md else main_md.count("\n> (")
    print(f"{n_pages} pages, {n_heads} titres, {n_notes} notes")
    for w in written:
        print(" ->", w)


if __name__ == "__main__":
    main()
