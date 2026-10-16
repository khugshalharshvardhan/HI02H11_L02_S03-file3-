# 4_ENGINE — HI02H11_L02_S03 per-game engine

`lesson_template.html` is a copy of the finished sibling's engine
(`HI02H11_L02_S01_DEV_HANDOFF/4_ENGINE/lesson_template.html`, kept unmodified here as
`_s01_baseline.html` so every S03 change is diffable) plus the edits below. The draft's injected
`train_modules.js` / `train_styles.css` / `inject_train.py` are retired to `_superseded_draft1/`.

Every module edit is **gated on a card `data.*` flag**, so a card that does not set it renders
exactly as S01 does.

| # | Where | Change | Why (deck) |
|---|---|---|---|
| 1 | `INWORD_MATRAS` | + `े`, `ै` | in-word red highlight on every page; above-base zero-advance marks subtract cleanly |
| 2 | `_matraWordSVG` | raster ascent 0.92em → 1.30em | the rising stroke of े/ै sat above 0.92em and was clipped (viewBox still crops to ink — no size change) |
| 3 | `_matraInkMask` | bindu exclusion (cluster rastered without ं/ँ) | p6: "the ं dot … do not include it in the red matra highlight" (भैंस) |
| 4 | MATRA_BUILD | `base_outline` (dashed soft frame), `base_hl_ms` (picture glows on its clause) | p3 group of children + «ये सब बच्चे हैं»; p5 «मेज़ पर किताब रखी है» |
| 5 | TRAIN_TAP | `keep_hl` (rung-2 highlights stay; rung 3 relights answer), `hl_on_correct` | p7–9 "retain the matra highlights"; "highlight only े inside सेब" on correct |
| 6 | TRAIN_SORT | per-card `hint1_audio`; `h2_show_word` (temporary word, removed on placement); `h2_enlarge`, `h2_silent_name`; label read-out only when a label clip exists; `h3_freeze` (other cards locked during rung 3); `h3_hand:false`; `hl_on_correct` | p10, p11, p13 |
| 7 | MATRA_FILL | `akshar` mode: slot `key` («से») separate from highlight `matra` («े»); `option_audio` (tap speaks the akshar); rung 2 = enlarge + matra red + akshar sound; rung 3 guides THIS blank (correct akshar + blank glow, rest locked, per-slot `hint3_audio`); unused distractors disabled at the end | p12 |
| 8 | new `SlideModules.SENTENCE_COMPLETE` + `.sc-*` CSS | scene · sentence with dashed blank · picture+word cards; tap speaks, drag answers; 3-rung ladder (preview each option in the blank + scene spotlight on rung 2) | p14, p16, p17 |
| 10 | `centerInkGlyph` reads `data-mh-word` | a highlighted word is an SVG carrying the word twice, so the fitter measured «सेबसेब» and halved it (result word 84→32px; would also shrink coach words once rung-2 highlights stay lit). Also present in S01 (जाल renders at 54px of 84) | p3, p5, p7–9 |
| 9 | runner cache-warmer | only runs when the card has a *RUNNER* slide | S01's warmer requested 14 files this lesson does not have (404s) |

Patch scripts that made these edits (run once, assert-guarded): `_patch_s03_modules.py`,
`_patch_s03_sentence.py`; edits 1–3 and two CSS tweaks were applied inline.
