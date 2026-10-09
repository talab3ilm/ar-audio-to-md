# ar-audio-to-md

Pipeline local de transcription de cours en arabe (YouTube) vers Markdown, avec
vocalisation (tashkeel) automatique. Alimente le vault Obsidian
[secondbrain-albaji](https://github.com/talab3ilm/secondbrain-albaji).

## Chaîne de traitement

```
YouTube ──grab_audio.sh──► audio/*.flac ──transcribe.py──► transcript.md ──md_to_text.py──► texte.md
                           (16 kHz mono)                  (horodaté + tashkeel)              (texte continu)
```

| Script | Rôle |
|---|---|
| `pull_sources.py [--list] [--dry-run] [--max-new N] [--force URL]` | Lit `sources.txt` (vidéos, playlists, chaînes YouTube, livres), traite ce qui est nouveau en enchaînant les trois scripts ci-dessous, dépose le résultat dans `secondBrain/raw/` et tient le registre `sources.done.tsv`. |
| `grab_audio.sh <id\|url>` | Télécharge l'audio en FLAC 16 kHz mono. Nom : `yyyy-mm-dd-hh-mm <titre> [<id>].flac`, la date étant celle de diffusion du direct. |
| `transcribe.py <audio> [sortie.md] [--tashkeel catt\|ichkil\|none] [--model …]` | faster-whisper `large-v3` sur GPU, puis vocalisation CATT par lots. Produit un Markdown avec un segment horodaté par ligne. |
| `md_to_text.py <transcript.md> [--pause S] [--mots N] [--lignes]` | Retire les horodatages et regroupe en paragraphes (silence > 2 s ou 100 mots). |
| `draft_lesson.py <dossier du cours>` | Après validation (`texte-ok.md`), fait écrire par le modèle local (Ollama, qwen3.5:27b) un `brouillon.md` : résumé, matière, plan, concepts, أعلام, فوائد, passages douteux, résumé français. C'est le premier étage de l'ingestion, Claude relit ce brouillon dans `/ingest`. |
| `txt_to_md.py <livre.txt> --categorie … --ouvrage … --tome N` | Texte de livre (aljam3/turath, pages séparées par `PAGE_SEPARATOR`) vers Markdown structuré : titres (sourate, باب, « قوله تعالى »), paragraphes recollés à travers les pages, marqueurs `<!-- ص N -->`, notes de bas de page dans un fichier séparé relié par wikilinks. |
| `pdf_to_md.py <livre.pdf> [--txt livre.txt] [--pages a-b] …` | Livre scanné : OCR marker-pdf (structure) + texte aljam3 (second avis) réconciliés page par page par le modèle local, puis même post-traitement que `txt_to_md.py`. Les pages réconciliées sont mises en cache dans `temp/marker/`. |
| `textTomd.py <fichier.txt>` | Ancien nettoyage basique, conservé pour référence. |

### Flux d'un cours

```
sources.txt ──pull_sources.py──► raw/youtube/<cours>/{meta,transcript,texte}.md
                                        │  relecture manuelle
                                        ▼
                                 texte-ok.md ──draft_lesson.py──► brouillon.md ──/ingest (Claude)──► wiki/
```

## Prérequis

- WSL2 ou Linux, Python 3.12, `ffmpeg` dans le PATH.
- GPU NVIDIA pour `large-v3` (testé sur RTX 5090). Les bibliothèques CUDA (cuBLAS, cuDNN)
  sont installées par pip et préchargées par `transcribe.py`, aucune installation système.
- Modèles téléchargés au premier lancement : Whisper large-v3 (≈ 3 Go), CATT (≈ 90 Mo).

## Installation

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Utilisation

```bash
./grab_audio.sh mxWq9pEKBTs
./transcribe.py "audio/2026-10-07-19-56 لقاء افتتاحي ｜ ذ. نبيل ڭزناي [mxWq9pEKBTs].flac"
./md_to_text.py "audio/2026-10-07-19-56 لقاء افتتاحي ｜ ذ. نبيل ڭزناي [mxWq9pEKBTs].md"
```

Ordre de grandeur sur RTX 5090 : 7 minutes de calcul pour 90 minutes d'audio, tashkeel compris.
Les fichiers produits sont ensuite déposés dans `secondBrain/raw/youtube/<nom>/` sous les noms
`transcript.md`, `texte.md` et `meta.md`.

## Vocalisation

Whisper ne produit pas de tashkeel. Il est ajouté après coup par
[CATT](https://github.com/abjadai/catt) (transformer encodeur-décodeur, Apache 2.0), le plus
précis des modèles testés ; `ichkil` (ONNX, CPU) reste disponible en alternative. Le résultat
reste approximatif sur les noms propres et les passages en darija : la version vocalisée sert
de référence dans `raw/`, le wiki est écrit sans tashkeel sauf citations.

## Arborescence

```
ar_audioToMd/
├── grab_audio.sh, transcribe.py, md_to_text.py, textTomd.py
├── requirements.txt
├── audio/            # FLAC téléchargés (ignoré par git)
├── temp/             # livres en cours de conversion (ignoré par git)
├── docs/nextwork/    # guides « AI Second Brain » qui ont inspiré le vault
└── secondBrain/      # le vault Obsidian, dépôt git séparé (ignoré ici)
```

## À venir

- `sources.txt` : liste d'URL YouTube (vidéos, playlists) et de livres à traiter automatiquement.
- `pdf_to_md.py` : conversion de livres scannés en Markdown structuré (marker-pdf + texte aljam3
  + réconciliation par modèle local), avec hiérarchie des chapitres et tashkeel.
