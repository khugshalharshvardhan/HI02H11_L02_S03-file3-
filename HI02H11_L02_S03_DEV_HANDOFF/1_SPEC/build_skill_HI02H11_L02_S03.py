# -*- coding: utf-8 -*-
"""Build HI02H11_L02_S03 (ए / ऐ) — «मात्राओं की रेल».

[S03 · 2026-10-16] THIS FILE IS HI02H11_L02_S02's BUILDER (github CodeWithPiyush0/
HI02H11_L02_S02_DEV_HANDOFF @ 992e684) WITH THE S03 CONTENT SWAPPED IN. The flow, the screen
logic, the guards, the gate / celebration / runner wiring are S02's, unchanged, as asked: "make my
file look exactly similar and functional with the logics of that file". The words, pictures and
Hindi lines are the S03 SME deck's. The S02 notes below are kept for the reasoning behind each rule.
Converted by 1_SPEC/_make_s03_builder.py.


Curriculum: Hindi_content progression.xlsx row 56.
    Part-1: उ, ऊ मात्रा वाले शब्द पढ़ता है।   (Part-2 is ए / ऐ — a separate build)

=======================================================================================
ROUND 3 — built to `HI02H11_L02_S02_SME_Review.pptx` (reviewed 2026-09-22).
=======================================================================================
The SME's words are recorded verbatim in `_SME_RECOMMENDATIONS_ROUND3.md`; the engineering
reading is `CHANGE_REQUEST_ROUND3.md`; the row-by-row contract this build is checked against is
`../CHANGES.md`. Where the first two disagree, the verbatim file wins.

WHAT CHANGED FROM ROUND 2, AND WHY EACH ONE IS HERE

  · **Two screens deleted.** The deck carries a slide and a note for every page it keeps. Pages 7
    (CONTRAST_PAIR, फुल ≠ फूल) and 8 (the third MEET_PAIR, सूरज · मुकुट) have neither.
    CONTRAST_PAIR was my substitution for the third build screen S01 has and this skill does not;
    the SME has now answered that question by deleting it. Both modules stay registered in the
    engine — nothing else mounts them, and removing them would change the engine for the sibling
    lessons on this line.

  · **The poem is gone.** POEM_SEARCH was ours, not theirs. Four SENTENCE_COMPLETE screens replace
    it: the child reads a sentence and picks the word that completes it. It is the only screen in
    the lesson where the matra is not the visible question, which is what makes it a test of
    reading rather than of spotting a mark.

  · **MATRA_FILL → WORD_BUILD.** Round 2 dragged a bare `ु` into `प_ल`. Round 3 drags a whole
    अक्षर into a blank that now sits FIRST — `_ल` + `पु`. Harder and more useful: it forces a
    choice between पु and फू, which is the exact ह्रस्व/दीर्घ confusion the curriculum row names.

  · **Register flips तुम → आप, everywhere.** The SME says so twice in as many words. It also
    settles a question open since round 1: the three phase-gate clips the engine plays between
    phases are shared fleet-wide and already speak आप, so round 2's तुम made a Grade 2 child
    switch register at every gate. `guard_register` fails the build if a तुम form survives.

  · **Coach labels lose छोटी / बड़ी.** On screen only — the VO still says छोटी उ / बड़ी ऊ.

  · **Praise goes per item.** On every sort and build screen the SME writes the praise line card
    by card («शाबाश! 'सुई' शब्द में उ की मात्रा है।») and asks for no completion line at all, so
    the last card's own line is the last thing the child hears.

  · **The train reaches the landing and the intro.** «The matras can be shown inside two train
    bogies … so that the lesson visually continues as a मात्राओं की रेल journey.»

THREE THINGS THIS BUILD DELIBERATELY DOES NOT DO

  1. **The hand on practice screens.** The SME asks for a hand nudge on the 2nd wrong attempt on
     every test screen. The engine carries a signed-off ruling ([28f], Yasir 2026-07-28): the hand
     is allowed in tutorial and guided and never in practice. Confirmed with the user 2026-09-23:
     keep [28f]. Practice screens therefore get the coach/option GLOW and pulse — which is ours
     and is not phase-gated — and the hand is withheld. Every nudge routes through
     `handOnAnswer()`, the single place that rule can be enforced.
  2. **Painted art for the train.** The landing mockup draws a painted locomotive and bogies. The
     interactive trains are SVG/CSS because coaches recolour, glow, shake, lock and accept drops,
     which a flat PNG cannot do. Confirmed: painted treatment on the landing and the intro only —
     and those two ship as the DRAWN train now, because a painted PNG needs a generation run.
     Swapping it in later is a background-image change on `.lt-*` / `.mi-*` and nothing else.
  3. **Rewriting the SME's Hindi to dodge a TTS bug.** Their MEET_PAIR lines are written
     «गुड़, बोलकर देखिए। इसमें …», the exact em-dash-before-a-short-word shape that makes the
     model truncate a clip (measured: 0.73–1.05 s against a 1.53–2.21 s peer median). Their
     wording ships; the clips are flagged for the duration check instead. `_verify_assets.py` is
     the only thing that catches a truncated clip — run it.

ENGINE. Pinned to this handoff's own `4_ENGINE/lesson_template.html`, which carries the train
module set. Everything is additive — new entries on `SlideModules` plus one CSS block — so every
other lesson on this engine line renders byte-identically.

⚠️ NEITHER MATRA CAN BE HIGHLIGHTED BY THE ENGINE'S COLUMN CLIP. ु and ू are BELOW-BASE marks
sharing their consonant's columns, so a pixel-column highlight colours the NEXT letter. Measured:
पुल puts 11342 red px ON THE ल. `matraHL()` clips in two dimensions instead, and is what every
highlight in this lesson goes through. `guard_engine` hard-fails if either mark is ever added to
RIGHT_SPACING_MATRAS, because that failure is silent and looks like the feature working.

Run:  PYTHONUTF8=1 python 1_SPEC/build_skill_HI02H11_L02_S02.py   (from the handoff root)
"""
import hashlib
import os, re, sys, json, argparse
import array
import contextlib, wave        # [r8] page-1 matra cue, measured off the clip

CODE     = "HI02H11_L02_S03"
# ---------------------------------------------------------------- paths
# SELF-CONTAINED HANDOFF LAYOUT. The original script built inside the wider SwiftPAL factory
# (`<factory>/G2/<CODE>/` against `<factory>/KG and G1 refernce ready HTML's`). This handoff folder
# is deliberately standalone — README: "This folder is self-contained" — so every path below
# resolves INSIDE it and nothing reaches out to the factory:
#     1_SPEC/           this script
#     3_CURRENT_BUILD/  the bundle  (HTML + card.json + assets/)
#     4_ENGINE/         the pinned engine copy + the train module sources
HANDOFF  = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUNDLE   = os.path.join(HANDOFF, "3_CURRENT_BUILD")
ENGINE   = os.path.join(HANDOFF, "4_ENGINE", "lesson_template.html")
SPEC_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BUNDLE, "assets", "Images")
AUD_DIR  = os.path.join(BUNDLE, "assets", "Audio")
CARD_TAG = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)
VER_RE   = re.compile(r'ENGINE_VERSION\s*=\s*["\']([^"\']+)["\']')
RSM_RE   = re.compile(r'RIGHT_SPACING_MATRAS\s*=\s*new Set\(\[([^\]]*)\]\)')

# CONTRAST_PAIR, POEM_SEARCH and MATRA_FILL are no longer mounted by this card — round 3 deleted
# or replaced their screens. They stay in this list because the guard is a PRESENCE check on the
# engine copy: if the injector ever ran short, that is what tells us.
TRAIN_MODULES = ["TRAIN_TAP", "TRAIN_SORT", "MATRA_FILL", "MATRA_BUILD",
                 "MEET_PAIR", "CONTRAST_PAIR", "POEM_SEARCH", "MATRA_INTRO",
                 "WORD_BUILD", "SENTENCE_COMPLETE", "MATRA_PAIRS"]
STOCK_MODULES = ["CELEBRATION"]
# Fixed clips that are not recorded for this lesson. The three sfx_train_*/whistle files are
# REAL RECORDINGS brought over from the sibling lesson HI02H11_L02_S01; round 3 previously
# synthesised the train sounds with the engine's _tone(), which gives a two-note beep rather than
# the "soft train arrival / whistle SFX" the SME asks for on the landing and on every train screen.
COPY_AUDIO = ["vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice",
              "sfx_celebrate", "sfx_correct", "sfx_wrong", "sfx_tap", "sfx_pop",
              "sfx_fb_correct", "sfx_fb_incorrect",   # [r73] Yasir's feedback sounds
              "sfx_play_button", "sfx_next_button",   # [r84] Yasir's play / next button sounds
              "sfx_train_arrive", "sfx_train_move", "sfx_whistle",
              "sfx_whoosh"]                           # [r142] the transition screen's swish

# [S03] the two slots keep S02's names so every rule below reads unchanged: U is ए's matra, UU ऐ's
U, UU = "े", "ै"

# ---------------------------------------------------------------- content
# key -> (word, emoji, matra). Every word carries exactly ONE target matra — the task is
# "which matra does this word have", so a two-matra word has no single right answer. This is
# why the G1 उ/ऊ lesson's कुत्ता / गुलाब / मूली / जूता / भालू are all unusable here.
OBJ = {
    "obj_seb":    ("सेब",  "\U0001F34E", U),
    "obj_ped":    ("पेड़",  "\U0001F333", U),
    "obj_mez":    ("मेज़",  "\U0001FA91", U),
    "obj_sher":   ("शेर",  "\U0001F981", U),
    "obj_ber":    ("बेर",  "\U0001FAD2", U),
    "obj_rail":   ("रेल",  "\U0001F682", U),     # page 8 lists it (word only, no picture shown)
    "obj_pair":   ("पैर",  "\U0001F9B6", UU),
    "obj_bail":   ("बैल",  "\U0001F402", UU),
    "obj_bag":    ("बैग",  "\U0001F392", UU),
    "obj_pen":    ("पैन",  "\U0001F58A", UU),
    "obj_bhains": ("भैंस", "\U0001F403", UU),
    "obj_thaila": ("थैला", "\U0001F45C", UU),    # carries ा too - the SME: keep ा navy, compare े/ै
    "obj_paisa":  ("पैसा", "\U0001FA99", UU),
}

# Full illustrated SCENES — a new asset class in round 3, and not the same thing as the cut-out
# objects above. `gen_objects.py`'s magenta chroma-key pipeline exists to cut a subject OUT of its
# background; these have a background on purpose, so they must be generated flat and full-bleed
# and must NOT go through keying.
SCENE = {
    "scn_likhna":    "\U0001F58A",
    "scn_bageecha":  "\U0001F333",
    "scn_seb_khana": "\U0001F34E",
}

MATRA_VO   = {U: "vo_matra_e", UU: "vo_matra_ai"}
LETTER_VO  = {U: "vo_letter_e", UU: "vo_letter_ai"}
LETTER_TEXT = {"vo_letter_e": "ए", "vo_letter_ai": "ऐ"}
# rung-2 scene glow, as fractions of the artwork (cx, cy, rx, ry) - read off the shipped 1024² scenes
SCENE_GLOW = {
    # [2026-10-22] re-measured on the replacement scenes the user supplied
    "scn_likhna":    [[0.410, 0.440, 0.065, 0.090]],   # the pen in his writing hand
    "scn_bageecha":  [[0.570, 0.430, 0.330, 0.430]],   # the big tree, trunk and canopy
    "scn_seb_khana": [[0.570, 0.400, 0.065, 0.075]],   # the apple at his mouth
}
MATRA_TEXT = {"vo_matra_e": "ए की मात्रा", "vo_matra_ai": "ऐ की मात्रा"}
MATRA_TEXT.update(LETTER_TEXT)
MATRA_NAME = {U: "ए", UU: "ऐ"}      # the deck: «ए की मात्रा» / «ऐ की मात्रा», never छोटी / बड़ी
LETTER     = {U: "ए", UU: "ऐ"}

AUDIO_TEXT = {}
TEXT2ID    = {}
PENDING_ART = []


def vo(vid, text):
    if vid in AUDIO_TEXT and AUDIO_TEXT[vid] != text:
        raise ValueError("clip %s registered twice with different text:\n  %s\n  %s"
                         % (vid, AUDIO_TEXT[vid], text))
    AUDIO_TEXT[vid] = text
    return vid


def once(vid, text):
    """One clip per LINE, never per slide.

    Round 3 repeats several lines verbatim across screens — the tap prompt on screens 6 and 8, the
    sort hint on screens 9 and 12, all three shared lines on the four sentence screens. Keying by
    TEXT means each is recorded once, so two screens can never end up speaking the same sentence
    in two different takes. (Round 2 keyed these by slide and recorded the tap prompt three times.)
    """
    if text in TEXT2ID:
        return TEXT2ID[text]
    TEXT2ID[text] = vid
    return vo(vid, text)


def slug(key):
    return key.split("_", 1)[1] if "_" in key else key


def pic(key):
    """The image key if its PNG is on disk, else None so the engine renders the emoji instead.

    ROUND 3 ADDS SEVEN PICTURES THAT DO NOT EXIST YET (§6 of the change request): धनुष, खुश, सुबह
    and the four scenes. They need a generation run with an API key, which this build does not
    have. Rather than ship seven references that 404, the card carries the emoji fallback for
    anything not yet drawn, and the key lights up by itself the moment the PNG lands and this
    script is re-run. What is still missing is printed at the end of the build and written into
    `_art_manifest.json`, so the art run has a work list.
    """
    if os.path.isfile(os.path.join(IMG_DIR, key + ".webp")):   # [r126] every picture is WebP
        return key
    if key not in PENDING_ART:
        PENDING_ART.append(key)
    return None


def key_of(word):
    for k, v in OBJ.items():
        if v[0] == word:
            return k
    sys.exit("X  no OBJ entry for %r" % word)


# The MATRA_BUILD base words, kept OUT of OBJ on purpose. OBJ is "words that carry exactly one
# target matra" and `guard_single_matra` audits it as such; पल and फल carry none, because they
# are the form BEFORE the matra. They still want a picture - a child reading पल with nothing
# beside it has no idea the word means anything, and the sibling's base panel has art - so they
# live here, where no matra guard can trip over them.
BASE_OBJ = {
    "सब": ("obj_sab", "🧒"),   # three children in one soft outline (page 3)
    "पर": ("obj_par", "📘"),   # a book resting on a table (page 5)
}


def key_of_opt(word):
    """key_of() but returns None instead of exiting.

    Looks in BASE_OBJ as well as OBJ: the MATRA_BUILD base words are not vocabulary the child is
    being taught, so they are not in OBJ, but they do have art of their own."""
    for k, v in OBJ.items():
        if v[0] == word:
            return k
    if word in BASE_OBJ:
        return BASE_OBJ[word][0]
    return None


def matra_of(word):
    for _k, (w, _e, m) in OBJ.items():
        if w == word:
            return m
    sys.exit("X  no matra known for %r" % word)


def name_clip(word):
    """One clip per WORD, never per slide — a line used twice is recorded once."""
    return vo("vo_name_" + slug(key_of(word)), word)


# ---------------------------------------------------------------- screens

def _matra_cue_ms(audio_id, line, phrase="इसकी"):
    """When, inside `line`'s recording, the phrase «इसकी मात्रा है» starts — in ms.

    Page 1's highlight has to land ON THE WORDS, and a fixed delay cannot do that: the two clips
    are 4.13s and 3.85s, so any constant is early on one and late on the other. There is no forced
    aligner in this toolchain, so the cue is the clip's REAL duration scaled by where the phrase
    begins in the text. Devanagari is close enough to evenly paced for one sentence of this length,
    and the highlight is a 1.2s glow — it only has to start inside the right phrase, not on the
    exact sample.

    Computed from the file on disk, so a re-recorded clip recomputes its own cue and a missing one
    falls back to a delay that is at least not wrong in the same direction every time.
    """
    path = os.path.join(AUD_DIR, audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            secs = w.getnframes() / float(w.getframerate())
    except Exception:
        return 1300                      # a plausible middle for a ~4s line, flagged by the receipt
    i = line.find(phrase)
    if i < 0:
        return int(secs * 1000 * 0.35)
    # strip spaces on both sides of the split: they are not spoken and there are more of them in
    # the second half, which would otherwise push the cue late
    before = len(line[:i].replace(" ", ""))
    total  = len(line.replace(" ", ""))
    return int(secs * 1000 * (before / float(total)))

def _sound_cues_ms(audio_id, n):
    if not audio_id:                 # [QA] a build screen may have no «स। से। सेब।» line
        return None
    """Where each of the `n` sounds STARTS inside «प। पु। पुल।» — in ms.

    This one clip is not prose, it is three sounds with deliberate silence between them, and that
    silence is measurable. So unlike `_matra_cue_ms`, which has to estimate from character
    proportion because a sentence has no gaps to find, this reads the ACTUAL onsets: scan for
    runs of audible samples separated by quiet, and take where each run begins.

    The note asks for the difference between प, पु and पुल to be unmistakable. Lighting each
    part of the equation exactly as its own sound is spoken is what makes it so; lighting the whole
    equation for all three says nothing about which is which.

    Returns None when the clip does not resolve into exactly `n` runs — better for the screen to
    fall back to a single glow than to flash the wrong element confidently.
    """
    path = os.path.join(AUD_DIR, audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            if w.getsampwidth() != 2 or w.getnchannels() != 1:
                return None
            sr = float(w.getframerate())
            a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
    except Exception:
        return None
    if not len(a):
        return None
    # frame-wise energy; the threshold is relative to the clip's own peak so a quiet take and a
    # loud one segment the same way
    hop  = max(1, int(sr * 0.01))
    peak = max(1, max(abs(v) for v in a))
    loud = [max(abs(v) for v in a[i:i + hop]) > peak * 0.10
            for i in range(0, len(a) - hop, hop)]
    runs, i, minq = [], 0, int(0.18 / 0.01)        # 180ms of quiet ends a sound
    while i < len(loud):
        if loud[i]:
            j = i
            q = 0
            while j < len(loud) and q < minq:
                j += 1
                q = 0 if (j < len(loud) and loud[j]) else q + 1
            runs.append(i)
            i = j
        else:
            i += 1
    if len(runs) != n:
        return None
    return [int(r * 0.01 * 1000) for r in runs]


def _voice_runs_ms(audio_id, quiet_s=0.30):
    """[r121] Where each spoken PHRASE in a clip starts, in ms - the runs of sound between pauses.

    Same reading as `_sound_cues_ms`, but it returns every run instead of insisting on `n`, with a
    longer pause (300 ms) closing a phrase, so the short gaps inside a phrase do not split it.
    Page 1's two lines are four phrases each - «यह है» · «उ» · «इसकी मात्रा है» · «ु» - and the ask
    is that the letter appears on the 2nd and the matra on the 4th. Returns [] if the clip is not
    readable, and the caller falls back to its proportional estimate.
    """
    path = os.path.join(AUD_DIR, audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            if w.getsampwidth() != 2 or w.getnchannels() != 1:
                return []
            sr = float(w.getframerate())
            a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
    except Exception:
        return []
    if not len(a):
        return []
    hop  = max(1, int(sr * 0.01))
    peak = max(1, max(abs(v) for v in a))
    loud = [max(abs(v) for v in a[i:i + hop]) > peak * 0.10
            for i in range(0, len(a) - hop, hop)]
    runs, i, minq = [], 0, int(quiet_s / 0.01)
    while i < len(loud):
        if loud[i]:
            j, q = i, 0
            while j < len(loud) and q < minq:
                j += 1
                q = 0 if (j < len(loud) and loud[j]) else q + 1
            runs.append(int(i * 10))
            i = j
        else:
            i += 1
    return runs


def s_intro(sid):
    """Screen 1. «उ → ◌ु», one pair at a time — matched to the sibling lesson's page 1.

    NO HEADING AND NO TRAIN, both on the SME's instruction. Their note says "Remove the current
    extra heading text from the top … so the screen stays clean and focused" and "Do not add extra
    decorative elements"; the sibling (`HI02H11_L02_S01`), whose page-1 note is the same note,
    reads it the same way and draws two glyphs and an arrow on the bare stage. The train belongs
    to the screens that need coaches to sort into — this screen is two marks and the relationship
    between them.

    Pair by pair, letter first: «First उ appears, then ु appears beside it with a soft glow. After
    that, both can fade slightly / dim softly. Then ऊ appears, and ू appears beside it.» A pair
    already taught stays faded; the note never asks for it to be restored.

    `no_heading` is what lets `prompt_hi` be empty here. It is a per-SLIDE opt-out on purpose:
    round 2 hid the heading band globally and shipped 14 screens with a mascot beside nothing, so
    `guard_prompts` still fails on any empty heading that has not asked for it.
    """
    # SPOKEN vs SHOWN — deliberately not the same string. The SME gives the VO verbatim, with
    # छोटी/बड़ी: spoken, that is exactly what separates two vowels which sound alike. The heading
    # is the screenshot's own line, without them — printed directly above the two glyphs those
    # words are redundant, and they turn a short heading into a long one.
    p = "आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।"
    heading = p
    # `cue_ms` is when «इसकी मात्रा है» starts inside each clip. The matra is highlighted THEN,
    # rather than when it pops in - the ask is that the glow lands on the words that name it.
    # [QA] S02's page-1 script: «यह है उ। इसकी मात्रा है — ु।». A bare ◌े / ◌ै cannot be spoken, so the
    # line ends on «इसकी मात्रा है।» and the mark lands on screen as it is said.
    _u_line  = "यह है ए। इसकी मात्रा है।"
    _uu_line = "यह है ऐ। इसकी मात्रा है।"
    # [r121] Yasir: «when VO says "यह है उ" the letter appears, then it says "इसकी मात्रा है" and
    # the matra appears - all in sync with the VO». Each clip is four phrases with clear pauses
    # (measured: vo_pair_u 30 · 1260 · 2320 · 3970 ms), so the letter lands on the 2nd and the
    # matra on the 4th. A clip that does not read as 3+ phrases falls back to the old estimates.
    def _pair(letter, m, aid, line):
        r = _voice_runs_ms(aid)
        cue = _matra_cue_ms(aid, line)
        ok = len(r) >= 3
        return {"letter": letter, "matra": m, "audio": vo(aid, line), "cue_ms": cue,
                "letter_ms": r[1] if ok else 900,
                "arrow_ms": r[-2] if ok else cue,
                "matra_ms": r[-1] if ok else cue + 1100}
    pairs = [_pair("ए", U, "vo_pair_e", _u_line),
             _pair("ऐ", UU, "vo_pair_ai", _uu_line)]
    # HEADING OFF AGAIN (r7). It went on in r6 because the screenshot that came with that ask
    # had one; it comes off now because the ask is explicit. The sentence is still SPOKEN - it is
    # `p` below, the SME's own VO line - so nothing is lost from the lesson, only from the screen.
    # `heading` stays defined and unused on purpose: it is one edit away if the ask reverses
    # again, and it documents what the band would say.
    del heading
    return {"id": sid, "phase": "tutorial", "eis": "enactive", "type": "MATRA_PAIRS",
            "prompt_hi": "",
            # [r134] no opening line here any more - it moved to the cover (vo_landing)
            "audio": {},
            "data": {"pairs": pairs, "phonemes": dict(MATRA_VO), "auto": True,
                     "no_heading": True}}


def s_build(sid, base_word, base_slug, consonant, matra, syllable, result_word, sounds, base_more=""):
    """The transformation teach, respoken to the SME's round-3 wording.

    The note is explicit about the phrasing and rejects the alternative by name:
        "Please avoid awkward phrasing such as: «प में उ की मात्रा लगी, बना पु।»
         Use: «प के साथ छोटी उ की मात्रा लगाने पर 'पु' बनता है।»"
    Round 2 shipped «प के नीचे …». *के साथ*, then.

    The round-2 panel captions are GONE. The note's own "On Screen" list is पल, the equation, पुल
    and the picture, and it ends "Keep the screen clean and minimal. Do not add unnecessary
    explanatory text." The captions were carried over from S01's mockup and are exactly that.

    `explain` is gone too: its content is now inside `result` («अब 'ल' जुड़ने पर 'पुल' बनता है।»).
    `sounds` is new — the note's "Sound Differentiation" beat, प · पु · पुल with a pause between
    each, as ONE clip because three clips back to back lose the pause the note is asking for.
    """
    rk = key_of(result_word)
    g = slug(rk)
    a = {
        "prompt": vo("vo_%s_prompt" % sid.lower(),
                     "आइए, देखें कि %s की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।" % MATRA_NAME[matra]),
        # [S03] «यह शब्द देखिए — सब। ये सब बच्चे हैं।» (em-dash -> comma, the measured TTS rule)
        "base": vo("vo_base_" + base_slug, ("यह शब्द देखिए, %s। %s" % (base_word, base_more)).strip()),
        "matra_name": MATRA_VO[matra],
        "onset": vo("vo_onset_" + g,
                    "%s के साथ %s की मात्रा लगाने पर %s बनता है।"
                    % (consonant, MATRA_NAME[matra], syllable)),
        "result": vo("vo_result_" + g,
                     "अब %s जुड़ने पर %s बनता है।" % (result_word[-1], result_word)),
        "sounds": vo("vo_sounds_" + g, sounds) if sounds else None,
    }
    a = {k: v for k, v in a.items() if v}
    bk = key_of_opt(base_word)
    ONSET_LINE  = AUDIO_TEXT.get(a["onset"], "")
    RESULT_LINE = AUDIO_TEXT.get(a["result"], "")
    ON_RUNS, RE_RUNS = _voice_runs_ms(a["onset"]), _voice_runs_ms(a["result"])
    return {"id": sid, "phase": "tutorial", "eis": "symbolic", "type": "MATRA_BUILD",
            # NO HEADING. The deck gives this screen no "Heading" section — unlike the tap
            # screens, which say "Keep the heading at the top: …" — and tells it to "keep the
            # screen clean and minimal. Do not add unnecessary explanatory text." The sibling
            # lesson's equivalent screen carries none either.
            "prompt_hi": "", "audio": a,
            "data": {"base_word": base_word, "consonant": consonant, "matra": matra,
                     "syllable": syllable, "result_word": result_word,
                     "result_img": pic(rk), "result_emoji": OBJ[rk][1], "travel": "down",
                     # WHERE THE VISUALS BELONG INSIDE EACH LINE, so the screen follows the voice
                     # rather than running ahead of it. Both offsets are measured off the clip
                     # that exists, so a re-record moves them instead of leaving them stranded.
                     #   onset  «प के साथ … लगाने पर 'पु' बनता है।»  -> पु forms on «बनता»
                     #   result «अब 'ल' जुड़ने पर 'पुल' बनता है।»     -> ल joins on «जुड़ने»
                     "syl_ms":  _matra_cue_ms(a["onset"],  ONSET_LINE, "बनता"),
                     "join_ms": _matra_cue_ms(a["result"], RESULT_LINE, "जुड़ने"),
                     # «प। पु। पुल।» — which of the three is being said, at each moment.
                     # SME: "Make the pronunciation difference very clear."
                     "sound_ms": _sound_cues_ms(a.get("sounds"), 3),
                     # [r121] the equation panel is gone: the right-hand word takes the matra on
                     # «पु» (the onset line's last phrase) and its picture arrives on «पुल» (the
                     # result line's last phrase). Measured runs, so a re-record moves them too.
                     "drop_ms": (ON_RUNS[-1] if len(ON_RUNS) >= 2
                                 else _matra_cue_ms(a["onset"], ONSET_LINE, syllable)),
                     "pic_ms": (RE_RUNS[-1] if len(RE_RUNS) >= 2
                                else _matra_cue_ms(a["result"], RESULT_LINE, result_word)),
                     # [r131] the right-hand word is built ONE PIECE AT A TIME: प, then the matra
                     # (पु, on «पु» - drop_ms), then ल on «ल जुड़ने» - the result line's 2nd phrase when
                     # it reads as three («अब» · «ल जुड़ने पर» · «पुल बनता है»), else estimated
                     "tail_ms": (RE_RUNS[1] if len(RE_RUNS) >= 3
                                 else _matra_cue_ms(a["result"], RESULT_LINE,
                                                    "%s जुड़ने" % result_word[-1])),
                     "base_img": (pic(bk) if bk else None),
                     "base_emoji": (BASE_OBJ[base_word][1] if base_word in BASE_OBJ
                                   else (OBJ[bk][1] if bk else None)),
                     # SME: "Keep the screen clean and minimal. Do not add unnecessary
                     # explanatory text." The round-2 panel captions go.
                     "cap_base": None, "cap_mid": None, "cap_result": None,
                     "no_heading": True}}


def s_pair(sid, words, lead, lines):
    """Two example words, one at a time, each with its picture and its matra called out.

    ⚠️ THE EM-DASH IS GONE FROM THESE LINES, AND IT IS A MEASURED DECISION, NOT A PREFERENCE.
    The SME writes them as «गुड़, बोलकर देखिए। इसमें …», which puts an em-dash straight after a
    short word. Round 3 first shipped exactly that wording, on the grounds that silently rewriting
    a reviewer's Hindi is the worse failure — and then measured the result: all four came back at
    0.69-1.21 s against the ~5.4 s their length calls for. The model speaks the first word and
    stops. The sibling lesson HI02H11_L02_S01 hit the same wall and probed it head to head, same
    words, three takes each: em-dash 0.73-1.05 s · comma 1.53-2.21 s · danda 1.13-2.01 s, with the
    dash also carrying the worst refusal rate.

    So the dash becomes a COMMA and nothing else changes. No word is altered and the listener
    cannot hear the difference — the SME's sentence is intact. Verified on this lesson:
    vo_base_pal went from 0.69 s to 2.65 s on the same voice with only that substitution.
    Flagged to the SME as a punctuation change (CHANGES.md Q6); the sibling did exactly the same.

    The separate matra call-out clip is gone: round 3 folds it into the line itself.
    """
    ex = []
    for w, line in zip(words, lines):
        k = key_of(w)
        vid = "vo_meet_" + slug(k)
        # WHERE THE VISUALS BELONG INSIDE THE LINE. The note asks for the animation to follow the
        # voice - "word should appear first, then image", "when VO says the matra part, the ु
        # should glow". The line has three clauses and each one owns a beat:
        #     «गुड़,»               -> the word is on screen already
        #     «बोलकर देखिए।»        -> the picture arrives
        #     «इसमें ग पर … लगी है।» -> the matra lights
        # Both offsets are measured off the clip that exists, so a re-record moves them with it.
        ex.append({"word": w, "matra": matra_of(w), "img": pic(k), "emoji": OBJ[k][1],
                   "audio_line": vo(vid, line),
                   # [r134] the line is now «गुड़, | इसमें ग पर छोटी उ की मात्रा लगी है। | बोलकर देखिए।»:
                   # the picture comes with «इसमें» (the 2nd phrase), the matra lights on «छोटी / बड़ी»
                   "pic_ms":   ((_voice_runs_ms(vid) + [0, 0])[1] or _matra_cue_ms(vid, line, "इसमें")),
                   "matra_ms": _matra_cue_ms(vid, line, MATRA_NAME[matra_of(w)].split()[0]),
                   "matra_audio": None})
    return {"id": sid, "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
            # NO HEADING, same reasoning as the build screens: the deck gives this page no
            # heading, and the sibling's equivalent shows the word and its picture and nothing else
            "prompt_hi": "",
            "audio": {"prompt": vo("vo_%s_prompt" % sid.lower(), lead)},
            # [r134] the mic: if it is not tapped for 7 s, this line asks for it.
            # [r136] Yasir: "extract the same «इस बटन पर टैप कीजिए» VO from that repo" (HI02H04_L01_S01's
            # vo_tap_speaker_sentence_story, human voice). It says «… और वाक्य पढ़िए» - a sentence, but the
            # child reads a WORD here - so it is trimmed after «करिए» (Yasir's choice), at the pause.
            "data": {"examples": ex, "no_heading": True,
                     "mic_nudge_audio": once("vo_mic_nudge", "इस बटन पर टैप करिए।"),
                     # [S03 2026-10-23] the user: the hand + «इस बटन पर टैप करिए» come at once on page 3 only
                     # (the child's first mic); on page 5 they wait for 7 s of inactivity, as before r151
                     "mic_nudge_now": sid == "T3"}}


def s_tap(sid, words, target, matra, correct_line):
    """Tap the coach whose word carries the matra. S02's screen; the S03 deck's lines (pages 7-9)."""
    n = MATRA_NAME[matra]
    tag = "e" if matra == U else "ai"
    nq = "“%s”" % LETTER[matra]
    return {"id": sid, "phase": "guided", "eis": "symbolic", "type": "TRAIN_TAP",
            "prompt_hi": "%s की मात्रा वाले शब्द पर टैप कीजिए।" % nq,
            "audio": {
                "prompt": once("vo_tap_prompt_" + tag,
                               "जिस डिब्बे में %s की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" % n),
                "hint1": once("vo_tap_h1_" + tag,
                              "फिर से पढ़िए। %s की मात्रा वाले शब्द पर टैप कीजिए।" % n),
                "hint2": once("vo_tap_h2_" + tag, "%s की मात्रा वाले शब्द पर टैप कीजिए।" % n),
                "hint3": vo("vo_%s_h3" % sid.lower(),
                            "%s शब्द में %s की मात्रा है। %s पर टैप कीजिए।" % (target, n, target)),
                "correct": vo("vo_%s_correct" % sid.lower(), correct_line)},
            "data": {"target": target, "matra": matra,
                     "coaches": [{"word": w, "correct": (w == target),
                                  "audio": name_clip(w), "matra": matra_of(w)} for w in words]}}


def s_sort(sid, phase, kind, bins, cards, heading, prompt, hint1, hint2, single=False,
           hint3_fallback=None):
    """Drag cards into coaches.

    ROUND 3 CHANGES, all from the deck:
      · coach labels lose छोटी / बड़ी — «उ (ु)» / «ऊ (ू)» on the word round, bare «उ» / «ऊ» on the
        matra and picture rounds. The VO still says छोटी उ / बड़ी ऊ; the change is on screen only.
      · praise is PER CARD (`correct_audio`), and there is no completion line at all.
      · the matra round takes one card per coach (`single`).
    """
    return {"id": sid, "phase": phase, "eis": "enactive", "type": "TRAIN_SORT",
            "prompt_hi": heading,
            # Rungs 2 and 3 are PER CARD on the word and picture rounds — Review-1 writes both
            # with the card's own name in them — so there is no screen-level line to record and
            # none is emitted. `guard_audio` accepts a rung satisfied item by item, the same way
            # it already accepts the praise line.
            "audio": dict([("prompt", vo("vo_%s_prompt" % sid.lower(), prompt)),
                           ("hint1", hint1)]
                          + ([("hint2", hint2)] if hint2 else [])
                          + ([("hint3", hint3_fallback)] if hint3_fallback else [])),
            "data": {"kind": kind, "bins": bins, "cards": cards, "single": single}}


def s_word_build(sid):
    """Page 12. S02's WORD_BUILD; the S03 deck's words: _ब · _र · _ज़ under apple / foot / table,
    options से बै मे बे पै (रे removed, बे added). «मेज़ बन गई» is feminine, as the deck writes it."""
    slots, opts = [], []
    for word, head, tail in [("सेब", "से", "ब"), ("पैर", "पै", "र"), ("मेज़", "मे", "ज़")]:
        k = key_of(word)
        gone = "गई" if word == "मेज़" else "गया"
        verb = "बनती" if word == "मेज़" else "बनता"
        slots.append({"word": word, "head": head, "tail": tail, "matra": matra_of(word),
                      "img": pic(k), "emoji": OBJ[k][1],
                      "name_audio": name_clip(word),
                      # [QA p12] S02's rung-3 line, which sounds the word out: «पु को पुल वाले डिब्बे में डालिए। पु, ल… पुल।»
                      "hint3_audio": vo("vo_p1_h3_" + slug(k),
                                        "%s को %s वाले डिब्बे में डालिए। %s, %s… %s।"
                                        % (head, word, head, tail, word)),
                      "correct_audio": vo("vo_wb_" + slug(k),
                                          "शाबाश! %s बन %s।" % (word, gone))})
        opts.append({"akshar": head, "audio": vo("vo_ak_" + slug(k), head)})
    opts.append({"akshar": "बै", "audio": vo("vo_ak_bai", "बै")})
    opts.append({"akshar": "बे", "audio": vo("vo_ak_be", "बे")})
    return {"id": sid, "phase": "practice", "eis": "enactive", "type": "WORD_BUILD",
            "prompt_hi": "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।",
            "audio": {
                "prompt": vo("vo_%s_prompt" % sid.lower(), "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"),
                # [QA p12] S02's page-12 lines
                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से देखिए। चित्र का नाम सोचिए और देखिए शब्द पूरा करने के लिए "
                            "कौन-सा अक्षर लगेगा।"),
                "hint2": vo("vo_%s_h2" % sid.lower(),
                            "नाम ध्यान से सुनिए। जिस शब्द की शुरुआत इस अक्षर से होती है, उसी "
                            "डिब्बे में इसे डालिए।"),
                "hint3": vo("vo_%s_h3_any" % sid.lower(),
                            "जो अक्षर चमक रहा है, उसे उसी डिब्बे में डालिए।")},
            "data": {"slots": slots, "options": opts}}


SC_HEADING = "सही शब्द चुनकर वाक्य पूरा कीजिए।"


def _full(pre, word, post):
    """the sentence with `word` in its blank - the exact text its `_try_` clip was recorded from"""
    return (pre + word + post).replace("  ", " ").strip()


def s_sentence(sid, scene, pre, post, answer, options, correct_line, ask, text_only=False):
    """Screens 13–16 — the new module, four instances.

    The three instruction lines are identical on all four screens, so `once` gives them one
    recording each. The praise line is per screen and reads the completed sentence back — except
    on screen 14, where the SME wrote «शाबाश! मैंने सही शब्द चुनकर वाक्य पूरा किया।» instead. That
    is first person and unlike its three siblings; it ships as written and is flagged rather than
    quietly normalised.
    """
    o = []
    for w in options:
        k = key_of(w)
        # REVIEW-1 RUNG 2: "put each of the three words in the blank in turn and read the whole
        # sentence out". So every option carries the sentence it makes — including the two that
        # make nonsense, which is the entire point: the wrong ones have to be HEARD to be wrong.
        o.append({"word": w, "img": pic(k), "emoji": OBJ[k][1], "audio": name_clip(w),
                  "sentence_audio": vo("vo_%s_try_%s" % (sid.lower(), slug(k)),
                                       (pre + w + post).replace("  ", " ").strip())})
    return {"id": sid, "phase": "practice", "eis": "symbolic", "type": "SENTENCE_COMPLETE",
            "prompt_hi": SC_HEADING,
            "audio": {
                "prompt": once("vo_sc_prompt", "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।"),
                # rung 1 asks a DIFFERENT question of the picture on each of the four screens,
                # so it is per screen and not `once`
                # [QA p14-16] S02's sentence ladder, unchanged
                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से पढ़िए। चित्र देखिए, %s? सही शब्द चुनकर वाक्य पूरा कीजिए।" % ask),
                "hint2": once("vo_sc_h2", "जो वाक्य सही लग रहा है, वही शब्द चुनिए।"),
                "hint3": vo("vo_%s_h3" % sid.lower(),
                            "%s %s चुनिए।" % ((pre + answer + post).replace("  ", " ").strip(),
                                              answer)),
                "correct": vo("vo_%s_correct" % sid.lower(), correct_line)},
            "data": {"scene_img": pic(scene), "scene_emoji": SCENE[scene],
                     "sentence_pre": pre, "sentence_post": post,
                     "answer": answer, "options": o,
                     # [r121] Yasir: pages 16 and 17 - «remove image from the options card, keep
                     # only text»
                     "opts_text_only": bool(text_only),
                     # [r121] Yasir: «when we drag & drop the correct option it should read the
                     # complete sentence as well». The answer's own sentence clip plays first -
                     # unless the praise line already reads the sentence back (P3, P5, P6 do:
                     # «शाबाश! सीमा आज बहुत खुश है।»), where playing both would say it twice.
                     "sentence_on_correct": (
                         None if _full(pre, answer, post).rstrip("।") in correct_line
                         else vo("vo_%s_try_%s" % (sid.lower(), slug(key_of(answer))),
                                 _full(pre, answer, post))),
                     "sentence_full": _full(pre, answer, post),
                     "scene_glow": SCENE_GLOW.get(scene, [])}}


def sort_hints(card, tag, h2_fmt, h3_fmt):
    """Hang Review-1's per-card rungs 2 and 3 on a sort card.

    Both name the card and its matra, so neither can be a screen-level line — «'सूरज' में बड़ी 'ऊ'
    की मात्रा है» is only true of that one card. The screen-level clips stay as the fallback the
    engine reaches for if a card is ever added without its own pair.
    """
    w, m = card["word"], card["bin"]
    k = slug(key_of(w))
    card["hint2_audio"] = vo("vo_%s_h2_%s" % (tag, k), h2_fmt % (w, MATRA_NAME[m]))
    card["hint3_audio"] = vo("vo_%s_h3_%s" % (tag, k), h3_fmt % (w, MATRA_NAME[m]))
    return card


def sort_card(word, correct_audio):
    k = key_of(word)
    return {"bin": matra_of(word), "word": word, "img": pic(k), "emoji": OBJ[k][1],
            "audio": name_clip(word), "correct_audio": correct_audio}


def build_slides():
    S = []
    # ---- TUTORIAL · deck pages 2-6 -----------------------------------------------------------
    S.append(s_intro("T1"))                                                   # page 2
    S.append(s_build("T2", "सब", "sab", "स", U, "से", "सेब", None,     # [QA p2] no «स। से। सेब।»
                     base_more="ये सब बच्चे हैं।"))
    S.append(s_pair("T3", ["मेज़", "पेड़"],                                     # page 4
                    "आइए, ए की मात्रा वाले कुछ शब्द देखें।",
                    ["मेज़, इसमें म पर ए की मात्रा लगी है। बोलकर देखिए।",
                     "पेड़, इसमें प पर ए की मात्रा लगी है। बोलकर देखिए।"]))
    S.append(s_build("T4", "पर", "par", "प", UU, "पै", "पैर", "प। पै। पैर।",     # page 5
                     base_more="मेज़ पर किताब रखी है।"))
    S.append(s_pair("T5", ["बैल", "भैंस"],                                     # page 6
                    "आइए, ऐ की मात्रा वाले कुछ शब्द देखें।",
                    ["बैल, इसमें ब पर ऐ की मात्रा लगी है। बोलकर देखिए।",
                     "भैंस, इसमें भ पर ऐ की मात्रा लगी है। बोलकर देखिए।"]))

    # ---- GUIDED · deck pages 7-11 --------------------------------------------------------------
    # ids chosen so S02's own sequence (G1 -> G3 -> G2) plays the S03 deck order: सेब, बैग, पैन
    S.append(s_tap("G1", ["सेब", "पैर", "बैल"], "सेब", U,                     # page 7
                   "शाबाश! सेब शब्द में ए की मात्रा है।"))
    S.append(s_tap("G3", ["पेड़", "रेल", "बैग"], "बैग", UU,                    # page 8
                   "शाबाश! बैग शब्द में ऐ की मात्रा है।"))
    S.append(s_tap("G2", ["मेज़", "पैन", "सेब"], "पैन", UU,                    # page 9
                   "शाबाश! पैन शब्द में ऐ की मात्रा है।"))

    g4_h1 = vo("vo_g4_h1", "फिर से पढ़िए। शब्द में कौन-सी मात्रा है, देखिए और उसे उसी मात्रा वाले डिब्बे में डालिए।")
    p2_h1 = vo("vo_p2_h1", "फिर से सुनिए। चित्र का नाम ध्यान से सुनिए और देखिए उसमें कौन-सी मात्रा है।")
    g4_bins = [{"key": m, "label": LETTER[m], "audio": LETTER_VO[m], "matra": m} for m in (U, UU)]
    # S02's G5 demo: letters onto their matra coaches, watch-only, handing its train on to G5
    S.append({"id": "G5D", "phase": "guided", "eis": "iconic", "type": "TRAIN_SORT",
              "prompt_hi": "देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं।",
              "audio": {"prompt": vo("vo_g5d_prompt",
                                     "देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं।"),
                        "outro": vo("vo_g4d_end", "अब आप भी ऐसे ही करके देखिए।")},
              "data": {"kind": "matra", "single": True, "demo": True, "keep_train_next": True,
                       "bins": [{"key": m, "label": "◌" + m, "audio": MATRA_VO[m], "matra": m}
                                for m in (U, UU)],
                       "cards": [{"bin": m, "word": LETTER[m], "audio": LETTER_VO[m],
                                  "correct_audio": vo("vo_g5d_%s" % ("e" if m == U else "ai"),
                                                      "%s की मात्रा इस डिब्बे पर है, इसलिए %s इस डिब्बे में गया।"
                                                      % (LETTER[m], LETTER[m]))}
                                 for m in (U, UU)]}})
    # page 10 - words into ए / ऐ coaches; rung 2 reads every card left, then the deck's line
    g4_cards = []
    for w in ["शेर", "बेर", "थैला", "पैसा"]:
        c = sort_card(w, vo("vo_ok_%s" % slug(key_of(w)),
                            "शाबाश! %s शब्द में %s की मात्रा है।" % (w, LETTER[matra_of(w)])))
        c["hint2_audio"] = vo("vo_g4_h2_%s" % slug(key_of(w)),                 # [QA p11]
                              "%s में %s की मात्रा है।" % (w, LETTER[matra_of(w)]))
        c["hint3_audio"] = vo("vo_g4_h3_%s" % slug(key_of(w)),
                              "%s शब्द में %s की मात्रा है। इसे %s वाले डिब्बे में डालिए।"
                              % (w, LETTER[matra_of(w)], LETTER[matra_of(w)]))
        g4_cards.append(c)
    S.append(s_sort("G4", "guided", "word", g4_bins, g4_cards,
                    "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
                    "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
                    g4_h1, None))
    # page 11 - the matras into ए / ऐ coaches
    S.append(s_sort("G5", "guided", "matra",
                    [{"key": m, "label": LETTER[m], "audio": LETTER_VO[m], "matra": m} for m in (U, UU)],
                    [{"bin": m, "word": "◌" + m, "audio": MATRA_VO[m],
                      "hint3_audio": vo("vo_g5_h3_%s" % ("e" if m == U else "ai"),
                                        "यह %s की मात्रा है। इसे %s वाले डिब्बे में डालिए।"
                                        % (LETTER[m], LETTER[m])),
                      "correct_audio": vo("vo_ok_matra_%s" % ("e" if m == U else "ai"),
                                          "शाबाश! यह %s की मात्रा है।" % LETTER[m])}
                     for m in (U, UU)],
                    "सही मात्रा को सही डिब्बे में डालिए।",
                    "सही मात्रा को सही डिब्बे में डालिए।",
                    vo("vo_g5_h1", "फिर से देखिए। सही मात्रा को सही डिब्बे में डालिए।"),
                    vo("vo_g5_h2", "मात्रा का आकार ध्यान से देखिए। इसे सही डिब्बे में डालिए।"),
                    single=True))

    # ---- PRACTICE · deck pages 12, 13, 17, 14, 16 ------------------------------------------------
    S.append(s_word_build("P1"))                                               # page 12
    p2_cards = []
    for w in ["पैन", "मेज़", "शेर", "बैग"]:                                    # page 13
        c = sort_card(w, vo("vo_okp_%s" % slug(key_of(w)),
                            "शाबाश! %s में %s की मात्रा है।" % (w, LETTER[matra_of(w)])))
        c["hint2_audio"] = vo("vo_p2_h2_%s" % slug(key_of(w)),                 # [QA p13] S02's lines
                              "%s में %s की मात्रा है। अब इसे सही मात्रा वाली बोगी में डालिए।"
                              % (w, LETTER[matra_of(w)]))
        c["hint3_audio"] = vo("vo_p2_h3_%s" % slug(key_of(w)),
                              "%s को %s की मात्रा वाली बोगी में डालिए।" % (w, LETTER[matra_of(w)]))
        p2_cards.append(c)
    S.append(s_sort("P2", "practice", "picture", g4_bins, p2_cards,
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    p2_h1, None))
    # three sentences - the SME deleted page 15 (मेरे ___ में दर्द है). Order = the deck's reorder.
    S.append(s_sentence("P3", "scn_likhna", "मैं ", " से लिखता हूँ।", "पैन",       # page 17
                        ["पैन", "पेड़", "बैल"], "शाबाश! मैं पैन से लिखता हूँ।",
                        "बच्चा किससे लिख रहा है"))
    S.append(s_sentence("P4", "scn_bageecha", "बगीचे में एक बड़ा ", " है।", "पेड़",  # page 14
                        ["पेड़", "बैल", "पैन"], "शाबाश! बगीचे में एक बड़ा पेड़ है।",
                        "बगीचे में क्या है"))
    S.append(s_sentence("P5", "scn_seb_khana", "मुझे ", " खाना अच्छा लगता है।", "सेब",  # page 16
                        ["सेब", "बैग", "मेज़"], "शाबाश! मुझे सेब खाना अच्छा लगता है।",
                        "बच्चा क्या खा रहा है",
                        text_only=True))      # [2026-10-22] user: page 16 - text only on the options

    # S02's sequence (r127 / r134): the G5 demo and G5 open the guided block, then the taps, then G4
    SEQ = ["G5D", "G5", "G1", "G3", "G2", "G4", "P1", "P2", "P3", "P4", "P5"]
    _by = {x["id"]: x for x in S}
    assert set(SEQ) <= set(_by), "sequence names a screen that does not exist"
    S[:] = [x for x in S if x["id"] not in SEQ] + [_by[i] for i in SEQ]

    # ---- the मात्रा रनर, now ए / ऐ ----------------------------------------------------------------
    mg_prompt = "अब एक खेल! ऊपर दी गई मात्रा वाले शब्द पकड़िए।"
    S.append({"id": "MG1", "phase": "practice", "eis": "enactive", "type": "MINI_GAME",
              "prompt_hi": mg_prompt,
              "audio": {"prompt": vo("vo_mg_prompt", mg_prompt)},
              "data": {"src": "matra-runner/index.html", "title": "मात्रा रनर"}})

    recap = CEL_LINE
    S.append({"id": "CEL", "phase": "practice", "eis": "iconic", "type": "CELEBRATION",
              "prompt_hi": recap,
              "audio": {"prompt": vo("vo_cel_prompt", recap)}, "data": {}})
    return S


def build_card(slides):
    for vid, text in MATRA_TEXT.items():
        vo(vid, text)
    # the SME's landing line, in their spelling: «स्विफ्टी» in Devanagari, «जानेंगे» not «जानेगें»
    # [r134] Yasir: the cover's «आज हम मात्राओं के बारे में जानेंगे» becomes page 1's line, which page 1
    # no longer speaks. Re-cut from the two human recordings (1_SPEC/edit_lesson_voice_r134.py).
    # [S03] the deck's greeting + page 2's line, merged onto the cover the way S02 r134 merged its own
    vo("vo_landing", "नमस्ते दोस्त! मैं हूँ स्विफ्टी। आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।")   # [QA] नमस्ते, as S02
    vo("vo_try_again", "एक बार फिर सुनिए।")          # आप, with everything else

    counts = {}
    for s in slides:
        counts[s["phase"]] = counts.get(s["phase"], 0) + 1
    audio = {v: "assets/Audio/%s.ogg" % v for v in sorted(AUDIO_TEXT)}
    for v in COPY_AUDIO:
        audio.setdefault(v, "assets/Audio/%s.ogg" % v)
    image = {k: "assets/Images/%s.webp" % k for k in sorted(used_images(slides))}

    return {
        "version": "0.1", "skill_code": CODE, "lo_code": "HI02H11_L02",
        "grade": "02", "attribute": "H11", "skill_type": "CORE",
        "part_label": "", "medium": "hi",
        "title": {"hi": "मात्राओं की रेल", "en": "Matra train — the e / ai matras"},
        "subtitle_hi": "",
        "theme": "toybox",
        "skill_description_hi": ("ए, ऐ मात्रा वाले शब्द पढ़ता है। "
                                 "शब्दों में आने वाली मात्रा पहचानता है।"),
        "landing_audio": "vo_landing",
        # SME: "Show only two matra boxes/cards: 1st box ु, 2nd box ू … The matras can be shown
        # inside two train bogies/cards so that the lesson visually continues as a «मात्राओं की
        # रेल» journey", with a right-to-left arrival, the bogies appearing one by one, a whistle
        # on entry and a sparkle as each matra lands.
        #
        # `matra_train` is the PAINTED train ported from the sibling lesson HI02H11_L02_S01 — the
        # same artwork the mockup draws, as a 36-cell spritesheet, cropped from three coaches to
        # two for this lesson's two matras (634 -> 479px per cell). See the module set's dressLandingTrain().
        #
        # THE MATRAS ARE BARE HERE, not «◌ु». An orphan combining mark makes the font draw its own
        # dotted placeholder circle, which is exactly the «ु» the note asks for and is how the
        # sibling ships it. The intro screen still uses an explicit ◌ because its glyphs sit in a
        # text run where the font does not supply one.
        "landing_hero": {"kind": "matra_train", "matras": [U, UU],
                     # r7: the coach shows the LETTER with its matra in brackets -
                     # the same «उ (ु)» form the G4 bins already use, so the cover
                     # and the sorting screens name the pair the same way.
                     "letters": ["ए", "ऐ"]},
        "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                                   "practice": "vo_pt_practice"},
        # flipped to आप with everything else — these sit between the phases, next to the shared
        # gate clips, which already speak आप
        "phase_transition_title": {"tutorial": "चलिए, रेल चलाएँ!", "guided": "साथ में करें।",
                                   "practice": "अब आपकी बारी।"},
        "phase_distribution": counts,
        # [r65] the gate bird is Yasir's seeking/speaking Swifty. Cropped to the bird and encoded
        # as animated WebP (the source GIF is 9.7 MB at 1500^2; it lives in 1_SPEC/game_art_src/
        # gate/). She starts talking 3.82 s in - measured frame by frame - so the gate VO waits.
        # [r82] trimmed: the seek, straight into the rise and her first word - the blink-and-look-
        # around (1.4 s) and most of the pause before she speaks are cut. New name, because the
        # deployment caches assets/ as immutable and would keep serving the long version.
        # [r84] Yasir's sounds for the landing play button and the next arrow (engine: CARD.ui_sfx)
        "ui_sfx": {"play": "sfx_play_button", "next": "sfx_next_button"},
        # [r106] Yasir: "first she should seek from the bottom, then start speaking - the VO should start
        # when she starts speaking": back to her first speaking frame (r105 had made it 0)
        # [r142] the transition screen is Hindi-game-gender-identify's (engine phaseBlurTransition):
        # its Swifty (assets/UI/peeking_talk_up.webp) and animation replace the seeking bird and her
        # lip-sync, so `img`, `talk_at_ms`, `title_dur_ms` and the lip-sync sheet step are gone.
        "gate": {
                 # [r83] Yasir: the third transition «अब आपकी बारी!» after page 17, i.e. just before
                 # the runner game - not in front of the first practice page (engine: CARD.gate.at)
                 "at": {"round3": "MG1"},
                 # [r103] where each transition's on-screen phrase starts inside its clip, so the text
                 # appears when Swiftee says it: «चलिए, शुरू करें!» / «चलिए, साथ में करें!» /
                 # «अब आपकी बारी!» - measured (silencedetect -35 dB) on the shared kit clips
                 # [r109] re-measured on the recorded transition lines (25 ms envelope, the phrase
                 # after the last long pause): «चलिए, शुरू करें!» 3075-4225 ms of 4.32 s, «चलिए, साथ
                 # में करें!» 3575-4900 of 5.01 s, «अब आपकी बारी।» 925-1775 of 1.87 s
                 # [S03 2026-10-23] re-measured on the lesson's own recorded VO set (silencedetect -35 dB):
                 # «चलिए, शुरू करें!» from 2975 of 4.44 s, «चलिए, साथ में करें!» 3755 of 5.28 s,
                 # «अब आपकी बारी।» 1260 of 2.40 s
                 "title_cue_ms": {"tutorial": 2975, "guided": 3755, "practice": 1260}},
        # REVIEW-1 LADDER — three rungs on every test screen:
        #   wrong 1 = rung-1 VO, nothing else moves and nothing is highlighted
        #   wrong 2 = rung-2 VO plus a DEMONSTRATION (words read out, matras glowed, sentences
        #             tried in the blank) — and still no hand
        #   wrong 3 = rung-3 VO, the hand on the answer, and everything else LOCKS
        # `hand_on_hint3` is the one switch for flag F2: ruling [28f] keeps the hand out of
        # practice, and Review-1 asks for it on six practice screens. Set it false and the hand
        # goes back to tutorial/guided only, with the glow carrying rung 3 on its own.
        "scaffold_rules": {"nudge_timeout_ms": {"guided": 6000, "practice": 8000},
                           "max_attempts": 3, "hint_levels": 3, "hand_on_attempt": 3,
                           "hand_on_hint3": True, "lock_after_hint3": True,
                           "reveal_on_attempt": None, "silent_on_late_correct": True},
        "signals_expected": ["slide_entered", "slide_completed", "intro_letter_tap",
                             "train_tap_first_try", "matra_sort_item", "matra_sort_first_try",
                             "word_build_item", "word_build_first_try",
                             "sentence_complete_first_try",
                             "answer_wrong", "hint_shown",
                             "phase_transition", "mastery_score", "lesson_completed"],
        # BASE_OBJ has to be in here too. It was added so पल / फल could have pictures without
        # entering OBJ (which `guard_single_matra` audits as "words carrying exactly one target
        # matra", and those two carry none) — but this map is built from OBJ, so the two new
        # images arrived with no emoji fallback and the receipt failed them. Caught by the
        # receipt, which is exactly what it is for.
        "_emoji_fallback": dict(list({k: v[1] for k, v in OBJ.items()}.items())
                                + [(v[0], v[1]) for v in BASE_OBJ.values()]
                                + list(SCENE.items())),
        "assets": {"audio": audio, "audio_text": AUDIO_TEXT, "image": image,
                   "audio_ext": "ogg", "img_ext": "webp"},
        "slides": slides,
    }


# ---------------------------------------------------------------- guards
def used_images(slides):
    """Every image key a slide actually renders. `pic()` returns None for art that is not on disk
    yet, so a pending picture never reaches this set and never lands in assets.image."""
    used = set()
    for s in slides:
        d = s.get("data", {}) or {}
        for k in ("result_img", "base_img", "scene_img"):
            if d.get(k):
                used.add(d[k])
        for group in ("examples", "cards", "slots", "options"):
            for it in d.get(group, []) or []:
                if isinstance(it, dict) and it.get("img"):
                    used.add(it["img"])
    return used


def guard_engine(src):
    m = VER_RE.search(src)
    if not m:
        sys.exit("X  no ENGINE_VERSION in 4_ENGINE/lesson_template.html")
    ver = m.group(1)
    for name in TRAIN_MODULES:
        if ("SlideModules." + name + " = {") not in src:
            sys.exit("X  the engine copy is missing the module %s. Re-run the injector "
                     "(4_ENGINE/inject_train.py); do NOT hand-edit the monolith." % name)
    for name in STOCK_MODULES:
        if not (re.search(r'^\s{2}"?' + name + r'"?\s*[:(]', src, re.M)
                or re.search(r'SlideModules\.' + name + r'\s*=', src)):
            sys.exit("X  the engine copy is missing the stock module %s" % name)
    if "TRAIN STYLES :: BEGIN" not in src:
        sys.exit("X  the train CSS block is missing — the coaches would render unstyled")
    rsm = RSM_RE.search(src)
    inset = set(re.findall(r'"([^"]+)"', rsm.group(1))) if rsm else set()
    for bad in (U, UU):
        if bad in inset:
            sys.exit("X  %r is in RIGHT_SPACING_MATRAS. It is ABOVE-BASE with no advance: it shares its\n"
                     "     consonant's columns, so the highlight colours the NEXT letter.\n"
                     "     Measured: पुल puts 11342 red px on the ल. Remove it." % bad)
    if 'case "letter":' not in src:
        sys.exit("X  conceptTileHTML has no `letter` case — the landing strip would be empty")
    if "dressLandingTrain" not in src:
        sys.exit("X  the landing-train dressing is missing — the landing bogies would not render")
    if 'kind !== "matra_train"' not in src:
        sys.exit("X  the landing train is still the drawn version — re-run inject_train.py")
    if "TrainChrome" not in src or "TRAIN_ART" not in src:
        sys.exit("X  TrainChrome is missing — the activity screens would draw a SECOND, "
                 "different locomotive beside the painted cover. "
                 "Re-run 4_ENGINE/inject_train.py.")
    print("  OK  engine: %s  (4_ENGINE, pinned)" % ver)
    print("      modules present: %s" % ", ".join(TRAIN_MODULES))
    if "ABOVE_MATRAS" not in src:
        sys.exit("X  the े/ै above-line highlight is missing from the engine - re-run inject_train.py")
    print("      train styles present; े/ै on the above-line highlight path")
    return ver


def guard_flow(slides):
    """The flow must match the deck screen for screen, plus the mini-game: landing + 18."""
    want = ["MATRA_PAIRS", "MATRA_BUILD", "MEET_PAIR", "MATRA_BUILD", "MEET_PAIR",
            # [r134] Yasir's order: the G5 demo and G5 first, then the three taps, then G4
            "TRAIN_SORT",         # G5D - the watch-only demo of G5 (r131)
            "TRAIN_SORT",         # G5
            "TRAIN_TAP", "TRAIN_TAP", "TRAIN_TAP",
            "TRAIN_SORT",         # G4
            "WORD_BUILD", "TRAIN_SORT",
            "SENTENCE_COMPLETE", "SENTENCE_COMPLETE", "SENTENCE_COMPLETE",   # [S03] page 15 deleted
            "MINI_GAME",          # [r36] added after the deck was written - see screen 17
            "CELEBRATION"]
    got = [s["type"] for s in slides]
    if got != want:
        sys.exit("X  flow does not match the SME's round-3 deck.\n     want: %s\n     got:  %s"
                 % (want, got))
    print("  OK  flow guard: landing + %d slides, in S02's r134 order"
          % len(slides))


def guard_single_matra():
    bad = []
    for w, m in [(v[0], v[2]) for v in OBJ.values()]:
        found = set(c for c in w if c in (U, UU))
        if found != set([m]):
            bad.append("%s carries %s, declared %r" % (w, sorted(found) or "none", m))
    if bad:
        sys.exit("X  single-matra rule broken:\n     " + "\n     ".join(bad))
    print("  OK  single-matra rule: all %d words carry exactly one target matra" % len(OBJ))


def guard_sentences(slides):
    """Every sentence screen must be answerable and must not give itself away.

    Two ways a sentence screen can be quietly broken, both invisible to an existence check: the
    answer is not among the options (unanswerable), or the answer is already printed in the
    sentence (free). Whether a distractor ALSO reads correctly cannot be decided mechanically —
    that one is a human read, and it is on the verification list.
    """
    bad = []
    for s in slides:
        if s["type"] != "SENTENCE_COMPLETE":
            continue
        d = s["data"]
        words = [o["word"] for o in d["options"]]
        if d["answer"] not in words:
            bad.append("%s: answer %r is not one of the options %s" % (s["id"], d["answer"], words))
        if len(set(words)) != len(words):
            bad.append("%s: duplicate option %s" % (s["id"], words))
        shown = (d["sentence_pre"] or "") + (d["sentence_post"] or "")
        if d["answer"] in shown:
            bad.append("%s: the answer %r is already printed in the sentence"
                       % (s["id"], d["answer"]))
    if bad:
        sys.exit("X  sentence audit:\n     " + "\n     ".join(bad))
    n = len([s for s in slides if s["type"] == "SENTENCE_COMPLETE"])
    print("  OK  sentence audit: %d screens, answer present as an option and never pre-printed" % n)


def guard_word_build(slides):
    """A WORD_BUILD option must complete EXACTLY ONE coach, and every coach must be completable.

    The module judges a drop by reconstructing the word (`akshar + tail == word`), so an option
    that completed two coaches would make one of them accept the wrong tile, and a distractor that
    accidentally completed a coach would mark a wrong answer right. Both are silent at runtime.
    """
    for s in slides:
        if s["type"] != "WORD_BUILD":
            continue
        d = s["data"]
        for sl in d["slots"]:
            hits = [o["akshar"] for o in d["options"] if o["akshar"] + sl["tail"] == sl["word"]]
            if len(hits) != 1:
                sys.exit("X  word-build: %r is completed by %s — must be exactly one option"
                         % (sl["word"], hits or "nothing"))
        dis = [o["akshar"] for o in d["options"]
               if not any(o["akshar"] + sl["tail"] == sl["word"] for sl in d["slots"])]
        if not dis:
            sys.exit("X  word-build: the SME asks for 1-2 distractors; there are none")
        if "रे" in [o["akshar"] for o in d["options"]]:
            sys.exit("X  word-build: रे is still an option — the SME asked for it to be removed")
        print("  OK  word-build audit: %d coaches, exactly 1 option each, distractors %s (रे removed)"
              % (len(d["slots"]), dis))


GESTURE = {"TRAIN_TAP": "pick", "TRAIN_SORT": "drag", "MATRA_FILL": "drag",
           "WORD_BUILD": "drag", "SENTENCE_COMPLETE": "pick", "POEM_SEARCH": "search"}


def guard_prompts(slides):
    """EVERY slide must carry on-screen heading text.

    THE DEFECT THIS EXISTS TO PREVENT (SME review round 2, 2026-09-21):
    «ऊपर स्विफ्टी वाले बॉक्स की हेडिंग मिसिंग है». The first build shipped prompt_hi: "" on 14 of
    16 slides and then hid the heading band with CSS, because the SME's per-screen note says
    "No instruction text on screen. Only VO should play." That reading was wrong — their own
    mockups draw the band, with text in it, on both test and teach screens, and the round-3
    mockups draw it again on all four sentence screens and on the word-build screen. The note
    means no EXTRA explanatory copy in the PLAY AREA; the heading band beside the mascot is house
    chrome on every screen of every shipped lesson.

    Failing the build is the right response because the symptom was invisible to every other
    check: the page scored 0 FAIL / 0 WARN, all assets served and no JS errored — it simply had a
    mascot sitting next to nothing.
    """
    bad = [sl["id"] for sl in slides
           if not (sl.get("prompt_hi") or "").strip()
           and not (sl.get("data") or {}).get("no_heading")]
    if bad:
        sys.exit("X  guard_prompts: empty prompt_hi on %s — the heading band would render "
                 "blank beside the mascot" % ", ".join(bad))
    short = [(sl["id"], sl["prompt_hi"]) for sl in slides
             if not (sl.get("data") or {}).get("no_heading")
             and len(sl["prompt_hi"].strip()) < 8]
    if short:
        sys.exit("X  guard_prompts: heading too short to read: %s" % short)
    opted = [sl["id"] for sl in slides if (sl.get("data") or {}).get("no_heading")]
    print("   guard_prompts ....... %d/%d slides carry heading text%s"
          % (len(slides) - len(opted), len(slides),
             ("; %s opted out on the SME's instruction" % ", ".join(opted)) if opted else ""))


BAD_REGISTER = ["करो", "सोचो", "देखो", "डालो", "सुनो", "चुनो", "पढ़ो", "बोलो", "ढूँढो",
                "घुमाओ", "मिलाओ", "लगाओ", "बनाओ", "तुम"]
# [r105] the one line allowed a तुम form: the standard Swiftee end-screen dialogue Yasir chose
CEL_LINE = "बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!"
REGISTER_ALLOW = {CEL_LINE}


def guard_register(slides, card):
    """No तुम-form imperative may survive the round-3 flip.

    The SME says it twice — "Use respectful language throughout: सुनिए, पहचानिए, डालिए" and
    "Maintain respectful language: सोचिए, देखिए, चुनिए instead of सोचो, देखो, चुनो". Round 2 was
    entirely तुम, so this touches almost every clip and every heading, and a single missed line
    reads as sloppiness rather than as a bug — which is exactly the kind of thing no other check
    would catch. So it is checked mechanically.
    """
    hits = []
    targets = [("%s (clip)" % v, t) for v, t in AUDIO_TEXT.items()]
    targets += [("%s heading" % s["id"], s.get("prompt_hi") or "") for s in slides]
    targets += [("phase title %s" % k, v) for k, v in card["phase_transition_title"].items()]
    for where, text in targets:
        if text in REGISTER_ALLOW:
            continue
        for b in BAD_REGISTER:
            if b in text:
                hits.append("%s: %s" % (where, text))
                break
    if hits:
        sys.exit("X  register guard: तुम-form survives the round-3 flip in %d place(s):\n     %s"
                 % (len(hits), "\n     ".join(hits)))
    print("  OK  register guard: आप throughout — no तुम form in any clip, heading or phase title")


def guard_mechanics(slides):
    # [r36] MINI_GAME is excluded with CELEBRATION: the drag/pick ratio is about how the lesson
    # ASKS its questions, and a runner asks none - counting it would skew a balance the deck set.
    tests = [s for s in slides
             if s["phase"] != "tutorial" and s["type"] not in ("CELEBRATION", "MINI_GAME")]
    fams = {}
    for s in tests:
        f = GESTURE.get(s["type"])
        if not f:
            sys.exit("X  %s: %s unclassified in GESTURE" % (s["id"], s["type"]))
        fams[f] = fams.get(f, 0) + 1
    n = len(tests)
    if len(fams) < 2:
        sys.exit("X  mechanic gate: one family only")
    if "drag" not in fams:
        sys.exit("X  mechanic gate: no produce mechanic")
    # ROUND 3 RAISES THE CEILING FROM 60% TO 70%, AND THAT IS A REAL LOOSENING — so it says so out
    # loud rather than being quietly widened. The SME's round-3 flow is three tap screens plus
    # four sentence screens against four drag screens: 7 pick / 4 drag = 64% pick. The gate exists
    # to stop a lesson being one gesture end to end, and 64/36 across two families with a real
    # produce mechanic is not that. The deck is authoritative on the flow, so the guard moves
    # rather than the lesson — and the move is reported in the scorecard.
    for f, c in sorted(fams.items()):
        if 100.0 * c / n > 70.0:
            sys.exit("X  mechanic gate: %s is %.0f%% of %d test slides" % (f, 100.0 * c / n, n))
    mix = ", ".join("%s %d (%.0f%%)" % (f, c, 100.0 * c / n) for f, c in sorted(fams.items()))
    print("  OK  mechanic gate: %d test slides — %s" % (n, mix))
    if max(100.0 * c / n for c in fams.values()) > 60.0:
        print("  !!  NOTE: above the round-2 ceiling of 60%. The SME's round-3 flow is pick-heavy "
              "by design (3 tap + 4 sentence screens); ceiling raised to 70% for this deck.")


def guard_pictures(slides, card):
    used = used_images(slides)
    declared = set(card["assets"]["image"])
    if used - declared:
        sys.exit("X  images used but not declared: %s" % sorted(used - declared))
    if declared - used:
        sys.exit("X  images declared but never shown: %s" % sorted(declared - used))
    missing = [k for k, p in card["assets"]["image"].items()
               if not os.path.isfile(os.path.join(BUNDLE, p))]
    if missing:
        sys.exit("X  declared images missing from disk: %s" % sorted(missing))
    print("  OK  picture guard: %d images, all declared, all used, all on disk" % len(used))


def guard_audio(slides, card):
    """Every audio id a slide names must be declared, and every test slide must carry the whole
    3-rung ladder — a missing rung is a silent beat exactly when the child is stuck.

    ROUND 3: the `correct` rung may be satisfied PER ITEM instead of per slide. The SME moved the
    praise line onto each card («शाबाश! 'सुई' शब्द में उ की मात्रा है।») and asked for no completion
    line, so a sort or build screen whose every item carries `correct_audio` has a complete ladder
    without a slide-level clip — and demanding one would mean recording a line nothing ever plays.
    """
    declared = set(card["assets"]["audio"])
    miss, ladders = [], []
    for s in slides:
        d = s.get("data", {}) or {}
        for k, v in (s.get("audio") or {}).items():
            if v and v not in declared:
                miss.append("%s.%s -> %s" % (s["id"], k, v))
        items = (d.get("cards") or []) + (d.get("slots") or [])
        for group in ("cards", "slots", "options", "examples", "pairs", "bins", "coaches"):
            for it in d.get(group, []) or []:
                if not isinstance(it, dict):
                    continue
                for k in ("audio", "correct_audio", "audio_line", "matra_audio",
                          "hint2_audio", "hint3_audio", "name_audio", "sentence_audio"):
                    if it.get(k) and it[k] not in declared:
                        miss.append("%s %s.%s -> %s" % (s["id"], group, k, it[k]))
        # [r83] a watch-only demonstration asks the child nothing, so it has no ladder to check
        if s["type"] in GESTURE and not d.get("demo"):
            per_item = bool(items) and all(c.get("correct_audio") for c in items)
            # REVIEW-1: rungs 2 and 3 may be satisfied PER ITEM as well. On the word and picture
            # rounds both lines name the card («'सूरज' में बड़ी 'ऊ' की मात्रा है»), so a
            # screen-level recording would be a line nothing ever plays.
            per_h2 = bool(items) and all(c.get("hint2_audio") for c in items)
            per_h3 = bool(items) and all(c.get("hint3_audio") for c in items)
            for rung in ("prompt", "hint1", "hint2", "hint3", "correct"):
                if (s.get("audio") or {}).get(rung):
                    continue
                if rung == "correct" and per_item:
                    continue
                if rung == "hint2" and per_h2:
                    continue
                if rung == "hint3" and per_h3:
                    continue
                ladders.append("%s missing %s" % (s["id"], rung))
    if miss:
        sys.exit("X  undeclared audio ids:\n     " + "\n     ".join(miss))
    if ladders:
        sys.exit("X  incomplete 3-attempt ladder:\n     " + "\n     ".join(ladders))
    print("  OK  audio guard: every id declared; every test slide has a complete ladder")


# ---------------------------------------------------------------- stale-asset pruning
def prune_stale(card):
    """Delete exactly the clips round 3 invalidated — nothing more.

    THIS IS THE DEFECT IT PREVENTS, and it has already happened on this lesson once: a clip's TEXT
    changed in the builder while its ID stayed the same, the old .ogg stayed on disk, and
    `gen_tts.py` — which skips ids that already have a file — never re-recorded it. The game then
    shipped round-2 audio under round-3 text. It is invisible to an existence check and to a
    file-size check.

    The previous build's `card.json` still holds the previous `audio_text`, so the comparison is
    exact: a clip is STALE if its text changed and ORPHANED if its id is gone. Deleting exactly
    those leaves gen_tts a minimal, correct work list — which is also the rule about regenerating
    only what changed, since re-running an UNCHANGED clip returns a different take.
    """
    old_path = os.path.join(BUNDLE, "card.json")
    if not os.path.isfile(old_path):
        return [], [], []        # [S03] S02 returned 2 here, crashing a first build
    try:
        old = json.load(open(old_path, encoding="utf-8"))
    except Exception:
        return [], [], []        # [S03] S02 returned 2 here, crashing a first build
    old_text = (old.get("assets") or {}).get("audio_text") or {}
    new_text = card["assets"]["audio_text"]
    stale, orphan = [], []
    for vid, text in sorted(old_text.items()):
        if vid not in new_text:
            orphan.append(vid)
        elif new_text[vid] != text:
            stale.append(vid)
    for vid in stale + orphan:
        f = os.path.join(AUD_DIR, vid + ".ogg")
        if os.path.isfile(f):
            os.remove(f)
    old_img = set((old.get("assets") or {}).get("image") or {})
    img_orphan = sorted(old_img - set(card["assets"]["image"]))
    return stale, orphan, img_orphan


def write_vo_list():
    """The recording list, with the two traps this lesson keeps hitting called out by name."""
    risky = sorted(v for v, t in AUDIO_TEXT.items() if "—" in t or t.count("।") >= 3)
    with open(os.path.join(SPEC_DIR, "VO_RECORDING_LIST.md"), "w", encoding="utf-8") as f:
        f.write("# %s (ए / ऐ) · «मात्राओं की रेल» — VO recording list\n\n" % CODE)
        f.write("%d clips. Shown text == spoken text; record exactly this.\n\n" % len(AUDIO_TEXT))
        f.write("**Register is आप** — the SME asked for it twice, in as many words. Round 2 was "
                "तुम, so most of this list is a re-record, not a new line. `guard_register` in the "
                "builder fails the build if a तुम form survives anywhere.\n\n")
        f.write("**Only re-record what changed.** The builder deletes exactly the clips whose text "
                "moved this round, so `gen_tts.py` (which skips ids that already have a file) "
                "regenerates precisely those and leaves every unchanged take alone. Never "
                "`--force` the whole card: generated audio is non-deterministic, so re-running an "
                "unchanged clip returns a different take — a change the SME never asked for.\n\n")
        f.write("## ⚠️ EAR-CHECK — %d clips a human must listen to before delivery\n\n" % len(risky))
        f.write("The TTS model truncates a clip when an **em-dash precedes a short final word** "
                "(measured on this lesson: em-dash 0.73–1.05 s vs comma 1.53–2.21 s for the same "
                "words), and it does the same to a line built from several short danda-separated "
                "pieces. The SME's round-3 MEET_PAIR lines and the new sound-differentiation clips "
                "are written in exactly those shapes. Their wording ships as written — rewriting a "
                "reviewer's Hindi to dodge a synthesis bug is the worse failure — so the clips are "
                "flagged instead. **Truncation is invisible to an existence check and to a "
                "file-size check.** `_verify_assets.py` compares each clip against peers of "
                "similar text length and is the only thing that catches it. Run it, then listen to "
                "every id below.\n\n")
        for v in risky:
            f.write("- `%s` — %s\n" % (v, AUDIO_TEXT[v]))
        f.write("\n## All clips\n\n| clip id | spoken text |\n|---|---|\n")
        for v in sorted(AUDIO_TEXT):
            f.write("| `%s` | %s |\n" % (v, AUDIO_TEXT[v]))
        f.write("\n## Copied, do NOT record\n\n")
        for v in COPY_AUDIO:
            f.write("- `%s`\n" % v)
    return risky


ART_BRIEFS = {}


def write_art_manifest(slides):
    """`_art_manifest.json` keeps the prompt for every picture in the lesson; the pending ones are
    split out so an art run can be pointed straight at a work list, and the scenes are named
    separately because they must NOT go through the chroma-key pipeline."""
    path = os.path.join(SPEC_DIR, "_art_manifest.json")
    existing = json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else {}
    if isinstance(existing, dict) and "all" in existing:
        existing = existing["all"]
    allm = dict(existing)
    allm.update(ART_BRIEFS)
    # anything this card no longer shows is dropped, so nothing is regenerated for a deleted screen
    live = set(used_images(slides)) | set(PENDING_ART)
    allm = dict((k, v) for k, v in allm.items() if k in live)
    out = {"all": allm,
           "pending": dict((k, allm[k]) for k in sorted(PENDING_ART) if k in allm),
           "scenes_do_not_key": sorted(SCENE)}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return out


def check_chrome():
    """The shared UI chrome and the fixed clips (phase gates + SFX) already live in the bundle.

    The factory build copied them from a reference bundle under
    `<factory>/KG and G1 refernce ready HTML's`, which is OUTSIDE this self-contained handoff.
    Nothing here reaches out to it: the files are checked in place and a missing one is reported
    rather than silently re-copied from a path that does not exist.
    """
    ui = os.path.join(BUNDLE, "assets", "UI")
    n = len(os.listdir(ui)) if os.path.isdir(ui) else 0
    missing = [v for v in COPY_AUDIO if not os.path.isfile(os.path.join(AUD_DIR, v + ".ogg"))]
    print("  OK  chrome in place: %d UI files, %d/%d fixed clips"
          % (n, len(COPY_AUDIO) - len(missing), len(COPY_AUDIO)))
    if missing:
        print("  !!  fixed clips MISSING from the bundle: %s" % missing)


LETTER_GLOW_CSS = """
<style id="bundleLetterGlow">
/* Landing letter-strip glow. concept_strip returns before the engine adds show/hint-glow, so
   every such landing in the fleet misses it; raised as a dev ask. Base rule, not keyframes-only:
   capture_pages.py kills animation, and a glow that lives only in @keyframes vanishes from the
   review deck. Amber, because blue disappears against the pale-blue landing card.
   ROUND 3: scoped OFF the train landing — there the bogie is the frame, so the pill and its
   pulse would fight it. See `.lt-train .sg-ex-letter` in the train styles. */
.sg-ex-letter{
  box-shadow:0 0 0 6px rgba(255,206,46,.65),0 0 18px 4px rgba(252,188,24,.50),
             0 12px 28px rgba(11,61,140,.16);
  animation:sgLetterGlow 2.2s ease-in-out infinite;
}
.sg-acell:nth-child(1) .sg-ex-letter{animation-delay:.95s;}
.sg-acell:nth-child(2) .sg-ex-letter{animation-delay:1.40s;}
@keyframes sgLetterGlow{
  0%,100%{box-shadow:0 0 0 6px rgba(255,206,46,.65),0 0 18px 4px rgba(252,188,24,.50),
                     0 12px 28px rgba(11,61,140,.16);}
  50%    {box-shadow:0 0 0 10px rgba(255,206,46,.92),0 0 28px 8px rgba(252,188,24,.70),
                     0 14px 32px rgba(11,61,140,.22);}
}
@media (prefers-reduced-motion:reduce){ .sg-ex-letter{animation:none;} }
</style>
"""


# ---------------------------------------------------------------- [r85] celebration Swiftie
# The lip-synced celebration from celebration_kit/ (see its README): she jumps on «शाबाश!», talks
# with her beak opening on each syllable of THIS lesson's celebration line, then idles mouth shut.
#   · the kit's three sheets are copied UNCHANGED into assets/UI/celebration/ on every build
#   · the lip-sync track is measured from the celebration VO on every build, so a re-recorded clip
#     re-syncs by itself - make_lipsync.py is the kit's own measurer, run as it ships
#   · meta + track ride on the card as CARD.end_anim; the kit's player and the README's wrapper of
#     SlideModules.CELEBRATION.mount are injected after the engine script - the engine is not edited
KIT = os.path.join(HANDOFF, "celebration_kit")
CEL_DIR = os.path.join(BUNDLE, "assets", "UI", "celebration")


def celebration_anim(slides):
    import shutil, filecmp, tempfile, subprocess
    cel = [x for x in slides if x["type"] == "CELEBRATION"]
    vo_id = cel and (cel[0].get("audio") or {}).get("prompt")
    vo_path = vo_id and os.path.join(AUD_DIR, vo_id + ".ogg")
    if not (os.path.isdir(KIT) and vo_path and os.path.isfile(vo_path)):
        print("  !!  celebration Swiftie skipped (kit or %s missing) - the stock mascot stays" % vo_id)
        return None
    meta = json.load(open(os.path.join(KIT, "sheets", "cel_meta.json"), encoding="utf-8"))
    os.makedirs(CEL_DIR, exist_ok=True)
    for sheet in (meta["shabaash"]["src"], meta["talk"]["src"], meta["idle"]["src"]):
        a, b = os.path.join(KIT, "sheets", sheet), os.path.join(CEL_DIR, sheet)
        if not (os.path.isfile(b) and filecmp.cmp(a, b, shallow=False)):
            shutil.copy2(a, b)
    out = os.path.join(tempfile.gettempdir(), "cel_track_%s.json" % CODE)
    subprocess.run([sys.executable, os.path.join(KIT, "make_lipsync.py"), vo_path, "--json", out],
                   check=True, capture_output=True)
    track = json.load(open(out, encoding="utf-8"))
    if "1" not in track["bits"]:
        sys.exit("X  the celebration VO measured silent - no lip-sync track")
    print("  OK  celebration Swiftie: 3 kit sheets in assets/UI/celebration/, lip-sync track from %s "
          "(%d ms, %d steps)" % (vo_id, track["ms"], len(track["bits"])))
    return {"base": "assets/UI/celebration/", "vo": vo_id, "meta": meta, "track": track}


CEL_WRAP = r"""
/* [r85] THE CELEBRATION SWIFTIE - the kit's README wrapper, verbatim in intent. The engine's
   CELEBRATION module is wrapped, not edited: it still does everything it did (sfx, sunburst, stars,
   the arrow), then the stock .end-mascot is hidden and a 300x358 host takes its place - the mascot's
   own 358 px layout height, so the arrow below it keeps its exact size and position.
   The clock is the clip's own - see THE CLOCK below. */
(function(){
  if(typeof SlideModules === "undefined" || !SlideModules.CELEBRATION || typeof CARD === "undefined"
     || !CARD.end_anim || typeof SwiftieCelebration === "undefined") return;
  const EA = CARD.end_anim;
  /* the three sheets (~2 MB) are fetched quietly 12 s after the lesson loads, so on a first visit
     they are in the cache long before the last page: the kit only starts loading them when the
     celebration mounts, and on a slow connection the jump (350 ms in) would play before its sheet
     had arrived. Kept referenced so the cached copies are not dropped. */
  const _warm = [];
  const warm = ()=> [EA.meta.shabaash, EA.meta.talk, EA.meta.idle].forEach(s => {
    const i = new Image(); i.decoding = "async"; i.src = EA.base + s.src; _warm.push(i); });
  const arm = ()=> setTimeout(warm, 12000);
  if(document.readyState === "complete") arm(); else window.addEventListener("load", arm);
  /* THE CLOCK. The kit takes `audio` - anything with paused / ended / currentTime - and anchors
     itself as  t0 = now - currentTime  the first time it sees the clip sounding. Measured here: the
     celebration mounts in a burst of work (sunburst, stars, sound), the page's main thread stalls
     150-330 ms right as the clip starts, and a yes/no "sounding" signal is only noticed on the first
     frame AFTER the stall - which put the whole lip-sync 170-1470 ms late when opened as a file.
     So the clock below reports how long the clip has really been audible, from the moment it
     became so, however late the next frame runs:
       · Web Audio (served): when the engine started the source, + the context's output latency
       · <audio> (opened as a file): the element's own "playing" event timestamp */
  const _st = AudioBufferSourceNode.prototype.start;
  AudioBufferSourceNode.prototype.start = function(when){
    try{ const c = this.context;
      this.__swcAt = performance.now() + ((when && when > c.currentTime) ? (when - c.currentTime) * 1000 : 0)
                     + ((c.baseLatency || 0) + (c.outputLatency || 0)) * 1000; }catch(e){}
    return _st.apply(this, arguments);
  };
  const heardAt = ()=>{
    const a = currentAudio;
    if(a){
      if(!a.__swc){ a.__swc = true;
        a.addEventListener("playing", (e)=>{ a.__swcAt = e.timeStamp - a.currentTime * 1000; }); }
      return a.paused ? null : (a.__swcAt != null ? a.__swcAt
                               : (a.currentTime > 0 ? performance.now() - a.currentTime * 1000 : null));
    }
    return currentVoiceSource && currentVoiceSource.__swcAt != null ? currentVoiceSource.__swcAt : null;
  };
  const clock = {
    get paused(){ return !isPlaying || heardAt() == null; },
    get ended(){ return !isPlaying; },
    get currentTime(){ const t = heardAt(); return t == null ? 0 : Math.max(0, performance.now() - t) / 1000; }
  };
  const _cel = SlideModules.CELEBRATION.mount;
  SlideModules.CELEBRATION.mount = function(host, slide){
    const r = _cel.apply(this, arguments);
    const img = document.querySelector("#endScreen .end-mascot");
    let box = document.getElementById("celBox");
    if(!box && img){ box = document.createElement("div"); box.id = "celBox";
      /* the stock mascot's OWN layout height, measured before it is hidden: 330 px wide at its
         516x476 art is 357.72 px, not the kit's 358 - and 0.28 px is a whole screen pixel of arrow
         movement at 1920x1080. Falls back to the kit's 358 if the stock art never loaded. */
      const h = (img.naturalWidth && img.offsetWidth) ? img.offsetWidth * img.naturalHeight / img.naturalWidth : 358;
      box.style.cssText = "width:300px;height:" + h + "px;position:relative;z-index:2";
      img.parentNode.insertBefore(box, img); }
    if(!box) return r;
    if(img) img.style.display = "none";
    box.innerHTML = "";
    /* [r106] SHE JUMPS AND CELEBRATES FIRST, THEN SPEAKS. Yasir: "in the last celebration screen Swifty
       jumps and celebrates, then starts speaking - the VO should only play when she starts speaking".
       So the line is NOT played by the page on arrival (ownsAudio): the jump - the kit's own शाबाश
       sheet, its standing frames and its jump frames - plays first, silent but for the celebration
       sound; then the line starts and the kit's player takes over, with a track arranged so that it
       finishes the landing over the clip's lead-in and then lip-syncs the WHOLE line on the talk
       sheet (a 25 ms stand-in "first word" stops the kit spending the real first words on a jump). */
    state.ownsAudio = true;
    const M = EA.meta, S = M.shabaash, COLS = M.cols || 6;
    const sp = document.createElement("div"); sp.className = "swc-sprite";
    sp.innerHTML = '<div class="swc-art"></div>'; box.appendChild(sp);
    const art = sp.firstChild; art.style.aspectRatio = M.fw + " / " + M.fh;
    art.style.backgroundImage = 'url("' + EA.base + S.src + '")';
    const showF = (i)=>{ const c = i % COLS, rr = Math.floor(i / COLS);
      art.style.backgroundPosition = (c * 100 / (COLS - 1)) + "% " + (rr * 100 / (COLS - 1)) + "%";
      sp.dataset.sheet = "shabaash"; sp.dataset.f = i; };
    const frames = S.pre.concat(S.word), FMS = 45;          /* ~22 fps: 30 frames, 1.35 s */
    showF(frames[0]);
    const bits = EA.track.bits, lead = Math.max(0, bits.indexOf("1"));
    const step = EA.track.step_ms || 25;
    const bits2 = "1" + "00000000" + bits.slice(lead);      /* stand-in word, 200 ms gap, the line */
    const shift = (9 - lead) * step / 1000;                 /* keeps the line on the clip's clock */
    const clock2 = {
      get paused(){ return clock.paused; }, get ended(){ return clock.ended; },
      get currentTime(){ const t = clock.currentTime; return t > 0 ? Math.max(0.001, t + shift) : 0; }
    };
    const t0 = performance.now();
    (function jump(){
      if(!sp.isConnected || CARD.slides[state.idx] !== slide) return;
      const k = Math.floor((performance.now() - t0) / FMS);
      if(k < frames.length){ showF(frames[k]); requestAnimationFrame(jump); return; }
      /* the jump is over: the line starts, and the kit takes over the moment it is sounding */
      const src = (typeof audioFor === "function") ? audioFor(slide, "prompt") : null;
      if(src) play(src, ()=>{});
      const h = SwiftieCelebration.play({ host: box, meta: M, base: EA.base, bits: bits2, step_ms: step, audio: clock2 });
      h.el.style.animation = "none"; h.el.style.position = "absolute"; h.el.style.inset = "0";
      h.el.style.visibility = "hidden";
      (function swap(){
        if(!h.el.isConnected) return;
        if(h.el.dataset.t !== undefined || h.el.dataset.sheet === "idle"){ h.el.style.visibility = ""; sp.remove(); return; }
        requestAnimationFrame(swap);
      })();
    })();
    return r;
  };
})();
"""


def inject_celebration(html, card):
    if not card.get("end_anim") or 'id="swcKit"' in html:
        return html
    css = open(os.path.join(KIT, "swiftie_celebration.css"), encoding="utf-8").read()
    js = open(os.path.join(KIT, "swiftie_celebration.js"), encoding="utf-8").read()
    html, n1 = re.subn(r"</head>", lambda m: '<style id="swcKitCss">\n' + css + "</style>\n</head>", html, count=1)
    i = html.rfind("</body>")
    if n1 != 1 or i < 0:
        sys.exit("X  could not inject the celebration Swiftie")
    html = html[:i] + '<script id="swcKit">\n' + js + "\n" + CEL_WRAP + "</script>\n" + html[i:]
    print("  OK  celebration Swiftie injected (kit player + CELEBRATION.mount wrapper)")
    return html


def main():
    argparse.ArgumentParser().parse_args()
    # [r126] pictures -> WebP, videos -> WebM, before anything reads the asset folders (see the script)
    import subprocess
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "normalize_assets.py")], check=True)
    if not os.path.isfile(ENGINE):
        sys.exit("X  no engine at %s" % ENGINE)
    src = open(ENGINE, encoding="utf-8").read()
    ver = guard_engine(src)

    guard_single_matra()
    slides = build_slides()
    guard_flow(slides)
    guard_sentences(slides)
    guard_word_build(slides)
    card = build_card(slides)
    if sum(card["phase_distribution"].values()) != len(slides):
        sys.exit("X  phase_distribution does not sum to the slide count")
    guard_prompts(slides)
    guard_register(slides, card)
    guard_mechanics(slides)
    guard_pictures(slides, card)
    guard_audio(slides, card)

    for d in ("assets/Audio", "assets/Images", "assets/UI"):
        os.makedirs(os.path.join(BUNDLE, d), exist_ok=True)
    check_chrome()

    stale, orphan, img_orphan = prune_stale(card)
    if stale or orphan:
        print("  OK  cleared %d stale clip(s) (text changed) + %d orphan(s) (screen gone) — "
              "gen_tts will re-record exactly these" % (len(stale), len(orphan)))
    if img_orphan:
        print("  !!  images no longer used by the card (delete before packaging): %s" % img_orphan)

    card["end_anim"] = celebration_anim(slides)          # [r85]
    if not card["end_anim"]:
        del card["end_anim"]
    payload = json.dumps(card, ensure_ascii=False, indent=1)
    if not CARD_TAG.search(src):
        sys.exit("X  cardData tag not found")
    html = CARD_TAG.sub(lambda m: m.group(1) + payload + m.group(3), src, count=1)

    first = [k for k in ("obj_pul", "obj_phool") if k in card["assets"]["image"]]
    # [r126] the head's high-priority preloads are the COVER's train pictures - the first thing the child
    # sees, and on a slow line the thing that went missing. The page-2 pictures load with the rest.
    del first
    links = "".join('<link rel="preload" as="image" fetchpriority="high" href="assets/UI/%s">' % f
                    for f in ("train_still.webp", "train_spritesheet.webp"))
    html, n_pre = re.subn(r'(?:<link rel="preload" as="image"[^>]*>)+', links, html, count=1)
    declared = set(card["assets"]["image"])
    bad = sorted(set(re.findall(r'<link rel="preload"[^>]*href="assets/Images/([^".]+)\.\w+"',
                                html)) - declared)
    if bad:
        sys.exit("X  preload points at missing art: %s" % bad)
    print("  OK  preload: the cover's train pictures (%d block rewritten)" % n_pre)

    if 'id="bundleLetterGlow"' not in html:
        html, n = re.subn(r"</head>", LETTER_GLOW_CSS + "</head>", html, count=1)
        if n != 1:
            sys.exit("X  could not inject the letter glow")
        print("  OK  letter-strip glow injected")
    html = inject_celebration(html, card)                # [r85]


    # [r17] AUDIO CACHE VERSION. Hash every clip's bytes, so the stamp moves when a recording
    # changes and stays put when it does not. Without this a re-recorded clip keeps its filename,
    # the browser serves the copy it already has, and the reviewer hears the take we just replaced
    # - which is exactly what happened with vo_t3_prompt and vo_t5_prompt.
    _h = hashlib.sha1()
    for _f in sorted(os.listdir(AUD_DIR)):
        if _f.endswith(".ogg"):
            _h.update(_f.encode("utf-8"))
            _h.update(open(os.path.join(AUD_DIR, _f), "rb").read())
    html = html.replace("__AUDIO_V_STAMP__", _h.hexdigest()[:12])
    # [r80] the same for the runner game's own sounds: its voice clips, its music and the two
    # feedback sounds it plays. Hashed by content, so the stamp moves only when one changes.
    _mr = os.path.join(BUNDLE, "assets", "MatraRunner")
    _mh = hashlib.sha1()
    _mfiles = [os.path.join(_mr, "voice", f) for f in sorted(os.listdir(os.path.join(_mr, "voice")))
               if f.endswith(".ogg")]
    _mfiles += [os.path.join(_mr, "bgm_game.ogg"),
                os.path.join(AUD_DIR, "sfx_fb_correct.ogg"), os.path.join(AUD_DIR, "sfx_fb_incorrect.ogg")]
    for _f in _mfiles:
        if os.path.exists(_f):
            _mh.update(os.path.basename(_f).encode("utf-8")); _mh.update(open(_f, "rb").read())
    _n_mr = html.count("__MR_AUDIO_V_STAMP__")
    html = html.replace("__MR_AUDIO_V_STAMP__", _mh.hexdigest()[:12])
    print("  OK  runner audio stamp %s (%d)" % (_mh.hexdigest()[:12], _n_mr))
    # [r124] ...and for its pictures and video (every file directly in assets/MatraRunner/), which
    # were requested with no version at all and so stayed in a device's cache across redeploys
    _ah = hashlib.sha1()
    for _f in sorted(os.listdir(_mr)):
        _p = os.path.join(_mr, _f)
        if os.path.isfile(_p):
            _ah.update(_f.encode("utf-8")); _ah.update(open(_p, "rb").read())
    _n_art = html.count("__MR_ART_V_STAMP__")
    if not _n_art:
        sys.exit("X  the runner's art stamp placeholder is missing - re-run embed_matra_runner.py")
    html = html.replace("__MR_ART_V_STAMP__", _ah.hexdigest()[:12])
    # [r126] ...and the list of the game's pictures, for the lesson to fetch ahead (warmRunner): read
    # from the game's own art table, so it is exactly what the game will ask for
    _rs = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "matra_runner_src", "index.html"),
               encoding="utf-8").read()
    _art = sorted(set(re.findall(r'\[\s*"([\w.-]+\.webp)"\s*,\s*\d+\s*\]', _rs) +
                      re.findall(r'"--mr-ui-[\w-]+"\s*:\s*"([\w.-]+\.webp)"', _rs) + ["panel3.webp"]))
    _art = [f for f in _art if os.path.isfile(os.path.join(_mr, f))] + ["coin.svg"]
    if html.count("__MR_ART_LIST__") != 1 or len(_art) < 20:
        sys.exit("X  runner warm-up list: placeholder %d, %d files" % (html.count("__MR_ART_LIST__"), len(_art)))
    html = html.replace("__MR_ART_LIST__", ",".join(_art))
    print("  OK  runner warm-up list: %d pictures" % len(_art))
    print("  OK  runner art stamp %s (%d)" % (_ah.hexdigest()[:12], _n_art))
    open(os.path.join(BUNDLE, CODE + ".html"), "w", encoding="utf-8").write(html)
    open(os.path.join(BUNDLE, "card.json"), "w", encoding="utf-8").write(payload + "\n")

    risky = write_vo_list()
    art = write_art_manifest(slides)

    print("  OK  card:   %d slides  %s" % (len(slides), card["phase_distribution"]))
    print("  OK  audio:  %d to record + %d copied  (%d flagged EAR-CHECK)"
          % (len(AUDIO_TEXT), len(COPY_AUDIO), len(risky)))
    print("  OK  images: %d on disk" % len(card["assets"]["image"]))
    if art["pending"]:
        print("  !!  ART PENDING (%d) — rendering as the emoji fallback until generated: %s"
              % (len(art["pending"]), ", ".join(sorted(art["pending"]))))
    gap = [v for v in AUDIO_TEXT if not os.path.isfile(os.path.join(AUD_DIR, v + ".ogg"))]
    if gap:
        print("  !!  VO PENDING (%d of %d) — these fall back to a silent beat until recorded"
              % (len(gap), len(AUDIO_TEXT)))
    print("  OK  html:   %s.html  (engine %s)" % (CODE, ver))


if __name__ == "__main__":
    main()
