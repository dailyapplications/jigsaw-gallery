# Decisions (see also ../jigsaw/tasks/decisions.md)
| 2026-10-11 | Only CC0/PD/NASA; per-image `proof`; creators died ≤1955; validate.py + CI enforce | Owner: license safety |
| 2026-10-11 | Sources met, cleveland, smk, nasa; AIC and LoC unusable from scripts (403) | Tested |
| 2026-10-11 | Published tree in `docs/`; `build` writes catalog.json, daily.json, LICENSES.md | Pages from /docs like pdfwiki |
| 2026-10-11 | Active = status active and publishAt ≤ today; the app filters by date, CI daily job only rebuilds daily.json/catalog | Simple, offline-safe |
