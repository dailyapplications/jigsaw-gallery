# jigsaw-gallery

Public picture catalogue for the jigsaw puzzle app (`dailyapplications/jigsaw`). The app downloads `catalog.json`
and the pictures from here, so pictures can be added, replaced or removed **without releasing a new app version**.

Served by GitHub Pages from `docs/` → `https://dailyapplications.github.io/jigsaw-gallery/`

## Licence policy (strict on purpose)
Only **CC0 / public-domain** images (or NASA-created images) are accepted. No CC-BY, CC-BY-SA, "free for personal
use", Flickr, Unsplash, Pexels, Pixabay, Google/Pinterest images. Sources used: The Met Open Access, Cleveland
Museum of Art Open Access, SMK (National Gallery of Denmark), NASA Image Library. Each entry stores the API field
that proves the licence (`proof`). Works whose creator died after 1955 are refused; unknown creators need a work
from before 1900. No identifiable modern people, logos, trademarks or recent architecture.
`validate` enforces this and CI fails otherwise. `LICENSES.md` lists every image with its source.

Code is MIT. The images keep the terms of their sources (CC0 / public domain); credit is shown in the app.

## Takedown
If you believe an image should not be here, open an issue or write to dailyapplications@gmail.com. The picture is
set to `status: retired` and the app stops showing it on its next sync.

## Layout (everything under `docs/` is published)
```
docs/catalog.json                       categories + counts + cover + version (apps skip the download when unchanged)
docs/daily.json                         date → puzzle of the day, generated 30 days ahead
docs/categories/<id>/category.json      puzzles: title (per language), creator, licence, proof, status, publishAt …
docs/categories/<id>/img/<hash>.webp    2048 px long edge, content-hashed (cache forever)
docs/categories/<id>/thumb/<hash>.webp  480 px thumbnail
seed/categories.json                    category ids, order and translated titles (13 languages)
tools/gallery/                          Python tools (stdlib + Pillow)
```

## Everyday tasks
```
python3 -m venv .venv && .venv/bin/pip install pillow pytest        # once
.venv/bin/python -m tools.gallery.cli candidates <category> --query "Hokusai" --source met,cleveland,smk
#   → work/contact/<category>.jpg : look at the numbered sheet
.venv/bin/python -m tools.gallery.cli pick <category> 0,3,7         # downloads, resizes, writes provenance
.venv/bin/python -m tools.gallery.cli retire <category> <puzzle-id> # remove a picture (app drops it)
.venv/bin/python -m tools.gallery.cli build                         # catalog.json, daily.json, LICENSES.md
.venv/bin/python -m tools.gallery.cli validate [--launch]
.venv/bin/python -m pytest
```
- **Add later / schedule:** set `publishAt` (YYYY-MM-DD) in the entry; the app hides it until that date.
- **Replace an image:** `retire` the old one, `pick` the new one (new hash → new URL, no stale caches).
- **Update a title or translation:** edit `category.json`, run `build`, commit.
- The GitHub Action `daily` runs every day: it rebuilds `catalog.json`/`daily.json` and commits when they changed.
- The app syncs daily (and on start) and only downloads what changed.

## Size and speed
Pictures are WebP (≈250–450 KB full, ≈25 KB thumbnail), named by content hash so CDNs and the app cache them
forever. A category can later point to another `baseUrl` (another repo or CDN) if Pages bandwidth is outgrown.
