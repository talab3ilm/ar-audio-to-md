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
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATT = ROOT / "attachments"


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

    ics = "\r\n".join(["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ar-audio-to-md//cours albaji//AR",
                       "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
                       fold("X-WR-CALNAME:أكاديمية الإمام الباجي — وثائق الدروس"), *events, "END:VCALENDAR"]) + "\r\n"
    Path(args.out).write_text(ics, encoding="utf-8")
    dates = sorted(dt.date.fromisoformat(i["unlockDate"][:10]) for i in items if i.get("unlockDate"))
    print(f"{len(events)} événements du {dates[0]} au {dates[-1]} ({skipped} document(s) sans date, déjà publiés) -> {args.out}")


if __name__ == "__main__":
    main()
