#!/home/pc/projets/ar_audioToMd/.venv/bin/python
# Lanceur yt-dlp qui contourne le « mode restreint » YouTube imposé par le DNS du réseau.
#
# Sur cette machine, le DNS fait pointer www.youtube.com vers restrictmoderate.youtube.com,
# ce qui bloque certaines vidéos (erreur 151, « الفيديو غير متاح »). Ici, la résolution de
# www.youtube.com est remplacée, pour ce processus seulement, par celle de youtube.com
# (adresse normale). Aucun changement système, aucun droit administrateur.
# Usage : identique à yt-dlp (./ytdl.py <options> <url>).
import socket
import sys

_real_getaddrinfo = socket.getaddrinfo
_REDIRECT = {"www.youtube.com", "m.youtube.com", "music.youtube.com", "youtubei.googleapis.com"}


def _getaddrinfo(host, *args, **kwargs):
    if isinstance(host, str) and host.lower() in _REDIRECT:
        return _real_getaddrinfo("youtube.com", *args, **kwargs)
    return _real_getaddrinfo(host, *args, **kwargs)


socket.getaddrinfo = _getaddrinfo

from yt_dlp import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
