# HI02H11_L02_S03 · «मात्राओं की रेल» (ए / ऐ) — SME revision, round 1

**Source:** `HI02H11_L02_S03_SME_Review.pptx` (notes verbatim in `../1_SPEC/_SME_RECOMMENDATIONS.md`).
**Developer brief:** "same layout, buttons, animation, colours, typography and flow as the finished
HI02H11_L02_S01; only the content and pictures change."
**Built:** 2026-10-07 · engine `2026.08.04b-r4-unified` (the S01 per-game copy + S03 additions,
see `../4_ENGINE/CHANGES.md`).

Status vocabulary: ✅ DONE · ⚑ FLAGGED (decision needed / deviation) · N/C (nothing asked).

## What changed structurally

* The draft ran on its own injected train modules. It now runs on **S01's finished engine** —
  the spritesheet train cover with smoke and arched title, the TrainChrome screens with the
  arrival/departure animation, Swiftie peek gate, the lip-synced celebration, the 3-rung ladder.
* Final screen order (deck order after the SME's edits): landing · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 ·
  **drag demo** · 10 · 11 · 12 · 13 · **17 · 14 · 16** · 18. Page 15 (मेरे ___ में दर्द है → पैर)
  **deleted**.
* All VO regenerated in Gemini voice **Kore** — the voice S01 uses — so the two lessons sound the
  same. Five lines whose text is identical to S01's reuse S01's takes.
* 9 new pictures: सब (group of children), पर (book on table), भैंस, शेर, बेर, थैला, पैसा, and
  re-drawn पैर (now shows the ankle) and बैल (now shows the hump).

## Checklist

| # | Deck page | Ask (abridged from the verbatim note) | Status | Proof / note |
|---|---|---|---|---|
| 1 | Cover | — | N/C | |
| 2 | 1 Landing | Remove extra text; show only two boxes ए(◌े), ऐ(◌ै) as train bogies | ✅ | `landing_hero` matra_train, 2 coaches, «“ए” (◌े)» «“ऐ” (◌ै)» |
| 3 | 1 | Train enters right→left; matras pop in one by one after VO; **"First show ु, followed by ू"** | ✅ ⚑ | S01 cover entrance. The ु/ू line is a copy-paste leftover — built as े then ै |
| 4 | 1 | SFX whistle on entry; sparkle/pop per matra | ✅ | S01 cover audio |
| 5 | 1 | VO «हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।» | ✅ | `vo_landing` (S01 take, identical text) |
| 6 | 2 MATRA_INTRO | Keep heading «आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।», no other text | ✅ | T1 prompt_hi |
| 7 | 2 | Pairs ए→◌े then ऐ→◌ै, one active at a time, earlier pair dims; matra glow; VO «यह है ए। इसकी मात्रा देखिए।» | ✅ | S01 MATRA_PAIRS; matra lights on «इसकी» (measured cue) |
| 8 | 2 | Red only on matra strokes, dotted circle neutral; pop/chime; आगे only after both pairs | ✅ | S01 behaviour |
| 9 | 2 | No छोटी/बड़ी | ✅ | build guard fails on either word |
| 10 | 3 MATRA_BUILD | सब + picture of three children with ONE soft outline round the group | ✅ | `obj_sab` + `base_outline` (dashed rounded frame) |
| 11 | 3 | VO «यह शब्द देखिए — सब। ये सब बच्चे हैं।», group highlighted on «ये सब बच्चे हैं» | ✅ | `base_hl_ms` cue → picture glows while named (em-dash → comma, TTS truncation rule) |
| 12 | 3 | स lights; स + ◌े = से centre; matra slides down into place; VO «स के साथ ए की मात्रा लगाने पर ‘से’ बनता है।» | ✅ | S01 sequence; syllable forms on «बनता» |
| 13 | 3 | ब joins → सेब; only े red; apple appears after सेब; VO «अब ‘ब’ जुड़ने पर ‘सेब’ बनता है।» | ✅ | `join_ms` on «सेब»; in-word े highlight (new) |
| 14 | 3 | Sound differentiation स → से → सेब with pauses | ✅ | `vo_mb_seb_sounds` «स, से, सेब।», each element lifts on its own sound |
| 15 | 3 | SFX pop / chime / success; आगे after the whole sequence; dotted circle disappears on joining | ✅ | S01 behaviour |
| 16 | 4 MEET_PAIR | Heading «ए की मात्रा वाले शब्द पढ़िए।»; one example at a time: मेज़ then पेड़ | ✅ | T3 |
| 17 | 4 | VO «मेज़ — बोलकर देखिए। इसमें म पर ए की मात्रा लगी है।» (same for पेड़); word → picture → matra red on the explanation | ✅ | picture on «बोलकर», matra on «इसमें» |
| 18 | 4 | Nukta preserved, not highlighted; pop/chime; आगे after both | ✅ | ink-mask highlights े only |
| 19 | 5 MATRA_BUILD | पर + book-on-table picture; VO «यह शब्द देखिए — पर। मेज़ पर किताब रखी है।», picture lit on that clause | ✅ | `obj_par`, `base_hl_ms` on «मेज़» |
| 20 | 5 | प + ◌ै = पै; र joins → पैर; both ै strokes red; foot picture after पैर; प → पै → पैर sounds | ✅ | `obj_pair` redrawn: bare foot with toes + ankle |
| 21 | 6 MEET_PAIR | Heading «ऐ की मात्रा वाले शब्द पढ़िए।»; बैल then भैंस with VO lines | ✅ | T5 |
| 22 | 6 | बैल with hump + horns; भैंस dark with curved horns, distinct | ✅ | both redrawn / new |
| 23 | 6 | Both ै strokes red; **ं in भैंस stays regular colour** | ✅ | new bindu exclusion in the in-word mask (verified render) |
| 24 | 7 TRAIN_TAP | Heading «“ए” की मात्रा वाले शब्द पर टैप कीजिए।»; train arrives, coaches सेब पैर बैल; VO after train stops | ✅ | G1 |
| 25 | 7 | Correct सेब: confetti, glow, े red, VO «शाबाश! सेब शब्द में ए की मात्रा है।» | ✅ | `hl_on_correct` |
| 26 | 7 | Hint 1: shake, no highlight/hand, VO «फिर से पढ़िए…» | ✅ | rung 1 |
| 27 | 7 | Hint 2: read all three L→R, highlight each matra, **retain** all highlights, VO «सेब। पैर। बैल।» + «ए की मात्रा वाले शब्द पर टैप कीजिए।» | ✅ | rung 2 + `keep_hl` |
| 28 | 7 | Hint 3: glow सेब, hand on it, lock others, VO «सेब शब्द में ए की मात्रा है। सेब पर टैप कीजिए।»; child taps | ✅ | rung 3 |
| 29 | 7 | After Hint 3: no extra VO | ✅ | `silent_on_late_correct` |
| 30 | 7 | "Enable आगे after the feedback finishes" | ⚑ | S01's flow is kept: no आगे on train screens — the train pulls out on its own after the feedback. Restoring आगे is one flag (`navOnCorrect`) |
| 31 | 7 | One wrong-tap counter across options; taps disabled during VO | ✅ | engine contract |
| 32 | 8 TRAIN_TAP | ऐ · पेड़ रेल बैग · correct बैग, same ladder + lines | ✅ | G2 (रेल stays here, as the deck lists it) |
| 33 | 9 TRAIN_TAP | Replace रेल with सेब → मेज़ पैन सेब · correct पैन, same ladder + lines | ✅ | G3 |
| 34 | 10 TRAIN_SORT | New words शेर बेर थैला पैसा with pictures; coaches labelled only ए / ऐ; two cards per coach | ✅ | G4, `multi` |
| 35 | 10 | Instruction VO, then each card's word read before interaction; tap = name, not an attempt | ✅ | `announce_items` |
| 36 | 10 | Correct: snap, sparkle, matra red, lock, matching praise line | ✅ | `hl_on_correct` |
| 37 | 10 | Hint 1 / 2 / 3 per card (counter per card); H2 reads the word with matra red (ा in थैला/पैसा stays navy); H3 glow + hand + other cards frozen + per-word line | ✅ | `h3_freeze`, per-item h3 clips |
| 38 | 10 | Completion: coaches glow, whistle + steam; "Enable आगे" | ✅ ⚑ | train departs on its own (S01 flow), see #30 |
| 39 | 11 TRAIN_SORT | Matra cards ◌े ◌ै into ए / ऐ coaches; no name on pick-up | ✅ | G5, cards carry no audio |
| 40 | 11 | Correct praise «शाबाश! यह ए की मात्रा है।» etc.; matra strokes red | ✅ | |
| 41 | 11 | H2: enlarge card, matra red, no name spoken, VO «मात्रा का आकार ध्यान से देखिए…» | ✅ | `h2_enlarge`, `h2_silent_name` |
| 42 | 11 | H3: glow card + coach, hand, lock, «यह ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।» | ✅ | |
| 43 | 12 WORD_BUILD | रेल → मेज़; blanks _ब _र _ज़ under apple/foot/table pictures; options से बै मे बे पै (रे removed) | ✅ | P1 (MATRA_FILL in new अक्षर mode) |
| 44 | 12 | Tap = akshar sound only; correct: snap, completed word with matra red, praise «शाबाश! सेब बन गया।» / «मेज़ बन गई।» | ✅ | `option_audio` |
| 45 | 12 | H1 shake + VO; H2 read only the dropped akshar, enlarge + matra red, then instruction | ✅ | new rung-2 branch |
| 46 | 12 | H3 glow correct akshar + blank, lock the rest, per-word line «से लगाने से सेब बनता है…» | ✅ ⚑ | counter is **per blank** (distractor and wrong-blank misses both count against the blank they were dropped on) |
| 47 | 12 | Practice hand on H3 — "confirm with Ankita; pending: glow + lock, no hand" | ⚑ | built as the pending default: **no hand** |
| 48 | 12 | Completion: unused distractors stay, disabled; coaches glow, whistle | ✅ | `tt-spent` |
| 49 | 13 TRAIN_SORT | रेल picture → शेर; pictures पैन मेज़ शेर बैग, no names on screen; heading/VO «चित्र का नाम सुनिए…» | ✅ | P2 `hide_labels` |
| 50 | 13 | H1 replays the picture's name: «फिर से सुनिए। पैन। चित्र को…» | ✅ | per-item `hint1_audio` |
| 51 | 13 | H2 shows the word temporarily under the picture with matra red, kept until placed | ✅ | `h2_show_word` |
| 52 | 13 | H3 glow + lock, no hand (pending ruling), per-item line | ✅ ⚑ | see #47 |
| 53 | 15 (deleted) | Sentence «मेरे ___ में दर्द है।» | ✅ | not built |
| 54 | 17 SENTENCE | मैं ___ से लिखता हूँ । options पैन पेड़ बैल; correct पैन | ✅ | P3 (new SENTENCE_COMPLETE module) |
| 55 | 17/14/16 | Picture first, sentence with blank, options fade in one by one, instruction + sentence VO (blank not spoken) before interaction | ✅ | sentence clip reads «… » as a pause |
| 56 | 17/14/16 | Tap = name; drag = answer; correct: snap, glow, confetti, praise line | ✅ | |
| 57 | 17/14/16 | H1 shake + VO; H2 read sentence with each option previewed (neutral) + scene detail highlighted; H3 glow + lock + line; one counter | ✅ | scene spotlight boxes measured on each picture |
| 58 | 14 SENTENCE | बगीचे में एक बड़ा ___ है। · पेड़ बैल पैन | ✅ | P4 |
| 59 | 16 SENTENCE | मुझे ___ खाना अच्छा लगता है। · सेब बैग मेज़ | ✅ | P5 |
| 60 | 14/16/17 | Practice hand on H3 pending | ⚑ | no hand, as #47 |
| 61 | 18 Celebration | — | N/C | S01 celebration Swiftie, line unchanged |

## Changed beyond the deck (each deliberate, from the "same as S01" brief)

* **S01's watch-only drag demonstration** sits before page 10 (सेब → ए, पैर → ऐ), as in S01's flow.
* **No आगे on the train screens** (pages 7–13): the train departs after feedback, as in S01.
* Coach labels / picture plates / tray / cover / gate / celebration all take S01's look.
* phase distribution recomputed (tutorial 5 · guided 6 · practice 5) after the deletion + demo.

## Ear-check before delivery

* Single-word and single-akshar clips (`vo_name_*` for सेब पैर बैल रेल बैग पैन शेर बेर थैला पैसा,
  `vo_ak_*` से बै मे बे पै) were synthesised as one list and sliced at the pauses, because the TTS
  voice refuses a lone word. Order was checked by segment count; **a human should play them once**.
* Sentence clips that needed the refusal ladder are listed in `_tts_ear_check.txt`.

## Verification (2026-10-07)

* **Build:** `17 slides · 119 audio ids · 17 images · phases {tutorial 5, guided 6, practice 6}` —
  `PENDING VO (0) · PENDING ART (0)`; engine guard 21/21 features present.
* **Played in headless Chrome with audio stubbed to short beats:** all five teaching screens run
  to the end and unlock आगे; on G1, G4, G5, P1, P2, P3 the ladder was walked wrong → wrong → wrong →
  right: rung-1 line · rung-2 demonstration + line · rung-3 per-item line with glow/lock · silent
  success after rung 3 · G1's train departs to the next page · P3's आगे unlocks. Screenshots in
  `_review_shots/end_states/` and `_review_shots/hint_ladders/`.
* **Not click-tested by a human yet** — real touch-drag on a device, and the audio itself (see
  ear-check above and `_tts_ear_check.txt`).
* `_verify_assets.py`: `3 FAIL 0 WARN` — all three are the sentence scenes reported "100% opaque",
  which is correct for full illustrations (the checker assumes cut-outs). No truncated clips.
* Console: two 404s remain, `sfx_pop_soft.ogg` and `sfx_fb_correct.ogg`. The engine falls back to its
  synthesised tones for both — S01 ships the same way.

## Deliverables added 2026-10-16

* **Review deck:** `HI02H11_L02_S03_REVISED_review.pptx` (this folder) — title + 18 pages, one
  screenshot each with the per-page note; stamped with the build it reviews (`da1e32bed502`).
* **Delivery copy:** `../dist/HI02H11_L02_S03/` — `index.html` + only the assets the game requests.
  VO re-encoded to Opus 32 kbps mono (19 MB → 2.3 MB), pictures palette-quantised (3.9 MB → 0.4 MB,
  no visible banding). **15 MB total — still over the ~10 MB cap**: ~11 MB of it is S01's animated
  Swiftie / train chrome (`new_landing_swiftee_anim`, `peeking`, `train_spritesheet`, `train_still`,
  `cel_*`, `gate_peek`, `sw_*_anim`), shipped unchanged. Smoke-tested: all 17 screens mount, Opus
  clips decode, no broken images; only `sfx_pop_soft.ogg` 404s (engine falls back to a tone, as in S01).
* The draft's quarantined audio/images moved out of the build to `../../_backup_draft1/_quarantine_from_build/`.
