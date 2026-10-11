# Jigsaw puzzle game — plan

## Context
New offline-first Android jigsaw game, ad-funded with a credit system like the PDF app. Two new sibling repos next to `pdfreader`/`pdfwiki` in `~/AndroidStudioProjects/`:
- **`jigsaw`**: the app (Kotlin, Compose, Material 3, minSdk 29, compile/target as pdfreader). Package `com.dailyapplications.jigsaw`.
- **`jigsaw-gallery`**: public content repo (images + JSON catalog + scripts + CI). The app reads it, so photos are added, changed or removed without an app release.

Assumptions (change if wrong): "under parent" = sibling folders like `pdfwiki`; placeholder app name "Jigsaw Atelier"; GitHub org `dailyapplications` with the existing SSH setup. **Owner authorised creating the repos and pushing to `dailyapplications`** (done in M0/M1; the repos are public except possibly the app repo, matching pdfreader's private one; real AdMob IDs and keystores stay out of git). Both repos follow the project convention: `CLAUDE.md` and `tasks/{status,lessons,decisions,plan,backlog}.md`, updated after each chunk.

## Is it worth it?
Yes with limits. Jigsaw is crowded (Jigsaw Puzzles Real, Magic Jigsaw, Jigsaw Explorer), so it only works if it feels better and content stays fresh at near-zero cost. Strengths: daily sessions, a long ad-friendly session length, no server, and the dynamic gallery repo makes content free to refresh. Risks: image licensing, GitHub Pages bandwidth, and ads not loading offline. Gate: ship the MVP (M0–M5), watch retention and ad revenue for 30–60 days, and only then invest in extras.

## Differentiators (what makes it better, not just different)
1. **Pieces join each other anywhere on a free table.** Pan and pinch-zoom, no forced tray. Matching neighbours merge into groups that move together (real-puzzle feel). The reference only has a tray and board.
2. **Join effect that feels physical.** Spring settle, a short light sweep along the new seam, soft dust particles, a quiet click and a haptic tick. Bigger effect when a group completes a border.
3. **Smart helpers:** edge-pieces-only filter, "tidy" animation that fans pieces into sorted rows, ghost-image opacity slider, press-and-hold peek, hint (highlights a piece and its slot).
4. **Completion moment:** seams fade, a light wave crosses the picture, it settles in a frame with title, author and license. Actions: share, save as wallpaper. A time-lapse replay of the solve comes later (needs only a move log).
5. **Download a category for offline** ("flight pack"), plus a small starter pack bundled in the APK so a first launch with no network still works.
6. **Daily puzzle with a streak calendar** (free, any size up to 300).
7. **Modes:** Relax (no timer, ghost on) and Challenge (timer, rotation on, no ghost).
8. **Own photos** from gallery or camera with an aspect-ratio crop. They stay on the device and are never uploaded, so no moderation is needed.
9. **Accessibility:** haptics toggle, reduce-motion, large-piece option, colour-safe UI.

Skipped on purpose: accounts, leaderboards, multiplayer (the no-account rule and server cost), and a copy of the reference's polaroid stacks, denim texture or navy and gold look.

## Visual direction (not AI slop)
- **Gallery/atelier feel:** warm paper and ink neutrals, one terracotta accent, bundled serif for titles (Fraunces) and a clean sans (DM Sans/Inter). Dark mode is a "night table". No purple gradients, glassy cards or emoji icons.
- **Table surface:** subtle procedurally generated linen noise. Pieces get a soft top-left light, thin edge highlight, and a deeper shadow while lifted.
- **Home:** editorial image-led layout: big daily-puzzle hero, category rows with varied card sizes, progress rings on in-progress puzzles.
- **Motion:** shared-element transition card → difficulty sheet → board. Pieces scatter in at start. Snap pulse. Respect the system animation scale and a reduce-motion setting.

## Content repo (`jigsaw-gallery`)
```
catalog.json                      schemaVersion, minAppVersion, version, categories[] (id,title,order,cover,baseUrl)
categories/<id>/category.json     puzzles[] {id,title,file,thumb,w,h,author,license,sourceUrl,addedAt,publishAt,status,tags,avgColor}
categories/<id>/img/<hash>.webp   2048 px long edge, WebP q~82 (~250–450 KB), content-hashed → cache forever
categories/<id>/thumb/<hash>.webp 480 px (~25 KB)
daily.json                        date → puzzle id, generated ahead by CI
queue/                            drop-in folder for batch adds
tools/ (Python)                   add_puzzle.py · import_folder.py · validate.py · build_index.py · schedule_daily.py (+ pytest)
.github/workflows/                validate (PRs) · daily (cron: apply publishAt, fill daily.json, rebuild, deploy Pages)
```
- **Add:** `add_puzzle.py --category nature --url <commons/museum url>`. It reads author and license from the source API, rejects disallowed licenses, resizes, hashes, writes JSON.
- **Update:** new file, new hash, the entry points to it.
- **Delete:** set `status: retired` (or remove). The app drops it from lists, purges cached copies after 30 days, and keeps in-progress puzzles playable.
- **Scale:** each category has `baseUrl`, so images can move to another repo or CDN (jsDelivr mirror) if Pages bandwidth or the ~1 GB repo size becomes a problem.
- **Licence safety policy (public repo, commercial ad-funded app, so the strictest rules):**
  - **Gallery accepts only CC0 / Public Domain.** No CC-BY, CC-BY-SA, "free for personal use", Flickr, Unsplash, Pexels, Pixabay, Google/Pinterest images (BY-SA forces share-alike on adaptations; Unsplash/Pexels/Pixabay forbid redistributing collections; the rest is unclear).
  - **Preferred sources, using the machine-readable public-domain flag:** Met Open Access (`isPublicDomain=true`), Art Institute of Chicago (`is_public_domain`), Rijksmuseum (CC0), Cleveland Museum of Art (CC0), Smithsonian Open Access (CC0), NASA Image Library (NASA-created only; no NASA logos, no endorsement implied, skip anything credited to a third party). Wikimedia Commons only as a fallback and only for files tagged CC0 or PD-old/PD-Art (creator died 70+ years ago and the file is a faithful 2D reproduction), never "attribution required", "non-free" or "permission pending".
  - **Content filters beyond copyright:** no identifiable modern people (privacy/publicity rights), no logos or brands, no recent architecture or public sculpture (freedom-of-panorama differs by country; use pre-1900 buildings or PD artworks), no trademarked characters, nothing sacred or sensitive.
  - **Own/AI-made illustrations:** only a small share, generated by us, recorded with the tool and terms used, never in the style of a named living artist or a known character; AI output may not be copyrightable, so don't rely on exclusivity.
  - **Provenance record per image, required by `validate.py`:** source URL, licence name and URL, creator, retrieved date, and the API field that proved the licence (stored as a hash of the saved response). CI fails on a missing or non-allowlisted licence. A generated `LICENSES.md` lists every image.
  - **Human check:** I review a contact sheet per category and spot-check 100% of Commons files against their description page before commit.
  - **Takedown path:** README contact + in-app "Report this picture" link; a report sets `status: retired` in minutes, and the app stops showing it on the next sync.
  - **Repo licensing:** code under MIT, content terms stated separately (CC0/PD sources, upstream credits kept). An optional lawyer review of this policy is recommended before the Play release.
- **Launch seed (owner requirement): 15 categories × at least 10 puzzles = 150+ images**, all licence-checked by `validate.py`:
  1. Art masterpieces · 2. Impressionism · 3. Japanese woodblock prints · 4. Mountains · 5. Beaches & oceans · 6. Forests & autumn · 7. Flowers & gardens · 8. Wildlife · 9. Birds · 10. Cats & dogs · 11. Space & nebulae (NASA) · 12. Cities & night lights · 13. Castles, bridges & architecture · 14. Vintage posters & botanical/natural-history illustrations (public domain) · 15. Seasons & holidays (Christmas, autumn, spring).
  Sources per category follow the licence policy above (museum open-access APIs first). Because strict CC0/PD rules and "no modern people/architecture" limit photography, categories such as Beaches, Cats & dogs and Cities lean on public-domain paintings, prints and vintage photographs plus NASA, which also looks good as puzzles; if a category can't reach 10 safe images it is replaced by another that can. Seeding is scripted (`add_puzzle.py --query ...`), filtered by min 2000 px long edge, sane aspect ratio and licence, then reviewed per the human-check rule before commit.

## App architecture (`jigsaw`)
- **Pure Kotlin engine** (unit-testable, no Android): `PuzzleGrid` (piece count → rows/cols for the image aspect), `EdgeGenerator` (seeded Bézier tabs; neighbouring edges are exact complements; border edges flat), `SnapRules` (tolerance ~25% of piece size), `PieceGroups` (union-find merging), `SaveState` (serializable), `Hints`.
- **Rendering:** Compose Canvas. Piece bitmaps are cut once on a background dispatcher with the piece path as a clip, then drawn with transforms. Hit-test uses bounds plus an alpha mask. Target: 500 pieces at 60 fps, 1000 pieces still usable; measure on the emulator and a real device.
- **Data:** kotlinx.serialization JSON files + DataStore (no Room). Catalog cache with ETag. Images fetched by OkHttp into app storage with LRU purge, thumbnails by Coil. WorkManager daily sync (same pattern as `CreditConfigSource`). Daily puzzle offline fallback: deterministic pick from the bundled pack by date.
- **Save/resume:** auto-save on every drop (debounced); several puzzles in progress.
- **Reuse from pdfreader:** copy `ads/*` (AdPolicy, AdRules, ConsentManager/UMP, slots, AdCoordinator), `credits/*` (CreditLedger, Store, Manager, remote config) and the isolated-process guard lessons into the new repo. Copy, not a shared library, until a third app needs it (note in decisions.md).

## Free image search from the phone ("Find more pictures")
Yes, it can be done free and legally, with no API key and no server of ours:
- **Wikimedia Commons API** (free, no key, returns licence + author per file), **Met Open Access API** (CC0, no key), **Art Institute of Chicago API** (CC0 subset, no key), **NASA Image Library API** (no key). Openverse (aggregator of CC0/PD/CC-BY) is an optional extra: anonymous use is rate-limited and a registered key would have to ship in the app, so skip it in v1.
- **Not used for in-app search:** Unsplash, Pexels, Pixabay. They need API keys, strict hotlink/attribution rules and low rate limits.
- **How it works:** a search box on the "My pictures" screen queries the museum APIs (Met, AIC, NASA; Commons last) live and keeps only results the source flags as public domain/CC0, minimum size ≥1600 px, no people filter on Commons results. It shows thumbnails with creator and licence. Pick one → it downloads to the device, is cut like an own photo (costs the same credits) and stays local; source and creator are kept with the puzzle and shown on the completion card. Needs network only while searching; downloaded pictures play offline.
- **Why this is safe:** same CC0/PD-only rule as the gallery (no CC-BY or BY-SA either), the user picks the image, we fetch it straight from the source to their device and never redistribute it or add it to the shared gallery. We send a descriptive User-Agent as the APIs ask.
- **Risk to note:** Commons has some mislabelled files, which is why it is the last source, shows the licence text, and has a "Report" link. Own photos stay on the device only, so Play's user-generated-content rules (sharing between users) don't apply.

## Languages
Launch with the ten-plus most popular Play Store languages, written to the same parity-tested pattern as pdfreader: **English (default), Spanish, Portuguese (Brazil), French, German, Italian, Russian, Turkish, Indonesian, Arabic (RTL), Japanese, Korean, Hindi**. (Same 13 as pdfreader minus Lithuanian; add `lt` if you want it.) Puzzle and category titles in the catalog get optional `title` translations per language with English fallback, so new content needs no app release; a parity test checks every string resource exists in all languages.

## Credits and ads
- **Start 2500 credits, +250 daily, cap 4000, rewarded ad +300**, all remote-tunable by a small text file like pdfreader's `CreditConfig`. Credits are never required for the basics: puzzles up to 40 pieces and the daily puzzle (up to 300 pieces) are always free.
- **Costs scale steeply with size (draft, in one `PuzzleCosts` place with a pinning test):** up to 40 pieces 0 · 60 pieces 50 · 100 pieces 100 · 150 pieces 150 · 300 pieces 300 · 500 pieces 600 · 1000 pieces 1500. Extras: own photo or searched picture +200, hint 50, rotation mode +100, offline category download 100. So the starting 2500 buys, for example, one 1000-piece puzzle plus several mid-size ones, then the player earns more through the daily top-up and rewarded ads. A calm balance chip; cost is stated before it is charged, with a refund if the puzzle fails to load. Numbers are tuned after real play data.
- **Ads, only at natural breaks:** a banner on Home, an interstitial after completing a puzzle (cap: not before day 2 or the first 3 puzzles, then every 2nd completion), rewarded for hints or credits, rewarded interstitial bonus, a native card in the category list. **No ads over the board and none before a puzzle opens.** UMP consent as in pdfreader. When no ad can load, the reward still works (offline friendly).

## Milestones
- **M0 Setup:** create both repos locally, tasks docs, CLAUDE.md, Gradle scaffold, CI skeleton.
- **M1 Content repo:** schema, tools + pytest, seed 150+ puzzles in 15 categories, validate/daily workflows, push to `dailyapplications/jigsaw-gallery` and enable Pages.
- **M2 Engine (riskiest, first):** geometry, cut, drag, snap, groups, performance spike on 500/1000 pieces.
- **M3 Board feel:** effects, haptics, sound, pan/zoom, tidy, edge filter, ghost, hint, completion sequence.
- **M4 Product shell:** catalog client, Home/categories, difficulty sheet, own photos, free image search (Commons/Met/AIC/NASA), save/resume, daily + streak, offline packs.
- **M5 Monetization:** credits, rewarded, interstitial, banner, native, consent.
- **M6 Polish and release:** design pass, dark mode, accessibility, 13 languages with parity test, store listing, R8 release smoke test, signing.

## Testing (positive and negative; no mutation testing)
- **Engine unit tests:** complementary edges match, border edges flat, grid for odd aspect ratios, snap inside vs outside tolerance, group merge and no merge on wrong neighbours, save/restore round-trip, hint picks an unplaced piece.
- **Data tests:** catalog parse (valid, unknown fields ignored, corrupt file falls back to cache), retired puzzle removed but in-progress kept, ETag unchanged = no download, offline fallback for daily.
- **Credits tests:** afford/insufficient, refund on failure, daily top-up and cap, remote-config validation (bad values ignored), `PuzzleCosts` pinned.
- **Content repo (pytest):** license allowlist accept/reject, missing author rejected, oversize image rejected, hash change updates the entry, retired removal, `publishAt` future entries hidden.
- **Compose and instrumented tests:** Home from a fake catalog, difficulty sheet shows cost, insufficient credits flow, dragging a piece onto its slot snaps and joins, wrong spot does not, rotation mode, resume after process death.
- **Performance and release:** frame-time/jank check on 500 and 1000 pieces (gfxinfo), animation sanity via emulator recordings, R8 release smoke test and `adb logcat -s AndroidRuntime:E` per the pdfreader lesson.

## Verification (end to end)
1. `./gradlew :app:testDebugUnitTest` and `connectedDebugAndroidTest` on `Medium_Phone_API_35` (all green).
2. `pytest` in `jigsaw-gallery`, and CI green on a PR that adds a puzzle.
3. Add a puzzle and retire another in the gallery repo with the tools, then check the app picks up both on next sync with no app update.
4. Play a 100-piece puzzle on the emulator: drag, snap with effect, merge, complete, share.
5. Airplane-mode check: starter pack plays, a downloaded category plays, ads and sync fail quietly.
6. Release build smoke test.

## Still needs you later
Real AdMob IDs and the final app name and icon. Repo creation and pushing are already authorised.
