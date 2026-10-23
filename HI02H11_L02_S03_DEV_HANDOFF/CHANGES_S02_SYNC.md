# HI02H11_L02_S03 — rebuilt on HI02H11_L02_S02 (round 2, 2026-10-16)

**Ask:** "make all the changes that are pushed in this repo (last 12 commits) … this should exactly
match with this repo — cover page animation, sfx, all the pages, its flow etc. … look exactly similar
and functional with the logics of that file."
**Source:** `github.com/CodeWithPiyush0/HI02H11_L02_S02_DEV_HANDOFF` @ `992e684` (the 12 commits
`25d2368 … 992e684`). S02 is the true sibling: this lesson's first draft was generated from an earlier
S02, and every one of those commits lands in the same three places — the builder, the injected
`train_modules.js` / `train_styles.css`, and the runner game. So S03 now runs on S02 **at HEAD**, whole,
rather than on a patch list, and only the content differs.

The previous S01-based build is kept intact in `../_backup_s01based/`.

## What is S02's, unchanged

| Area | From S02 @ 992e684 |
|---|---|
| Engine | `4_ENGINE/lesson_template.html` + `train_modules.js` + `train_styles.css` + `confetti_mtg.*`, assembled by S02's own `inject_train.py` |
| Cover | painted spritesheet train, whistle/arrival SFX, title cloud, bogies «ए (◌े)» «ऐ (◌ै)» |
| Gate | Swifty seek-and-speak gate with lip-sync per transition line; third transition placed before the game |
| Sound | `bgm_lesson.ogg` continuous background music, play/next button SFX, feedback SFX, train SFX |
| Flow | T1 pairs · T2 build · T3 words · T4 build · T5 words · **G5D demo · G5 matra sort · G1 · G3 · G2 taps · G4 word sort** · P1 word build · P2 picture sort · sentences · **MG1 मात्रा रनर** · CEL |
| Screens | S02's current MATRA_PAIRS (no heading, letter/matra land on the VO's own phrases), MATRA_BUILD (word built piece by piece, no equation panel), MEET_PAIR (with the mic button + nudge), TRAIN_TAP / TRAIN_SORT / WORD_BUILD / SENTENCE_COMPLETE with S02's hint ladders, S02's confetti |
| Game | the मात्रा रनर endless runner, folded into the engine by S02's `embed_matra_runner.py` |
| Celebration | S02's celebration kit (lip-synced Swifty) and S02's standard line «बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!» |
| Builder | `1_SPEC/build_skill_HI02H11_L02_S03.py` = S02's builder (all guards, stamps, cache-busting), converted by `1_SPEC/_make_s03_builder.py` |

## What is S03's

* **Words, pictures, scenes and Hindi lines** — from this lesson's SME deck (`1_SPEC/_SME_RECOMMENDATIONS.md`):
  सब→से→सेब · पर→पै→पैर · मेज़/पेड़ · बैल/भैंस · taps सेब / बैग / पैन · sort शेर बेर थैला पैसा ·
  ◌े ◌ै · word build _ब _र _ज़ with से बै मे बे पै · pictures पैन मेज़ शेर बैग · sentences पैन, पेड़, सेब.
* **Three sentence screens, not S02's four** — the SME deleted page 15.
* **The runner's words** — ए/ऐ pools of 20 each (no word carries ं, see below), goal lines «ए / ऐ की
  मात्रा वाले शब्द पकड़िए।», swapped-matra twins (सेब/सैब …). Levels keep S02's order: the second matra
  (ऐ) first, then ए.

## Engine changes beyond S02 (both needed by े / ै, both gated so S02's ु / ू path is unchanged)

1. `matraHL` (train_modules.js): **above-line highlight for े / ै** — the mark's box is found by
   rendering the syllable with and without it and diffing the pixels (ported from this lesson's draft);
   ं is removed from both renders so भैंस's dot never turns orange. S02 only has the below-line band.
2. Runner card highlight (matra_runner_src): the band over the consonant's top instead of under the baseline.
3. Builder: `prune_stale()` returned 2 values on a first build (no previous card.json) and crashed — fixed.

## Voice

* Lines whose text is word-for-word S02's play **S02's human recordings** (G5 demo, its outro, the
  G4 / P1 / P2 / sentence / game prompts, the celebration line, the gates, the mic nudge, the runner's
  tutorial and feedback lines).
* Everything S03-specific is **Gemini TTS, voice Kore** (the earlier S03 takes reused where the text
  is unchanged). So the lesson mixes a human narrator and a TTS voice — the same situation S02 was in
  before its recordings arrived. A recording list is written by the builder to `1_SPEC/VO_RECORDING_LIST.md`.
* Single words, letters and runner words are spoken as one list and sliced at the pauses (the TTS
  refuses a lone word) — **ear-check these**.

## Verification (2026-10-16)

* **Build:** every S02 guard passes on the S03 content (flow, single-matra, sentences, word build,
  register, mechanics, pictures, audio ladder); `0` VO pending; gate lip-sync and the celebration
  Swiftie measured from this lesson's clips.
* **Side by side:** both builds captured with S02's `_capture_settled.py` — same cover, same screens in
  the same order, same layouts; S03 has one sentence screen fewer.
* **Behaviour:** S02's `_drive_mechanics.py` (wrong → wrong → right on every activity; patched only to
  skip the watch-only demo, which crashed it on S02 itself) gives S03 the same pattern as S02 on all
  10 activity screens, `0` non-audio console errors on both.
* **Runner:** mounts with the «ऐ ◌ै» chip on level 1; every voice file it asks for returns 200.
* **Not yet done by a human:** playing the runner through, real touch on a device, and listening to
  the TTS clips (above all the sliced single words and the runner's twins — `vo_letter_*` were cut from
  the page-2 lines).
* The S01-based review deck and `dist/` from round 1 describe the OLD build; they are in
  `../_backup_s01based/`. Rebuild with `PYTHONUTF8=1 python 1_SPEC/build_skill_HI02H11_L02_S03.py`.

## Round 3 (2026-10-22) — S02's 7 QA-pass commits applied (`fb835c9 … 27cea22`)

S02 moved from `992e684` to `27cea22`: bugs 1-8 fixed, the Hindi-game-gender-identify transition screen
(`phaseBlurTransition`, Swifty `peeking_talk_up.webp`, `sfx_whoosh`), background music down to 40% then
30%, two more bug-fix rounds, and a proper 7 s inactivity nudge. Applied to S03 as:

* `4_ENGINE/lesson_template.html` — taken from S02 @ 27cea22, then S03's modules re-injected
* `4_ENGINE/train_modules.js`, `train_styles.css`, `1_SPEC/build_skill_HI02H11_L02_S03.py` — 3-way merged
  (S02 992e684 → 27cea22 onto S03's files): **0 conflicts**; the builder changes were all mechanical
  (whoosh sound, new gate, old gate lip-sync removed), none carried S02 content
* new assets: `assets/Audio/sfx_whoosh.ogg`, `assets/UI/peeking_talk_up.webp`
* the runner game is untouched by all 7 commits, so its ए/ऐ version stands as is

**Proof of sameness:** the built S03 page compared with S02's built page (card data, cache stamps and the
lesson code masked) differs only in the S03 runner content and the े/ै highlight — every other line of
~19,000 is identical. All 18 screens mount with 0 console errors; the new transition screen plays.
Pre-merge copies of every replaced file: `../_backup_draft1/pre_s02_7commits_2026-10-22/`.

## 2026-10-22 — four requested changes

1. **Transitions** — verified identical to S02 @ 27cea22: same engine code, same `gate` /
   phase-title / ui_sfx config, byte-identical `vo_pt_*` clips and `sfx_whoosh`, same placement
   (before T1, before G5D, before MG1); captured all three side by side, frame for frame the same.
2. **Page 1 matra boxes** — S02's `translateY(-.13em)` was tuned for «◌ु» hanging low; «◌े / ◌ै» rise
   above the circle and stuck out of the card. MATRA_PAIRS now centres the glyph's measured INK in its
   card (`centreInk` in train_modules.js).
3. **Page 16 (मुझे ___ खाना अच्छा लगता है)** — options are text only (`text_only=True`, S02's own switch).
4. **Scenes** — the user's new `scn-likhna / scn-bageecha / scn-seb-khana` replace the old three,
   cropped to the picture inside their baked-in frame; the rung-2 spotlight positions re-measured.
   Old scenes kept in `../_backup_draft1/replaced_images_2026-10-22/`.

## 2026-10-22 — QA list (title slide, pages 1-16)

Done:
* **S02 `6f621ea`** (idle reminder repeats every 7 s of silence) merged into the engine template.
* **Title** VO text → «नमस्ते दोस्त! मैं हूँ स्विफ्टी। आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।» (needs recording).
* **Page 1** VO → S02's script shape «यह है ए। इसकी मात्रा है।» (the bare ◌े cannot be spoken) (needs recording).
* **Page 2** the «स। से। सेब।» sound-by-sound line removed.
* **Pages 3, 5** े / ै highlight now stops at the top of the शिरोरेखा (matraHL, train_modules.js).
* **Page 4** foot re-centred on its visual weight and given the table's 4:3 footprint.
* **Pages 3, 5** pictures 220 → 260 px.
* **Pages 8-10** after the 3rd wrong attempt the speaker (and the idle reminder) repeats the rung-3
  line instead of reading the locked options out.
* **Page 11** hint 1 = S02's line (S02's human take); hint 2 per card «पैसा में ऐ की मात्रा है।».
* **Page 12** S02's hint 1 / hint 2 (S02's human takes) and rung-3 line «से को सेब वाले डिब्बे में डालिए। से, ब… सेब।».
* **Page 13** S02's hint 1 (S02's take), hint 2 «… अब इसे सही मात्रा वाली बोगी में डालिए।», hint 3 «… वाली बोगी में डालिए।».
* **Pages 14-16** S02's sentence ladder: per-screen question on hint 1, «जो वाक्य सही लग रहा है, वही शब्द चुनिए।»
  (S02's take), «<sentence> <word> चुनिए।» on hint 3.

Completed with a new key (2026-10-22):
* the 23 new VO lines generated (Kore, -16 LUFS), none short; 6 more lines use S02's human takes.
* Page 11: an Indian ₹ coin and a single-colour (golden-yellow) बेर; the four tray pictures normalised to
  the same 42 % coverage of a square canvas, so they read as one size.
* Verified: speaker after the 3rd wrong tap plays only the rung-3 line; the mechanics driver walks every
  activity with S02's VO order (page 11 hint 2 = «पैसा में ऐ की मात्रा है।» after the options are read).
* Page 11 coin replaced again with the user's own ₹1 coin picture (`paisa.png`), scaled to the same
  footprint as the other tray pictures; the generated coin is in `../_backup_draft1/replaced_images_2026-10-22/`.
* Pages 14-16: the scene panel takes the scenes' own ~1.12:1 shape (`aspect-ratio` on `.sc-scene`), so
  `object-fit:cover` no longer cuts off the top and bottom of the pictures.
* Page 12 (and every े / ै highlight): the orange no longer touches the शिरोरेखा - the overlay's glow is off
  for above-line marks (`.mh-above`) and the box stops half a px above the headline's top.

## 2026-10-23 — the lesson's own VO set installed

All 220 clips of `HI02H11_L02_S03_Manifest.xlsx` replaced from the delivered set (`VO's for ए-ऐ/voiceovers/*.wav`):
126 lesson clips → `assets/Audio/<id>.ogg` (WAV data, the lesson's convention), 94 runner clips →
`assets/MatraRunner/voice/<id>.ogg` (Ogg Vorbis q4); every clip loudness-matched to -16 LUFS (TP -1.5).
This includes the three transition lines and the lines that were S02's human takes - the lesson now has
one voice throughout. Transition title cues re-measured (2975 / 3755 / 1260 ms); the rebuild re-measured
page 1-5 animation cues and the celebration lip-sync from the new clips. Mechanics driver: every
activity plays its ladder, nav unlocks, 0 missing files. Previous audio: `../_backup_draft1/pre_new_vo_2026-10-23/`.

## 2026-10-23 — S02 `8e8fd29` (r151) applied: mic hand + «इस बटन पर टैप करिए» right after the word's line

Pages 3 / 5: the hand goes to the mic and «इस बटन पर टैप करिए» plays 0.35 s after «…बोलकर देखिए» ends (it used to
wait for 7 s of inactivity); then it repeats after every 7 s of nothing until the mic is tapped. Same one-line
change as S02 in `4_ENGINE/train_modules.js`, re-injected into the template. Measured: hand + line 0.37 s after
the line ends on मेज़ and बैल, repeat 7.0 s after it finishes.
* Then narrowed at the user's request: the instant hand + line is page 3 only (`data.mic_nudge_now`, set for T3
  by the builder); page 5 waits for 7 s of inactivity as before. Measured: page 3 at 0.36 s after the line,
  page 5 at 7.0 s; both repeat every 7 s until the mic is tapped.
* Narrowed again: instant only after page 3's FIRST word (मेज़); पेड़, बैल and भैंस wait for 7 s of inactivity.
  Measured: मेज़ 0.36 s, पेड़ 7.0 s, बैल 7.0 s, भैंस 7.0 s after the word's line ends.
