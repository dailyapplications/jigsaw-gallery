# Status — gallery repo (START HERE)
> A chat may have been opened from another project: work in `~/AndroidStudioProjects/jigsaw-gallery` (this repo) and the sibling app repo `~/AndroidStudioProjects/jigsaw`; read this file and `tasks/lessons.md` first. The app repo's `tasks/status.md` has the full TODO list (NEXT STEPS).
> Open gallery TODO: more HARD pictures for category `colour` (stained glass, carpets, tapestries, mosaics, kimono; CC0/PD only), daily puzzle rotating difficulty by weekday (`tools/gallery/schedule.py`), translations for new titles in `seed/title_translations.json` then `apply-titles`. Owner said: leave the duplicate wildlife pictures alone. After changes: `build`, `validate`, `pytest`, commit, push, then re-run `scripts/make_starter.py` in the app repo.
Last updated: 2026-10-11 (session 2: photo audit, Colour burst, more cartoons).
Repo is on GitHub (`dailyapplications/jigsaw-gallery`, master) and served by Pages from `/docs`. Now 17 categories, 227 active pictures (difficulty mix 49/90/65 before the new cartoons; landscapes are at least medium). Session 2: audited every picture (retired weak/duplicate ones, trimmed black scan borders with `trim-borders`), added category `colour` and 8 colourful cartoon scenes.

## Done
- `tools/gallery`: sources (met, cleveland, smk, nasa), images (WebP resize/hash), store, validate, schedule (daily.json), cli. 38 tests pass: `.venv/bin/python -m pytest -q`.
- README with licence policy, CI workflows (validate, daily), seed/categories.json (15 categories × 13 languages).
- Curation flow: `candidates` → contact sheet in `work/contact/<cat>.jpg` (gitignored) → `pick` → `build` → `validate --launch`.

## In progress / next
1. Seed 15 categories with ≥10 images each (check `cli validate --launch`). Record progress per category below.
2. `cli build`, commit images (≈400 KB each ⇒ ~60–80 MB total; fine for a repo, keep under 1 GB).
3. After the owner creates the repo: push, enable Pages, check the URL serves catalog.json.

## Seeding progress
(update as categories are completed)

## 2026-10-11 pivot (owner feedback: pictures must look like the reference screenshots — bright photos/illustrations, easier; plus difficulty tiers)
- Museum art alone is too dark/hard. New main source: **Wikimedia Commons CC0 own-work photos** (`sources/commons.py`; filter `incategory:"CC-Zero"`, LicenseShortName == CC0, Credit "Own work", ≥1600 px, blocked words for people/brands/art). Museums stay for "Old masters", "Impressionism", "Japanese prints"; NASA for "Space".
- Every picture now has `difficulty` 1/2/3 (easy/medium/hard) from `images.look_alike_share` (share of look-alike patches; thresholds 0.27/0.43 = thirds of the seed set). `cli rate -v` recomputes. App shows a badge and filter; suggested piece counts per tier.
- Categories (15): masterpieces ("Old masters"), impressionism, ukiyoe, mountains, seaside, forests, flowers, wildlife, birds, pets, space, cities, architecture ("Castles & landmarks"), food (replaced vintage), seasons.
- Seeded so far: masterpieces 10, impressionism 11, ukiyoe 12. Others: run `run_commons.sh`-style candidate searches (queries listed in this file's history) and `pick` after viewing `work/contact/<cat>.jpg`. Avoid brands/people/modern art; photos of US/UK/NL landmarks are fine (building exteriors), avoid lit-up Eiffel Tower-type FOP cases.

## 2026-10-11 night: seeding DONE
- 16 categories, 203 pictures, all ≥10 per category (`cli validate --launch` OK, 46 pytest tests pass). Docs folder ≈97 MB.
- Added `kids` category = 14 original cartoon scenes drawn by `tools/illustrations` (lib.py building blocks, scenes.py, render.py via cairosvg), imported with `cli import-illustrations` (source "original", CC0 own work, difficulty set by hand in `CARTOON_DIFFICULTY`).
- `maxPieces` per picture (from resolution) so small NASA images do not offer 1000 pieces.
- `docs/config.txt` (a=start credits, b=cap) is the remote credit config the app fetches.
- Owner idea (stock sites): Pexels/Pixabay/Unsplash would need API keys (signup) and their licences restrict redistributing copies in a public repo; not used. If wanted later: add a source module + extend `ALLOWED_LICENSES` after reading their terms (see backlog).
- TODO after owner creates the GitHub repo: push, enable Pages (master, /docs), confirm https://dailyapplications.github.io/jigsaw-gallery/catalog.json and raw config URL.
