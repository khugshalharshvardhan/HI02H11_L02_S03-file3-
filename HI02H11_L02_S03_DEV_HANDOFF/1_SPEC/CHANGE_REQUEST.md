# Change request — HI02H11_L02_S03 · ए / ऐ

Every item below traces to a note in [`_SME_RECOMMENDATIONS.md`](_SME_RECOMMENDATIONS.md), which is
verbatim. Where this document says something the notes do not, it is marked **⚠️ OPEN** or
**CONFLICT** — those are decisions, not instructions, and nobody should implement them unread.

**Do not start coding from this file alone.** It is a map of the notes, not a replacement for them.

---

## 1. The big one: the hint ladder becomes THREE rungs

This is the change that touches every test screen and most of the engine.

### What is in the build today

| | |
|---|---|
| miss 1 | shake + hint1 VO, no hand |
| miss 2 | shake + hint2 VO, glow on the correct answer, hand (guided only) |
| correct on the 3rd | celebrate, silent |

### What the notes ask for

| | |
|---|---|
| **Hint 1** — after the 1st wrong | shake the chosen item, return it. **No matra highlight, no glow, no hand.** VO re-asks the question. All options stay open. |
| **Hint 2** — after the 2nd wrong | shake and return. **Read the options and highlight their matras in red** — the teaching-screen style. Highlights **stay on screen** so the child can compare. Still no glow on the answer, still no hand. All options stay open. |
| **Hint 3** — after the 3rd wrong | shake and return. **Glow the correct answer**, **lock the distractors**, VO states the answer and tells the child what to do. **The child still has to perform the action** — never auto-place, never auto-advance. |
| after a Hint-3 completion | sparkle + chime, keep the matra highlighted, enable आगे. **No extra VO** — Hint 3 already said it. |

Hint 2 is not the same everywhere, and the difference is deliberate:

| screen type | what Hint 2 reads and highlights |
|---|---|
| TRAIN_TAP | **all three** words, left to right, each one's matra highlighted, all kept |
| TRAIN_SORT, WORD_BUILD | **only the wrongly dropped** item |
| SENTENCE_COMPLETE | **the whole sentence with each option in turn**, previewed in the blank, plus a highlight on the matching detail in the scene. The notes call this out as the deliberate exception, because this screen tests meaning, not the matra. |

### Engine work

`makeHints()` in `4_ENGINE/train_modules.js` currently has two rungs. It needs:

- a third rung, and a per-screen recipe for what each rung shows (the rungs are no longer one shape);
- **locking**: Hint 3 disables the distractors, and on the multi-item screens it also freezes the
  other unfinished items until the guided placement is done;
- **never auto-complete** — the notes repeat this on every screen;
- **input lock while any VO plays**, on every screen. Stated in every set of Developer Notes. The
  build has this on some paths only.
- the "no VO after a Hint-3 completion" rule, which is not the same as today's
  `silent_on_late_correct` — that one is keyed on attempt count, this one on *how* the child got there.

---

## 2. Attempt counters — this REVERSES a change made last week

The notes are precise, and they do not all agree with each other by design:

| screen | counter |
|---|---|
| TRAIN_TAP | **one per screen.** "Switching from पैर to बैल must not reset the counter." |
| SENTENCE_COMPLETE | **one per screen.** "Switching between बैल and पैन must not reset the counter." |
| TRAIN_SORT | **one per card.** "Each new card starts at zero." Unfinished cards keep their counters when the child switches. |
| WORD_BUILD | **one per correct अक्षर** (से, पै, मे) — *and* a separate counter per blank for the distractors बै/बे, which "must not reset" when the child swaps one distractor for the other. |

> **CONFLICT with the current build.** The build escalates **per screen on every screen**
> (`level = max(this item's misses, 2 once the screen has seen 2)`). That was a deliberate fix — the
> old per-card counter meant a child who missed two different cards once each heard Hint 1 twice and
> never earned the help. The notes now ask for per-card on the drag screens. Both readings are
> defensible; the notes win, but the hole that fix closed comes back, so **Hint 3 must be reachable
> per card** or a struggling child still gets no reveal. Flagging rather than choosing.

Not counted as an attempt, everywhere: a name-only tap, and a release outside any drop zone.

---

## 3. Words and pictures

| page | change | art |
|---|---|---|
| 3 · MATRA_BUILD ए | «सब» now needs a **picture**: three children under **one soft outline**, plus the VO «ये सब बच्चे हैं।» | **NEW** |
| 4 · MEET_PAIR ए | examples change from सेब, पेड़ → **मेज़**, पेड़ | have both |
| 5 · MATRA_BUILD ऐ | «पर» now needs a picture: **a book resting on a table**, VO «मेज़ पर किताब रखी है।» | **NEW** |
| 6 · MEET_PAIR ऐ | examples change from पैर, बैल → बैल, **भैंस** | **NEW** (भैंस) |
| 9 · TRAIN_TAP mixed | रेल → **सेब**; options become मेज़, पैन, सेब | have all |
| 10 · TRAIN_SORT word | whole set replaced: **शेर, बेर, थैला, पैसा** | **4 NEW** |
| 12 · WORD_BUILD | रेल → **मेज़**; third blank `_ल` → `_ज़`; options से, बै, मे, बे, पै — **रे out, बे in** | have मेज़ |
| 13 · TRAIN_SORT picture | रेल picture → **शेर**; set becomes पैन, मेज़, शेर, बैग | शेर shared with p10 |
| 14/16/17 · SENTENCE | see §4 | — |

**रेल is dropped from the lesson entirely** — the notes say it is confused with the train the game
is set on. `obj_rail.png` becomes unused; quarantine it, do not delete it.

**7 new images:** सब (group of children), पर (book on table), भैंस, शेर, बेर, थैला, पैसा.
Generate with `gen_objects.py`; the group/scene ones may need `gen_art.py --no-key`. Read
`_ART_RULES.md` **before** generating — in particular the one-connected-shape rule, which a group
of three children breaks by definition, so that one probably is not a chroma-keyed cut-out at all.

### ⚠️ CONFLICT: थैला and पैसा carry a second matra

Both end in **ा**. `guard_single_matra` in the builder fails the build on any word carrying more
than one matra, and that guard is exactly why थैला, पैसा, केला and मैना were excluded when this
lesson was first built: on a sort screen "which matra does this word have?" has no single answer.

The SME has clearly thought about it — the Hint-2 note says *"In थैला and पैसा, keep ा in the
regular text colour. The comparison here is between े and ै."* So this is a deliberate override,
not an oversight.

**Action:** relax the guard from *"exactly one matra"* to *"exactly one of े / ै"*, and record the
ruling in the builder next to the guard. **Do not just delete the guard** — it still has to catch a
word carrying both े and ै.

---

## 4. The deck itself changed

| | |
|---|---|
| **Page 15 deleted** | «मेरे ___ में दर्द है।» → **पैर**. The sentence screen is cut. |
| Pages reordered | 13 → 17 → 14 → 16 → 18 |
| Sentence screens left | **3**: पेड़ (page 14), सेब (page 16), पैन (page 17) |

> **Position 15 of the deck carries two recommendations in one notes field** — the page-14 one
> (बगीचा/पेड़), a pasted chat timestamp, then the page-17 one (लिखना/पैन). Position 16 repeats the
> page-14 one. The duplication is in the source file; the substance is not ambiguous.

> **⚠️ OPEN — the ए/ऐ split.** With पैर gone the three sentences are पेड़(े), सेब(े), पैन(ै) —
> **2 ए to 1 ऐ**. `guard_sentences` asserts an even split and **will fail the build**. Either accept
> the 2:1 and relax the guard, or add a ऐ sentence back. That is the SME's call.

---

## 5. ⚠️ OPEN — the hand on Hint 3 in practice

The notes raise this themselves, three times, and name the person:

> *"Confirm with Ankita whether Hint 3 should include a hand drag nudge. Pending confirmation, use
> glow and lock without a hand, following the earlier practice QA feedback."*

Where this lands:

- On **guided** screens the notes are unambiguous — the hand appears, but **only at Hint 3**. That is
  a change from today (hand at Hint 2) and it is a straight edit.
- On **practice** screens the pending default — glow and lock, no hand — is **already what the engine
  does**. `handOnAnswer()` gates on `HAND_PHASES = {tutorial, guided}` under ruling [28f], after a
  hand reached round 3 three times and was re-reported as fixed each time.
- **If the hand is approved for practice, this is not a card change.** It means editing
  `HAND_PHASES` in the shared engine, which is Yasir's ruling, not Ankita's. Route it to him before
  anyone writes the code.

---

## 6. Smaller items worth not losing

- **Landing VO changes** to «हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।»
- ⚠️ The page-1 note says *"First show ु, followed by ू."* Those are the **उ/ऊ** matras — a
  copy-paste leftover from the sibling lesson. It should read **े then ै**. Everything else on that
  page is about ए/ऐ. Confirm, then build the obvious reading.
- «छोटी» / «बड़ी» must not appear anywhere — repeated on several pages. Already true in the build;
  `guard_register` should be extended to catch it so it stays true.
- The **dotted circle** in ◌े is a display aid only. It must **disappear when the matra joins the
  consonant** (page 3), and must never be highlighted red.
- **Nukta:** `ज़` in `_ज़` / `मेज़` must survive; highlight the matra only, never the nukta.
- **Anusvara:** the ं in भैंस stays in the regular colour.
- Page 13 heading and VO: «चित्र को सुनिए» → **«चित्र का नाम सुनिए»**.
- Page 13 Hint 2 **temporarily shows the wrongly dropped picture's name** and then removes it. This
  is the one place a word appears on the pictures-only screen, and it is intended.
- Train entry, whistle and steam are asked for again on every screen — already built.

---

## 7. Voice-over

The build ships **88 clips**. Essentially every hint clip is replaced, and Hint 3 adds a reveal line
**per item** on the multi-item screens, so the new list is materially longer. The exact list falls
out of the builder once the card is updated — generate it there rather than counting by hand.

Two traps from this lesson's own history, both in `4_ENGINE/CHANGES.md`:

- an em-dash before a short final word **truncates the clip**, and the truncation is invisible to
  every existence and file-size check — only peer comparison by text length catches it;
- bare aksharas can be refused outright by the voice (बै needed a fallback voice).

The notes ask for several new bare-akshara option clips (बे, मे, पै, बै, से). Expect refusals.

---

## 8. Suggested order of work

1. Get the two ⚠️ OPEN rulings — the practice hand, and the 2 ए / 1 ऐ sentence split.
2. Relax `guard_single_matra` to *"exactly one of े / ै"* with the ruling recorded.
3. Update the card: words, pictures, headings, VO text, the deleted screen. Build. It will fail on
   the guards until the art exists — that is the guards working.
4. Generate the 7 new images. Read `_ART_RULES.md` first.
5. Rework `makeHints()` to three rungs with per-screen recipes, locking and the input lock.
6. Re-record. Peer-compare clip lengths before shipping.
7. Re-screenshot and rebuild the review deck.
