#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Convertit un livre scanné (PDF image) en Markdown structuré, en fusionnant deux sources :
#   1. marker-pdf (OCR Surya, GPU)        -> structure : titres, paragraphes, notes, mise en page
#   2. le texte TXT d'aljam3 (si fourni)   -> second avis mot à mot, aligné page par page
# puis réconciliation page par page par le modèle local (Ollama), puis le même post-traitement
# que txt_to_md.py (marqueurs de page, notes dans un fichier séparé, hiérarchie des titres).
#
# Usage :
#   ./pdf_to_md.py livre.pdf --txt livre.txt --categorie "علوم القرآن" --ouvrage "أحكام القرآن لابن الفرس" --tome 1
#   ./pdf_to_md.py livre.pdf --pages 58-62 ...            # test sur quelques pages
#   ./pdf_to_md.py livre.pdf --sans-llm ...               # marker seul (ou marker + txt sans fusion)
#   ./pdf_to_md.py livre.pdf --marker-md deja_produit.md  # réutiliser une sortie marker existante
#
# Étapes et coûts (RTX 5090) : marker ≈ 10 s/page, réconciliation ≈ 10-20 s/page.
# Le résultat intermédiaire de marker est gardé dans temp/marker/<pdf>/ pour ne pas le refaire.
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import txt_to_md as T  # noqa: E402

ROOT = Path(__file__).resolve().parent
MARKER = Path.home() / ".local" / "bin" / "marker_single"
OLLAMA = "http://localhost:11434/api/generate"

RECONCILE_PROMPT = """أنت مدقق نصوص عربية تراثية. أمامك نسختان لنفس الصفحة من كتاب مطبوع، كلتاهما من التعرف الضوئي (OCR) وفيهما أخطاء مختلفة.

النسخة (أ) من برنامج يحفظ البنية (العناوين بـ #، الفقرات، الحواشي في الأسفل) لكنه يخطئ أحيانا في الكلمات والأرقام.
النسخة (ب) نص خام بلا بنية، لكنه غالبا أدق في الكلمات والتشكيل والأرقام.

اكتب الصفحة مصححة بصيغة Markdown بهذه القواعد:
- احتفظ ببنية (أ): العناوين بـ ## أو ### كما هي، الفقرات، الترتيب.
- صحح الكلمات والأرقام بالاعتماد على (ب) عند الاختلاف. التشكيل: انقل ما هو موجود في إحدى النسختين فقط، ولا تضف حركات على كلمة غير مشكولة فيهما (الكتاب مشكول جزئيا، والمطلوب نقله كما طُبع). الآيات بين ﴿ ﴾ ومرجعها بين [ ].
- أرقام الحواشي داخل النص تبقى بالشكل (١) (٢)...
- الحواشي في نهاية الصفحة، كل حاشية في سطر يبدأ بـ (١) ثم نصها، بلا عنوان قبلها.
- لا تحذف شيئا موجودا في النسختين، ولا تضف شيئا غير موجود فيهما، ولا تعلّق، ولا تكرر سطرا.
- إذا كانت (ب) فارغة فاعتمد (أ) وحدها.

=== النسخة (أ) ===
{a}

=== النسخة (ب) ===
{b}

=== الصفحة المصححة ===
"""


def run_marker(pdf, pages, out_dir):
    """Lance marker avec sortie paginée ; renvoie le chemin du .md produit."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [str(MARKER), str(pdf), "--output_dir", str(out_dir), "--output_format", "markdown",
           "--paginate_output", "--force_ocr"]
    if pages:
        cmd += ["--page_range", pages]
    print("$", " ".join(cmd))
    t0 = time.time()
    subprocess.run(cmd, check=True)
    md = out_dir / pdf.stem / f"{pdf.stem}.md"      # marker écrit <out_dir>/<nom>/<nom>.md
    if not md.exists():
        md = next(p for p in out_dir.glob("*/*.md") if p.parent.name != "reconciled")
    print(f"marker : {time.time() - t0:.0f}s -> {md}")
    return md


def split_marker_pages(md_text):
    """La sortie paginée de marker sépare les pages par une ligne '{N}----…' (N = index 0-based)."""
    pages = {}
    chunks = re.split(r"\n?\{(\d+)\}-{20,}\n?", md_text)
    # chunks = [avant, N1, texte1, N2, texte2, ...]
    for i in range(1, len(chunks) - 1, 2):
        pages[int(chunks[i])] = chunks[i + 1].strip()
    if not pages and md_text.strip():       # pas de pagination : tout sur la page 0
        pages[0] = md_text.strip()
    return pages


def marker_to_plain(md):
    """Ramène le Markdown de marker vers le format 'texte brut' attendu par txt_to_md :
    une ligne par bloc, titres repérés par '* ' pour être reconnus, notes '(١) …' en fin."""
    lines = []
    for ln in md.splitlines():
        s = ln.strip()
        if not s or s.startswith("![](") or s.startswith("<span id="):
            continue
        s = re.sub(r"<sup>\(?</sup>\s*(?:\(?)([\d٠-٩۰-۹]{1,2})\)?", r"(\1)", s)   # <sup>(</sup>١) -> (١)
        s = re.sub(r"<sup>([\d٠-٩۰-۹]{1,2})</sup>", r"(\1)", s)
        s = re.sub(r"</?(b|i|u|sup|sub|span|br)[^>]*>", "", s)
        s = s.replace("\\*", "*").replace("\\_", "_")
        m = re.match(r"^#{1,6}\s+(.*)$", s)
        if m:
            s = "* " + m.group(1).strip()
        lines.append(s)
    return "\n".join(lines)


HARAKAT = re.compile(r"[ً-ْٰ]")


def guard_tashkeel(out, *sources):
    """Le modèle a tendance à vocaliser entièrement. On ne garde le tashkeel d'un mot que si ce
    mot apparaît vocalisé dans au moins une des sources (OCR marker ou texte aljam3)."""
    allowed = set()
    for src in sources:
        for w in re.findall(r"\S+", src or ""):
            if HARAKAT.search(w):
                allowed.add(HARAKAT.sub("", w))
    def fix(m):
        w = m.group(0)
        if not HARAKAT.search(w):
            return w
        bare = HARAKAT.sub("", w)
        return w if bare in allowed else bare
    return re.sub(r"\S+", fix, out)


def reconcile(a, b, model, ctx):
    # think=False : sans cela, qwen3.5 consomme tout le budget de sortie en réflexion et rend une page vide
    req = {"model": model, "prompt": RECONCILE_PROMPT.format(a=a, b=b or "(فارغة)"), "stream": False,
           "think": False, "options": {"num_ctx": ctx, "temperature": 0.1, "num_predict": 4000}}
    r = urllib.request.urlopen(urllib.request.Request(OLLAMA, data=json.dumps(req).encode(),
                                                      headers={"Content-Type": "application/json"}), timeout=1800)
    d = json.loads(r.read())
    out = re.sub(r"<think>.*?</think>\s*", "", d["response"], flags=re.S).strip()
    out = re.sub(r"^=+.*?=+\s*", "", out)
    return out


def parse_pages_arg(s):
    """'58-62,70' -> liste d'index 0-based pour marker (page 1 du PDF = index 0)."""
    idx = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            idx.extend(range(int(a) - 1, int(b)))
        else:
            idx.append(int(part) - 1)
    return idx


def main():
    ap = argparse.ArgumentParser(description="PDF scanné -> Markdown structuré (marker + txt + modèle local)")
    ap.add_argument("pdf")
    ap.add_argument("--txt", help="texte aljam3 du même tome (pages séparées par PAGE_SEPARATOR)")
    ap.add_argument("--pages", help="pages du PDF à traiter, 1-based, ex. 58-62,70 (défaut : tout)")
    ap.add_argument("--categorie", required=True)
    ap.add_argument("--ouvrage", required=True)
    ap.add_argument("--tome", type=int, default=1)
    ap.add_argument("--out-dir", default=str(ROOT / "secondBrain" / "raw" / "pdfs"))
    ap.add_argument("--marker-md", help="réutiliser une sortie marker paginée existante")
    ap.add_argument("--sans-llm", action="store_true", help="pas de réconciliation par modèle local")
    ap.add_argument("--model", default="qwen3.5:27b")
    ap.add_argument("--ctx", type=int, default=16384)
    ap.add_argument("--garder-notes-inline", action="store_true")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    page_idx = parse_pages_arg(args.pages) if args.pages else None
    marker_range = ",".join(str(i) for i in page_idx) if page_idx else None

    # 1. marker
    if args.marker_md:
        marker_md = Path(args.marker_md)
    else:
        marker_md = run_marker(pdf, marker_range, ROOT / "temp" / "marker" / pdf.stem)
    mpages = split_marker_pages(marker_md.read_text(encoding="utf-8"))
    print(f"marker : {len(mpages)} page(s) : {sorted(mpages)[:5]}…")

    # 2. texte aljam3 aligné par index de page (PAGE_SEPARATOR n° k sépare la page k de la page k+1)
    tpages = {}
    if args.txt:
        for i, p in enumerate(T.split_pages(Path(args.txt).read_text(encoding="utf-8"))):
            tpages[i] = p.strip()
        print(f"txt : {len(tpages)} pages")

    # 3. réconciliation page par page -> pseudo-TXT (PAGE_SEPARATOR entre les pages)
    merged_pages = []
    order = sorted(mpages) if page_idx is None else [i for i in page_idx if i in mpages]
    cache = ROOT / "temp" / "marker" / pdf.stem / "reconciled"     # une page réconciliée n'est jamais recalculée
    cache.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for n, i in enumerate(order, 1):
        a = marker_to_plain(mpages[i])
        b = tpages.get(i, "")
        cached = cache / f"{i + 1:04d}.md"
        if args.sans_llm or not a.strip():
            page = a if a.strip() else b
        elif cached.exists():
            page = guard_tashkeel(cached.read_text(encoding="utf-8"), a, b)
        else:
            page = reconcile(a, b, args.model, args.ctx)
            page = marker_to_plain(page)      # re-normaliser (titres '* ', notes '(١)')
            if page.strip():
                cached.write_text(page, encoding="utf-8")
            page = guard_tashkeel(page, a, b)
        page += f"\n{i + 1}"                 # numéro de page imprimé = index + 1 (hypothèse : pas de pages liminaires non numérotées)
        merged_pages.append(page)
        print(f"  page {i + 1} ({n}/{len(order)}) {len(page)} car., {time.time() - t0:.0f}s")
    pseudo_txt = ("\n" + T.PAGE_SEP + "\n").join(merged_pages)

    # 4. post-traitement commun et écriture
    main_md, notes_md = T.convert(pseudo_txt, args.ouvrage, args.tome, notes_inline=args.garder_notes_inline)
    written = T.write_book(main_md, notes_md, args.out_dir, args.categorie, args.ouvrage, args.tome)
    print(f"{main_md.count('<!-- ص ')} pages, {sum(1 for l in main_md.splitlines() if l.startswith('#'))} titres")
    for w in written:
        print(" ->", w)


if __name__ == "__main__":
    main()
