#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Brouillon de page de leçon par le modèle local (Ollama), à partir du texte validé d'un cours.
# Premier étage de l'ingestion : Claude relit ensuite ce brouillon lors de /ingest.
#
# Usage :
#   ./draft_lesson.py "secondBrain/raw/youtube/<dossier du cours>"        # lit texte-ok.md -> écrit brouillon.md
#   ./draft_lesson.py "<dossier>" --brut                                 # test : lit texte.md (non validé)
#   ./draft_lesson.py "<dossier>" --model qwen3.5:27b --ctx 32768
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

OLLAMA = "http://localhost:11434/api/generate"

MATIERES = ("السيرة النبوية · تجويد القرآن · التوحيد والعقيدة · النحو · التزكية والأخلاق · الفقه · "
            "آداب طلب العلم · مصطلح الحديث · أصول الفقه · شرح الحديث · قراءة نافع · الصرف · البلاغة · "
            "القواعد الفقهية · علوم القرآن · مقاصد الشريعة · تاريخ التشريع الإسلامي · الإلحاد المعاصر · "
            "حفظ القرآن · زكاة العلم")

PROMPT = """أنت محرر ويكي علمي دقيق. أمامك تفريغ درس من أكاديمية الإمام الباجي للعلوم الشرعية (المغرب).
المعلومات: العنوان: {title} — المحاضر: {speaker} — التاريخ: {date} — المدة: {duration}.

اكتب مسودة صفحة ويكي لهذا الدرس بالعربية الفصحى **بدون تشكيل** (إلا في الآيات والأحاديث وأقوال العلماء المنقولة حرفيا)، بهذا الهيكل بالضبط وبهذه العناوين:

## الملخص
(5 إلى 10 أسطر)

## المادة
(اختر مادة واحدة من هذه القائمة، أو اكتب "غير محدد": {matieres})

## المحاور
(قائمة نقاط مرتبة حسب تسلسل الدرس، كل نقطة جملة واحدة)

## المفاهيم والمصطلحات
(قائمة: **المصطلح** — تعريف قصير كما شرحه المحاضر. فقط ما شُرح فعلا في الدرس، لا ما ذُكر عرضا)

## الأعلام والكتب
(قائمة الأشخاص والكتب المذكورة، مع كلمة عن سياق الذكر)

## الفوائد
(نقاط للحفظ، كل نقطة جملة واحدة)

## مواضع غير مؤكدة
(مقاطع بدت لك غير واضحة أو بالدارجة أو فيها خطأ تفريغ محتمل، اذكر العبارة كما وردت)

## Résumé (français)
(5 lignes au plus)

قواعد صارمة: لا تخترع أي معلومة أو مرجع أو اسم غير موجود في النص. لا تنقل التفريغ، بل لخّص. لا تكتب أي شيء قبل "## الملخص" ولا بعد الملخص الفرنسي.

النص:
{text}"""


def read_meta(folder):
    meta = {}
    p = folder / "meta.md"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(\w+):\s*\"?(.*?)\"?\s*$", line)
            if m:
                meta[m.group(1)] = m.group(2)
    return meta


def strip_tashkeel(s):
    return re.sub(r"[ً-ْٰـ]", "", s)


def main():
    ap = argparse.ArgumentParser(description="Brouillon de page de leçon par modèle local")
    ap.add_argument("folder", help="dossier du cours dans secondBrain/raw/youtube/")
    ap.add_argument("--brut", action="store_true", help="utiliser texte.md au lieu de texte-ok.md (test)")
    ap.add_argument("--model", default="qwen3.5:27b")
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--out", default="brouillon.md")
    args = ap.parse_args()

    folder = Path(args.folder)
    src = folder / ("texte.md" if args.brut else "texte-ok.md")
    if not src.exists():
        sys.exit(f"Erreur : {src} n'existe pas" + ("" if args.brut else " (le cours n'est pas validé ; --brut pour tester)"))
    text = src.read_text(encoding="utf-8")
    text = re.sub(r"^# .*\n", "", text, count=1)       # titre du fichier
    text = strip_tashkeel(text)                          # le modèle lit mieux sans tashkeel, et la page doit être sans tashkeel
    meta = read_meta(folder)

    prompt = PROMPT.format(title=meta.get("title", folder.name), speaker=meta.get("speaker", "?"),
                           date=meta.get("date", "?"), duration=meta.get("duration", "?"),
                           matieres=MATIERES, text=text)
    req = {"model": args.model, "prompt": prompt, "stream": False,
           "options": {"num_ctx": args.ctx, "temperature": 0.2, "num_predict": 6000}}
    print(f"Modèle {args.model}, {len(text.split())} mots en entrée…")
    t0 = time.time()
    r = urllib.request.urlopen(urllib.request.Request(OLLAMA, data=json.dumps(req).encode(),
                                                      headers={"Content-Type": "application/json"}), timeout=3600)
    d = json.loads(r.read())
    body = d["response"].strip()
    body = re.sub(r"<think>.*?</think>\s*", "", body, flags=re.S)
    i = body.find("## الملخص")
    if i > 0:
        body = body[i:]

    header = (f"---\nsource: {src.name}\nmodel: {args.model}\ngenerated: {time.strftime('%Y-%m-%d %H:%M')}\n"
              f"prompt_tokens: {d.get('prompt_eval_count')}\noutput_tokens: {d.get('eval_count')}\n"
              f"status: brouillon — à relire par /ingest, ne va jamais tel quel dans wiki/\n---\n\n")
    out = folder / args.out
    out.write_text(header + body + "\n", encoding="utf-8")
    print(f"OK en {time.time() - t0:.0f}s : {out} ({d.get('prompt_eval_count')} tokens lus, {d.get('eval_count')} écrits)")


if __name__ == "__main__":
    main()
