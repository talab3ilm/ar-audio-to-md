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
| `turath_to_md.py <id\|url turath> --categorie … [--pdf]` | **Voie principale pour les livres, un seul lien suffit.** Lit le JSON public de turath.io (texte saisi, table des matières, pagination de l'imprimé, notes du محقق quand elles ont été saisies). Télécharge automatiquement le TXT du scan de la même édition (fonds ieasybooks sur Hugging Face, celui que sert aljam3.com), l'associe au bon tome par similarité, et reporte le tashkeel de l'imprimé mot à mot (alignement par forme nue, aucun tashkeel inventé). Récupère les notes depuis le scan si turath ne les a pas. Quelques secondes par livre, sans GPU. `--txt N=fichier` ou `--txt-dir` pour fournir les TXT à la main. |
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

## Plateforme de l'académie (API) et programme 2026-2027

Les scripts `get_attachments.py` et `make_calendar.py` lisent l'API de la plateforme
(`https://baji.irchademy.irchad-backends.com/api`, en-tête `x-tenant-key: baji`, jeton Bearer de
24 h dans `attachments/token.txt`, hors git). Chiffres relevés le 10 octobre 2026 pour le compte
étudiant, niveau 1, groupe « 2026-2027 - المستوى الأول ».

### Année et phases (`groups/active/me`)

| Période | Dates |
|---|---|
| Année scolaire | 4 octobre 2026 → 11 juillet 2027 (inscriptions jusqu'au 31 octobre 2026) |
| Phase 1 | 5 octobre 2026 → 9 janvier 2027 (25 semaines) |
| Pause entre les phases | 10 janvier → 13 mars 2027 (englobe Ramadan 1448, ≈ 8 février → 9 mars) |
| Phase 2 | 14 mars → 4 juillet 2027 (25 semaines) |

### Matières du niveau 1 (`subjects/level/1/is-active/true`)

الفقه · التوحيد و العقيدة · النحو · التجويد · السيرة النبوية · التزكية والأخلاق (toutes de
catégorie MAIN, coefficient 1). Les quatre niveaux du cursus ont chacun deux phases.

### Leçons vidéo programmées (`student-tasks/me`)

116 leçons du 12 octobre 2026 au 26 juin 2027, une par jour de cours, 65 en phase 1 et 51 en
phase 2. Le lien YouTube d'une leçon n'est exposé qu'à son ouverture.

| Matière | Leçons |
|---|---|
| الفقه | 26 |
| التوحيد و العقيدة | 24 |
| التجويد | 23 |
| السيرة النبوية | 22 |
| النحو | 21 |

### Documents de cours (`attachments?level=1`)

238 documents PDF, débloqués un à un du 12 octobre 2026 au 26 juin 2027 (aucun en février).
Trois types : تفريغ (transcription officielle de la leçon), تشجير (schéma), تلخيص (résumé).
L'URL d'un document n'apparaît qu'à sa date de déblocage ; les fichiers sont servis depuis S3
sans authentification et sont des PDF Word avec texte sélectionnable.

| Matière | Documents |
|---|---|
| السيرة النبوية | 65 |
| النحو | 62 |
| التوحيد و العقيدة | 59 |
| الفقه | 52 |

### Fichiers produits dans `attachments/`

- `attachments.json` : liste brute des documents ; `index.tsv` : la même en tableau avec la date de déblocage.
- `program.json` : programme brut (phases, semaines, leçons) ; `program.tsv` : une ligne par leçon (date, phase, semaine, matière, id, ouverte, lien vidéo).
- `cours_albaji.ics` : calendrier unique, 358 événements (116 leçons, 237 documents, année, phases, pause, Ramadan).
- `pdf/<niveau>/<matière>/` : les PDF téléchargés (hors git).

Relance hebdomadaire : `./get_attachments.py --fetch` puis `./make_calendar.py`, après avoir
recollé un jeton valide.

## À venir

- `sources.txt` : liste d'URL YouTube (vidéos, playlists) et de livres à traiter automatiquement.
- `pdf_to_md.py` : conversion de livres scannés en Markdown structuré (marker-pdf + texte aljam3
  + réconciliation par modèle local), avec hiérarchie des chapitres et tashkeel.
