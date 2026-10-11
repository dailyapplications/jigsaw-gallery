# Decisions (see also ../jigsaw/tasks/decisions.md)
| 2026-10-11 | Only CC0/PD/NASA; per-image `proof`; creators died ≤1955; validate.py + CI enforce | Owner: license safety |
| 2026-10-11 | Sources met, cleveland, smk, nasa; AIC and LoC unusable from scripts (403) | Tested |
| 2026-10-11 | Published tree in `docs/`; `build` writes catalog.json, daily.json, LICENSES.md | Pages from /docs like pdfwiki |
| 2026-10-11 | Active = status active and publishAt ≤ today; the app filters by date, CI daily job only rebuilds daily.json/catalog | Simple, offline-safe |

## Difficulty floor for landscapes (2026-10-11)
Owner feedback: realistic mountain/sea photos are not easy. The look-alike score alone rated them easy because every patch differs slightly. `images.CATEGORY_FLOOR` now makes mountains, seaside, forests, seasons, cities and architecture at least medium; close-up subjects (birds, flowers, food, wildlife) can stay easy. Applied on add (`store.puzzle_entry`) and by `rate`.

## Photo audit (2026-10-11)
Reviewed every picture on contact sheets. Retired near-duplicates and poor shots (cluttered, blurry, black background): birds 5, food 4, mountains 1, seasons 1. Fixed truncated titles. `trim-borders` cuts the black scan mat off photographed paintings (impressionism, masterpieces, ukiyoe; 7 pictures re-written).

## "Colour burst" category and more cartoons (2026-10-11)
Owner asked for more colourful pictures. New category `colour` (28 pictures): CC0 Commons photos (lorikeets, lavender, poppies, umbrellas, Chefchaouen door, sky) plus colourful public-domain paintings (Van Gogh, Gauguin, Rousseau, Signac via Met/Cleveland). Eight new colourful cartoon scenes added to `kids` (22 there now). `trim-borders` also runs on non-Commons pictures in `colour`.
