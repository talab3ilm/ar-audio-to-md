#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Calendrier .ics des documents de cours de la plateforme (date de déblocage de chaque document).
#
# Usage :
#   ./make_calendar.py                      # attachments/attachments.json -> attachments/cours_albaji.ics
#   ./make_calendar.py --group-by-day       # un événement par jour et par matière (liste des documents dans la description)
#   ./make_calendar.py --out mon_fichier.ics
#
# Événements sur la journée (sans heure) : la plateforme ne donne que la date. Importable dans
# Google Agenda, Outlook, Apple Calendar, Thunderbird.
import argparse
import datetime as dt
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATT = ROOT / "attachments"
API = "https://baji.irchademy.irchad-backends.com/api"
TOKEN_FILE = ATT / "token.txt"
# Ramadan 1448 (dates astronomiques prévues, à un jour près selon l'observation)
RAMADAN = (dt.date(2027, 2, 8), dt.date(2027, 3, 9))


def period(uid, start, end_inclusive, summary, description, stamp):
    """Événement sur plusieurs jours (DTEND exclusif)."""
    lines = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}",
             f"DTSTART;VALUE=DATE:{start:%Y%m%d}", f"DTEND;VALUE=DATE:{end_inclusive + dt.timedelta(days=1):%Y%m%d}",
             f"SUMMARY:{esc(summary)}", f"DESCRIPTION:{esc(description)}", "CATEGORIES:السنة الدراسية",
             "TRANSP:TRANSPARENT", "END:VEVENT"]
    return "\r\n".join(fold(l) for l in lines)


def fetch_group():
    """Groupe actif de l'étudiant (dates de l'année et des phases) ; None sans jeton ou en cas d'erreur."""
    if not TOKEN_FILE.exists():
        return None
    token = re.sub(r"^\s*(Authorization\s*:\s*)?(Bearer\s+)?", "", TOKEN_FILE.read_text().strip(), flags=re.I).strip("\"' ")
    req = urllib.request.Request(f"{API}/groups/active/me", headers={
        "Authorization": f"Bearer {token}", "Accept": "application/json", "x-tenant-key": "baji",
        "Origin": "https://dashboard.albajiacademy.com", "User-Agent": "Mozilla/5.0 ar-audio-to-md"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f"  (groupe actif non récupéré : {e})")
        return None


def esc(s):
    """Échappement ICS (RFC 5545) : antislash, virgule, point-virgule, retours à la ligne."""
    return (str(s).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    """Lignes de 75 octets max, continuation par espace (RFC 5545)."""
    out, b = [], line.encode("utf-8")
    while len(b) > 75:
        cut = 75
        while cut > 0 and (b[cut] & 0xC0) == 0x80:   # ne pas couper un caractère UTF-8
            cut -= 1
        out.append(b[:cut].decode("utf-8"))
        b = b" " + b[cut:]
    out.append(b.decode("utf-8"))
    return "\r\n".join(out)


def event(uid, date, summary, description, category, stamp):
    end = date + dt.timedelta(days=1)
    lines = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}",
             f"DTSTART;VALUE=DATE:{date:%Y%m%d}", f"DTEND;VALUE=DATE:{end:%Y%m%d}",
             f"SUMMARY:{esc(summary)}", f"DESCRIPTION:{esc(description)}",
             f"CATEGORIES:{esc(category)}", "TRANSP:TRANSPARENT", "END:VEVENT"]
    return "\r\n".join(fold(l) for l in lines)


def main():
    ap = argparse.ArgumentParser(description="Calendrier .ics des déblocages de documents")
    ap.add_argument("--json", default=str(ATT / "attachments.json"))
    ap.add_argument("--out", default=str(ATT / "cours_albaji.ics"))
    ap.add_argument("--group-by-day", action="store_true", help="un événement par jour et par matière")
    args = ap.parse_args()

    items = json.load(open(args.json, encoding="utf-8"))["data"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    events, skipped = [], 0

    def subj(i):
        s = (i.get("task") or {}).get("subject") or {}
        return s.get("title") or "غير محدد", (s.get("level") or {}).get("name") or ""

    if args.group_by_day:
        groups = defaultdict(list)
        for i in items:
            if not i.get("unlockDate"):
                skipped += 1
                continue
            d = dt.date.fromisoformat(i["unlockDate"][:10])
            groups[(d, *subj(i))].append(i)
        for (d, subject, level), docs in sorted(groups.items()):
            titles = "\n".join(f"- {x['title']} (id {x['id']})" for x in docs)
            events.append(event(f"albaji-{d:%Y%m%d}-{abs(hash(subject)) % 10**8}@ar-audio-to-md",
                                d, f"{subject} : {len(docs)} document(s)", f"{level}\n{titles}", subject, stamp))
    else:
        for i in items:
            if not i.get("unlockDate"):
                skipped += 1
                continue
            d = dt.date.fromisoformat(i["unlockDate"][:10])
            subject, level = subj(i)
            desc = f"{subject} — {level}\nid {i['id']} · {i.get('type', '')}" + (f"\n{i['url']}" if i.get("url") else "")
            events.append(event(f"albaji-attachment-{i['id']}@ar-audio-to-md", d, i["title"], desc, subject, stamp))

    # Périodes de l'année scolaire (groupe actif) + Ramadan
    group = fetch_group()
    periods = []
    if group:
        d = lambda k: dt.date.fromisoformat(group[k][:10])
        periods.append(period("albaji-year@ar-audio-to-md", d("startDate"), d("endDate"),
                              f"السنة الدراسية : {group['name']}", "Année scolaire selon la plateforme", stamp))
        phases = sorted(group.get("groupPhases", []), key=lambda p: p["phase"]["order"])
        for ph in phases:
            a, b = dt.date.fromisoformat(ph["startDate"]), dt.date.fromisoformat(ph["endDate"])
            periods.append(period(f"albaji-phase-{ph['id']}@ar-audio-to-md", a, b,
                                  f"المرحلة {ph['phase']['order']}", "Phase de cours selon la plateforme", stamp))
        if len(phases) >= 2:
            a = dt.date.fromisoformat(phases[0]["endDate"]) + dt.timedelta(days=1)
            b = dt.date.fromisoformat(phases[1]["startDate"]) - dt.timedelta(days=1)
            periods.append(period("albaji-break@ar-audio-to-md", a, b, "عطلة بين المرحلتين (رمضان)",
                                  "Pas de cours entre les deux phases", stamp))
        print(f"{len(periods)} périodes ajoutées depuis le groupe actif")
    # Leçons du programme (student-tasks/me, enregistré par get_attachments.py --fetch)
    prog_file = ATT / "program.json"
    if prog_file.exists():
        prog = json.load(open(prog_file, encoding="utf-8"))
        n = 0
        for g in prog.get("groups", []):
            for ph in g.get("phases", []):
                for w in ph.get("weeks", []):
                    for t in w.get("tasks", []):
                        subject = (t.get("subject") or {}).get("title", "")
                        day = dt.date.fromisoformat(t["taskDate"][:10])
                        desc = f"{subject} — المرحلة {ph.get('order')}، الأسبوع {w.get('order')}\nid {t['id']} · {t.get('type', '')}"
                        if t.get("videoUrl"):
                            desc += f"\n{t['videoUrl']}"
                        events.append(event(f"albaji-lesson-{t['id']}@ar-audio-to-md", day, f"🎥 {t['name']}", desc, subject, stamp))
                        n += 1
        print(f"{n} leçons ajoutées depuis le programme")
    periods.append(period("ramadan-1448@ar-audio-to-md", RAMADAN[0], RAMADAN[1], "رمضان ١٤٤٨ (تقديري)",
                          "Dates astronomiques prévues, à confirmer par l'observation", stamp))
    events = periods + events

    ics = "\r\n".join(["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ar-audio-to-md//cours albaji//AR",
                       "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
                       fold("X-WR-CALNAME:أكاديمية الإمام الباجي — وثائق الدروس"), *events, "END:VCALENDAR"]) + "\r\n"
    Path(args.out).write_text(ics, encoding="utf-8")
    dates = sorted(dt.date.fromisoformat(i["unlockDate"][:10]) for i in items if i.get("unlockDate"))
    print(f"{len(events)} événements du {dates[0]} au {dates[-1]} ({skipped} document(s) sans date, déjà publiés) -> {args.out}")


if __name__ == "__main__":
    main()
