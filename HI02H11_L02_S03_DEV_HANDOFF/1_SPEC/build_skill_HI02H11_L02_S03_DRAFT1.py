# -*- coding: utf-8 -*-
"""Build HI02H11_L02_S03 (ए / ऐ) — «मात्राओं की रेल», the SME's finalised train flow.

SKILL CODE. The SME assigned ए/ऐ to S03 on 2026-09-24. The curriculum sheet still lists S03 as
ओ/औ + अं/अः and puts ए/ऐ under S02 Part-2; that row has NOT been edited here. Reconcile the sheet
before ओ/औ is built, or the codes collide.

FLOW = THE SME'S FINALISED S02 DECK, SCREEN FOR SCREEN — 18 screens (landing + 17), the round-3
structure recorded in ../G2/HI02H11_L02_S02_DEV_HANDOFF/1_SPEC/_SME_RECOMMENDATIONS_ROUND3.md.

    screen  module              this lesson
    ------------------------------------------------------------------
      --    landing             ◌े ◌ै in the train bogies
      1     MATRA_INTRO         ए → ◌े · ऐ → ◌ै
      2     MATRA_BUILD         सब → स + े = से → सेब
      3     MEET_PAIR           सेब, पेड़
      4     MATRA_BUILD         पर → प + ै = पै → पैर
      5     MEET_PAIR           पैर, बैल
      6-8   TRAIN_TAP x3        े · ै · mixed
      9     TRAIN_SORT word     words  -> matra bin
     10     TRAIN_SORT matra    matras -> letter bin  (the reverse round)
     11     WORD_BUILD          _ब · _र · _ल   (drag the AKSHARA, not the matra)
     12     TRAIN_SORT picture  pictures only, the word is spoken not shown
     13-16  SENTENCE_COMPLETE   four sentences — decoding becomes MEANING
     17     CELEBRATION

REGISTER IS आप THROUGHOUT (कीजिए · सोचिए · देखिए · डालिए · सुनिए · पहचानिए · चुनिए), per the SME's
round-3 note, stated twice: "Use respectful language throughout". This also removes the mismatch
with the engine's shared phase-gate clips, which already speak आप. The sibling S02 is still तुम.

THE IN-WORD HIGHLIGHT WORKS HERE. े and ै are ABOVE-BASE marks: zero advance (so the engine's own
column-clip cannot touch them, exactly as with ु/ू) but the cluster's ink rises 27-31px above the
consonant at 100px. matraHL()'s third mode clips that band. Verified through the real module:
सेब clipped 0 → 26.8 with the baseline at 68, while पुल still clipped 76.8 → 111.4 — i.e. उ/ऊ is
unregressed. See engine_local/CHANGES.md.

    ⚠️ ओ/औ (ो, ौ) will NOT be covered by that work — they are right-spacing AND above-base at
    once, so the advance test fires first and the hook above the consonant is missed.

Run:  PYTHONUTF8=1 py -3.13 build_skill_HI02H11_L02_S03.py
"""
import os, re, sys, json, shutil

CODE     = "HI02H11_L02_S03"
KIT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FLN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REF_DIR  = os.path.join(KIT_ROOT, "KG and G1 refernce ready HTML's")
BUNDLE   = os.path.join(FLN_ROOT, "G2", CODE)
ENGINE   = os.path.join(BUNDLE, "engine_local", "lesson_template.html")
SIBLING  = os.path.join(FLN_ROOT, "G2", "HI02H11_L02_S02")
CARD_TAG = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)
VER_RE   = re.compile(r'ENGINE_VERSION\s*=\s*["\']([^"\']+)["\']')
RSM_RE   = re.compile(r'RIGHT_SPACING_MATRAS\s*=\s*new Set\(\[([^\]]*)\]\)')

TRAIN_MODULES = ["TRAIN_TAP", "TRAIN_SORT", "MATRA_BUILD", "MEET_PAIR", "MATRA_INTRO",
                 "WORD_BUILD", "SENTENCE_COMPLETE"]
STOCK_MODULES = ["CELEBRATION"]
COPY_AUDIO = ["vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice",
              "sfx_celebrate", "sfx_correct", "sfx_wrong", "sfx_tap", "sfx_pop"]

E, AI = "े", "ै"
ALL_MATRAS = set("ािीुूृेैोौ")

# ---------------------------------------------------------------- an accepted gate breach
# The Mechanic-Diversity Gate wants no gesture family above 60% of the test slides. This lesson
# is 73% drag (3 TRAIN_SORT + 1 WORD_BUILD + 4 SENTENCE_COMPLETE against 3 TRAIN_TAP) and there
# is no arrangement of the SME's finalised 18-screen flow that passes:
#
#     SENTENCE_COMPLETE as drag  ->  3 pick / 8 drag  = 73% drag
#     SENTENCE_COMPLETE as tap   ->  7 pick / 4 drag  = 64% pick
#     …as tap, with 3 sentences  ->  6 pick / 4 drag  = 60% pick   (passes, but drops a screen)
#
# So the breach is structural, not accidental: in a train lesson, dragging a card into a coach
# IS the core metaphor, and the SME specified drag for the sentence screens in as many words
# («snaps into the blank space», «returns to its original position»).
#
# Accepted deliberately, printed loudly at every build, and flagged to the SME rather than
# quietly switching the gate off. If they would rather keep the gate, the cheapest fix is to
# drop one sentence screen and make the remaining three tap.
MECHANIC_SKEW_ACCEPTED = True
MECHANIC_SKEW_REASON = ("The SME's finalised flow is drag-led by design; no arrangement of it "
                        "passes. Awaiting their ruling — see the module header.")

# ---------------------------------------------------------------- content
# key -> (word, emoji, matra).
#
# EVERY WORD CARRIES EXACTLY ONE MATRA, AND IT IS THE TARGET ONE. The sort screens ask "which
# matra does this word have", so a word with a second matra has no single right answer. That
# rule is what excluded the obvious everyday picks — केला, थैला, पैसा and मैना all carry a
# trailing ा as well — the same rule that excluded कुत्ता / गुलाब / जूता from the उ/ऊ lesson.
# guard_single_matra proves it every build rather than trusting this comment.
OBJ = {
    "obj_seb":  ("सेब",  "\U0001F34E", E),    # apple
    "obj_ped":  ("पेड़",  "\U0001F333", E),    # tree
    "obj_rail": ("रेल",  "\U0001F682", E),    # train — and the lesson's own theme
    "obj_mez":  ("मेज़",  "\U0001FA91", E),    # table
    "obj_pair": ("पैर",  "\U0001F9B6", AI),   # foot — the child's own body
    "obj_bail": ("बैल",  "\U0001F402", AI),   # ox
    "obj_bag":  ("बैग",  "\U0001F392", AI),   # school bag
    "obj_pen":  ("पैन",  "\U0001F58A", AI),   # pen
}

# Full scenes for SENTENCE_COMPLETE. A different asset class from the cut-out objects above:
# these keep their background on purpose and must NOT go through the chroma-key pipeline.
SCENE = {
    "scn_bageecha": "\U0001F333",
    "scn_pair_dard": "\U0001F9B6",
    "scn_seb_khana": "\U0001F34E",
    "scn_likhna":    "\U0001F58A",
}

MATRA_VO   = {E: "vo_matra_e", AI: "vo_matra_ai"}
MATRA_TEXT = {"vo_matra_e": "ए की मात्रा", "vo_matra_ai": "ऐ की मात्रा"}
MATRA_NAME = {E: "ए", AI: "ऐ"}
# SME round-3: coach labels carry ONLY the letter — no छोटी/बड़ी, no matra symbol.
MATRA_LABEL = {E: "ए", AI: "ऐ"}

AUDIO_TEXT = {}


def vo(vid, text):
    if vid in AUDIO_TEXT and AUDIO_TEXT[vid] != text:
        raise ValueError("clip %s registered twice with different text:\n  %s\n  %s"
                         % (vid, AUDIO_TEXT[vid], text))
    AUDIO_TEXT[vid] = text
    return vid


def slug(key):
    return key[4:] if key.startswith("obj_") else key


def key_of(word):
    for k, v in OBJ.items():
        if v[0] == word:
            return k
    sys.exit("X  no OBJ entry for %r" % word)


def matra_of(word):
    for _k, (w, _e, m) in OBJ.items():
        if w == word:
            return m
    sys.exit("X  no matra known for %r" % word)


def name_clip(word):
    return vo("vo_name_" + slug(key_of(word)), word)


# ---------------------------------------------------------------- screens
def s_intro(sid):
    p = "आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।"
    i = "किसी अक्षर के ऊपर मात्रा लगती है, तो उसकी आवाज़ बदल जाती है।"
    return {"id": sid, "phase": "tutorial", "eis": "enactive", "type": "MATRA_INTRO",
            "prompt_hi": p,
            "audio": {"prompt": vo("vo_%s_prompt" % sid.lower(), p),
                      "instruction": vo("vo_%s_instruction" % sid.lower(), i)},
            "data": {"pairs": [
                        {"letter": "ए", "matra": E,
                         "audio": vo("vo_pair_e", "यह है ए। इसकी मात्रा है, ए की मात्रा।")},
                        {"letter": "ऐ", "matra": AI,
                         "audio": vo("vo_pair_ai", "यह है ऐ। इसकी मात्रा है, ऐ की मात्रा।")}],
                     "phonemes": dict(MATRA_VO), "auto": True}}


def s_build(sid, base_word, consonant, matra, syllable, result_word):
    """The transformation teach, in the SME's round-3 wording.

    They corrected the phrasing explicitly: use «<अक्षर> के साथ <मात्रा> की मात्रा लगाने पर 'X'
    बनता है», NOT «<अक्षर> में … लगी, बना X». The S02 build said «के नीचे», which was both the
    wrong preposition and wrong for this skill — here the matra goes ON TOP.
    """
    rk = key_of(result_word)
    g = slug(rk)
    a = {
        "prompt":  vo("vo_%s_prompt" % sid.lower(),
                      "आइए, देखें कि %s की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।"
                      % MATRA_NAME[matra]),
        # COMMA, NOT AN EM-DASH. The SME writes «यह शब्द देखिए — सब।», but an em-dash before a
        # short final word truncates this TTS voice (measured 0.73-1.05s against a 1.53-2.21s
        # peer median on the sibling). The comma form synthesises reliably and reads the same.
        "base":    vo("vo_base_" + base_word, "यह शब्द देखिए, %s।" % base_word),
        "matra_name": MATRA_VO[matra],
        "onset":   vo("vo_onset_" + g,
                      "%s के साथ %s की मात्रा लगाने पर, %s बनता है।"
                      % (consonant, MATRA_NAME[matra], syllable)),
        "result":  name_clip(result_word),
        "explain": vo("vo_%s_explain" % sid.lower(),
                      "अब %s जुड़ने पर, %s बनता है।"
                      % (result_word[len(syllable):], result_word)),
    }
    return {"id": sid, "phase": "tutorial", "eis": "symbolic", "type": "MATRA_BUILD",
            "prompt_hi": "%s में %s की मात्रा लगाने पर %s बनता है।"
                         % (base_word, MATRA_NAME[matra], result_word),
            "audio": a,
            "data": {"base_word": base_word, "consonant": consonant, "matra": matra,
                     "syllable": syllable, "result_word": result_word,
                     "result_img": rk, "result_emoji": OBJ[rk][1],
                     # the matra travels DOWN from above, because that is where ए/ऐ sit
                     "travel": "down",
                     "base_img": None, "base_emoji": None,
                     "cap_base": "यह शब्द देखिए, %s" % base_word,
                     "cap_mid": "%s के साथ %s की मात्रा लगाने पर %s बनता है।"
                                % (consonant, MATRA_NAME[matra], syllable),
                     "cap_result": "%s से बना %s" % (base_word, result_word)}}


def s_pair(sid, words, lead, head):
    ex = []
    for w in words:
        k = key_of(w); m = matra_of(w)
        ex.append({"word": w, "matra": m, "img": k, "emoji": OBJ[k][1],
                   "audio_line": vo("vo_meet_" + slug(k),
                                    "%s में %s की मात्रा लगी है।" % (w, MATRA_NAME[m])),
                   "matra_audio": MATRA_VO[m]})
    return {"id": sid, "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
            "prompt_hi": head,
            "audio": {"prompt": vo("vo_%s_prompt" % sid.lower(), lead)},
            "data": {"examples": ex}}


def _test_audio(sid, prompt, hint1, hint2, correct):
    return {"prompt": vo("vo_%s_prompt" % sid.lower(), prompt),
            "hint1":  vo("vo_%s_hint1" % sid.lower(), hint1),
            "hint2":  vo("vo_%s_hint2" % sid.lower(), hint2),
            "correct": vo("vo_%s_correct" % sid.lower(), correct)}


def s_tap(sid, words, target, matra):
    p = "जिस डिब्बे में %s की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" % MATRA_NAME[matra]
    return {"id": sid, "phase": "guided", "eis": "symbolic", "type": "TRAIN_TAP",
            "prompt_hi": "%s की मात्रा वाले शब्द पर टैप कीजिए।" % MATRA_NAME[matra],
            "audio": _test_audio(
                sid, p,
                "फिर से सोचिए। %s की मात्रा वाला शब्द कौन-सा है?" % MATRA_NAME[matra],
                "ध्यान से देखिए। अक्षर के ऊपर कौन-सी मात्रा लगी है?",
                "शाबाश! %s शब्द में %s की मात्रा है।" % (target, MATRA_NAME[matra])),
            # SME round-3: do NOT highlight the matra before the answer — it would give it away.
            # The module only calls matraHL on the correct coach AFTER the tap.
            "data": {"target": target, "matra": matra,
                     "coaches": [{"word": w, "correct": (w == target)} for w in words]}}


def card_of(word):
    k = key_of(word)
    return {"bin": matra_of(word), "word": word, "img": k,
            "emoji": OBJ[k][1], "audio": name_clip(word)}


def s_sort(sid, phase, kind, bins, cards, prompt, hint2):
    bin_list = ([{"key": b, "label": MATRA_LABEL[b]} for b in bins]
                if kind != "matra" else [{"key": b["key"], "label": b["label"]} for b in bins])
    return {"id": sid, "phase": phase, "eis": "enactive", "type": "TRAIN_SORT",
            "prompt_hi": prompt,
            "audio": _test_audio(
                sid, prompt, "फिर से सुनिए और सही मात्रा पहचानिए।", hint2,
                "शाबाश! आपने सारे शब्द सही डिब्बे में डाल दिए।"),
            "data": {"kind": kind, "bins": bin_list, "cards": cards}}


def s_word_build(sid):
    """Drag the AKSHARA (consonant+matra already joined) into a leading blank.

    SME round-3 rewrote MATRA_FILL into this: the child no longer assembles स + े, they pick
    `से` whole. Distractors are required — options carry aksharas matching no picture.
    """
    slots = []
    for word, post, answer in [("सेब", "ब", "से"), ("पैर", "र", "पै"), ("रेल", "ल", "रे")]:
        k = key_of(word)
        # PER-SLOT matra, not one for the screen: सेब and रेल carry े while पैर carries ै,
        # so a screen-level value would highlight the wrong mark on two of the three words.
        slots.append({"word": word, "post": post, "answer": answer, "matra": matra_of(word),
                      "img": k, "emoji": OBJ[k][1], "audio": name_clip(word)})
    opts = ["से", "पै", "रे", "बै", "मे"]          # 3 answers + 2 distractors
    p = "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"
    d = {"slots": slots, "options": opts,
         "option_audio": {o: vo("vo_akshara_" + str(i), o) for i, o in enumerate(opts)}}
    return {"id": sid, "phase": "practice", "eis": "enactive", "type": "WORD_BUILD",
            "prompt_hi": p,
            "audio": _test_audio(
                sid, p,
                "फिर से सोचिए और चित्र को ध्यान से देखिए।",
                "ध्यान से देखिए, कौन-सा अक्षर लगाने से शब्द पूरा होगा?",
                "शाबाश! आपने तीनों शब्द पूरे कर दिए।"),
            "data": d}


SENTENCES = [
    ("बगीचे में एक बड़ा ", " है।", "पेड़",  "scn_bageecha",  ["पेड़", "बैल", "पैन"]),
    ("मेरे ",              " में दर्द है।", "पैर", "scn_pair_dard", ["पैर", "सेब", "रेल"]),
    ("मुझे ",              " खाना अच्छा लगता है।", "सेब", "scn_seb_khana", ["सेब", "बैग", "मेज़"]),
    ("मैं ",               " से लिखता हूँ।", "पैन", "scn_likhna",   ["पैन", "पेड़", "बैल"]),
]


def s_sentence(sid, pre, post, answer, scene, options):
    """The step from decoding to MEANING — the only screen where the matra alone cannot
    answer it. All three options are readable real words; only the sentence picks one."""
    p = "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।"
    opts = []
    for w in options:
        k = key_of(w)
        opts.append({"word": w, "img": k, "emoji": OBJ[k][1], "audio": name_clip(w)})
    return {"id": sid, "phase": "practice", "eis": "symbolic", "type": "SENTENCE_COMPLETE",
            "prompt_hi": "सही शब्द चुनकर वाक्य पूरा कीजिए।",
            "audio": _test_audio(
                sid, p,
                "फिर से सोचिए। कौन-सा शब्द वाक्य को पूरा करेगा?",
                "चित्र को ध्यान से देखिए और सही शब्द चुनिए।",
                vo_text_correct(pre, post, answer)),
            "data": {"scene_img": scene, "scene_emoji": SCENE[scene],
                     "sentence_pre": pre, "sentence_post": post,
                     "answer": answer, "matra": matra_of(answer), "options": opts}}


def vo_text_correct(pre, post, answer):
    return "शाबाश! " + (pre + answer + post).strip()


def build_slides():
    S = []
    # ---- TUTORIAL (5) — autonomous, zero taps --------------------------------------
    S.append(s_intro("T1"))
    S.append(s_build("T2", "सब", "स", E,  "से", "सेब"))
    S.append(s_pair("T3", ["सेब", "पेड़"],
                    "आइए, ए की मात्रा वाले कुछ शब्द देखिए।",
                    "ए की मात्रा वाले शब्द पढ़िए।"))
    S.append(s_build("T4", "पर", "प", AI, "पै", "पैर"))
    S.append(s_pair("T5", ["पैर", "बैल"],
                    "आइए, ऐ की मात्रा वाले कुछ शब्द देखिए।",
                    "ऐ की मात्रा वाले शब्द पढ़िए।"))

    # ---- GUIDED (5) ----------------------------------------------------------------
    S.append(s_tap("G1", ["सेब", "पैर", "बैल"], "सेब", E))
    S.append(s_tap("G2", ["पेड़", "रेल", "बैग"], "बैग", AI))
    S.append(s_tap("G3", ["मेज़", "पैन", "रेल"], "पैन", AI))       # mixed: ऐ among two ए
    S.append(s_sort("G4", "guided", "word", [E, AI],
                    [card_of(w) for w in ["सेब", "पेड़", "पैर", "बैल"]],
                    "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
                    "अक्षर के ऊपर देखिए। एक लकीर है, तो ए। दो लकीरें हैं, तो ऐ।"))
    # the REVERSE round: coaches carry the LETTER, the child drags the MATRA
    S.append(s_sort("G5", "guided", "matra",
                    [{"key": E, "label": "ए"}, {"key": AI, "label": "ऐ"}],
                    [{"bin": E,  "word": "◌" + E,  "audio": MATRA_VO[E]},
                     {"bin": AI, "word": "◌" + AI, "audio": MATRA_VO[AI]}],
                    "सही मात्रा को सही डिब्बे में डालिए।",
                    "ध्यान से देखिए, यह किसकी मात्रा है?"))

    # ---- PRACTICE (7) --------------------------------------------------------------
    S.append(s_word_build("P1"))
    S.append(s_sort("P2", "practice", "picture", [E, AI],
                    [card_of(w) for w in ["रेल", "मेज़", "बैग", "पैन"]],
                    "चित्र को सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    "शब्द को ध्यान से सुनिए। अक्षर के ऊपर कौन-सी मात्रा है?"))
    for n, (pre, post, ans, scn, opts) in enumerate(SENTENCES, 1):
        S.append(s_sentence("P%d" % (n + 2), pre, post, ans, scn, opts))

    recap = "शाबाश! आज हमने सीखा, ए और ऐ की मात्रा पहचानना, और मात्रा वाले शब्द पढ़ना।"
    S.append({"id": "CEL", "phase": "practice", "eis": "iconic", "type": "CELEBRATION",
              "prompt_hi": recap,
              "audio": {"prompt": vo("vo_cel_prompt", recap)}, "data": {}})
    return S


def build_card(slides):
    for vid, text in MATRA_TEXT.items():
        vo(vid, text)
    vo("vo_landing", "नमस्ते दोस्त! मैं हूँ स्विफ्टी। "
                     "आज हम मात्राओं की रेल में ए और ऐ की मात्रा सीखेंगे।")
    vo("vo_try_again", "एक बार फिर सुनिए।")

    counts = {}
    for s in slides:
        counts[s["phase"]] = counts.get(s["phase"], 0) + 1
    audio = {v: "assets/Audio/%s.ogg" % v for v in sorted(AUDIO_TEXT)}
    for v in COPY_AUDIO:
        audio.setdefault(v, "assets/Audio/%s.ogg" % v)
    image = {k: "assets/Images/%s.png" % k for k in sorted(list(OBJ) + list(SCENE))}

    return {
        "version": "0.1", "skill_code": CODE, "lo_code": "HI02H11_L02",
        "grade": "02", "attribute": "H11", "skill_type": "CORE",
        "medium": "hi",
        "title": {"hi": "मात्राओं की रेल", "en": "Matra train — the e / ai matras"},
        "subtitle_hi": "",
        "theme": "toybox",
        "skill_description_hi": ("ए, ऐ मात्रा वाले शब्द पढ़ता है। "
                                 "शब्दों में आने वाली मात्रा पहचानता है।"),
        "landing_audio": "vo_landing",
        "landing_hero": {"kind": "concept_strip", "cells": [
            {"type": "letter", "letter": "◌" + E,  "label": "ए"},
            {"type": "letter", "letter": "◌" + AI, "label": "ऐ"},
        ]},
        "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                                   "practice": "vo_pt_practice"},
        "phase_transition_title": {"tutorial": "चलिए, रेल चलाएँ!", "guided": "साथ में करते हैं।",
                                   "practice": "अब आपकी बारी।"},
        "phase_distribution": counts,
        # nudge_timeout_ms is the engine's HAND timer and [28i] makes the engine REFUSE it
        # outside tutorial, so these two values have never done anything. Left in place because
        # every card in the fleet carries them and removing one card's is worse than a
        # consistent no-op; `idle_hint_ms` is the knob that is actually read (see makeHints).
        "scaffold_rules": {"nudge_timeout_ms": {"guided": 6000, "practice": 8000},
                           "idle_hint_ms": 9000,
                           "max_attempts": 3, "hand_on_attempt": 2,
                           "reveal_on_attempt": None, "silent_on_late_correct": True},
        "signals_expected": ["slide_entered", "slide_completed", "train_tap_first_try",
                             "matra_sort_item", "matra_sort_first_try", "word_build_item",
                             "word_build_first_try", "sentence_complete", "answer_wrong",
                             "hint_shown", "idle_cue", "phase_transition", "mastery_score",
                             "lesson_completed"],
        "_emoji_fallback": dict({k: v[1] for k, v in OBJ.items()}, **SCENE),
        "assets": {"audio": audio, "audio_text": AUDIO_TEXT, "image": image,
                   "audio_ext": "ogg", "img_ext": "png"},
        "slides": slides,
    }


# ---------------------------------------------------------------- guards
TEST_TYPES = ("TRAIN_TAP", "TRAIN_SORT", "MATRA_FILL", "WORD_BUILD",
              "SENTENCE_COMPLETE")


def guard_engine(src):
    m = VER_RE.search(src)
    if not m:
        sys.exit("X  no ENGINE_VERSION in engine_local")
    ver = m.group(1)
    for name in TRAIN_MODULES:
        if ("SlideModules." + name + " = {") not in src:
            sys.exit("X  engine_local is missing the train module %s. Re-run "
                     "engine_local/inject_train.py; do NOT hand-edit the monolith." % name)
    for name in STOCK_MODULES:
        if not (re.search(r'^\s{2}"?' + name + r'"?\s*[:(]', src, re.M)
                or re.search(r'SlideModules\.' + name + r'\s*=', src)):
            sys.exit("X  engine_local is missing the stock module %s" % name)
    if "TRAIN STYLES :: BEGIN" not in src:
        sys.exit("X  the train CSS block is missing — the coaches would render unstyled")
    if "_inkAscent" not in src:
        sys.exit("X  matraHL has no above-base mode (_inkAscent missing). े and ै would be\n"
                 "     clipped BELOW the baseline, colouring nothing. Re-run the injector.")
    rsm = RSM_RE.search(src)
    inset = set(re.findall(r'"([^"]+)"', rsm.group(1))) if rsm else set()
    for bad in (E, AI):
        if bad in inset:
            sys.exit("X  %r is in RIGHT_SPACING_MATRAS. It is ABOVE-BASE with ZERO advance:\n"
                     "     a column clip would colour the consonant and its neighbour, not the\n"
                     "     mark. matraHL's above-base mode handles it; remove it from the set."
                     % bad)
    if 'case "letter":' not in src:
        sys.exit("X  conceptTileHTML has no `letter` case — the landing strip would be empty")
    print("  OK  engine: %s  (per-game engine_local)" % ver)
    print("      modules: %s" % ", ".join(TRAIN_MODULES))
    print("      above-base highlight present; े/ै correctly OUT of RIGHT_SPACING_MATRAS")
    return ver


def guard_single_matra():
    bad = []
    for k, (w, _e, m) in OBJ.items():
        found = [c for c in w if c in ALL_MATRAS]
        if len(found) != 1 or found[0] != m:
            bad.append((w, "".join(found) or "none"))
    if bad:
        sys.exit("X  guard_single_matra: these words do not carry exactly one target matra, so\n"
                 "     'which matra is in this word' has no single answer: %s" % bad)
    print("  OK  single-matra rule: all %d words carry exactly one target matra" % len(OBJ))


def guard_flow(slides):
    want = ["MATRA_INTRO", "MATRA_BUILD", "MEET_PAIR", "MATRA_BUILD", "MEET_PAIR",
            "TRAIN_TAP", "TRAIN_TAP", "TRAIN_TAP", "TRAIN_SORT", "TRAIN_SORT",
            "WORD_BUILD", "TRAIN_SORT", "SENTENCE_COMPLETE", "SENTENCE_COMPLETE",
            "SENTENCE_COMPLETE", "SENTENCE_COMPLETE", "CELEBRATION"]
    got = [s["type"] for s in slides]
    if got != want:
        sys.exit("X  guard_flow: screen order does not match the SME's finalised deck.\n"
                 "     want: %s\n     got:  %s" % (want, got))
    print("  OK  flow guard: %d screens (landing + %d), the SME's finalised round-3 order"
          % (len(slides) + 1, len(slides)))


def guard_prompts(slides):
    bad = [s["id"] for s in slides if not (s.get("prompt_hi") or "").strip()]
    if bad:
        sys.exit("X  guard_prompts: empty prompt_hi on %s — the heading band would render "
                 "blank beside the mascot" % ", ".join(bad))
    print("   guard_prompts ....... %d/%d slides carry heading text" % (len(slides), len(slides)))


def guard_register(slides):
    """The SME asked for आप twice, in as many words. तुम forms are the single easiest thing to
    leave behind when adapting a तुम lesson, and they are invisible to every other check."""
    TUM = ["करो।", "करो?", "सोचो", "देखो", "सुनो", "डालो", "पहचानो", "चुनो", "पढ़ो", "बोलो",
           "तुम्हारी", "तुम्हें"]
    hits = []
    for vid, text in AUDIO_TEXT.items():
        for t in TUM:
            if t in text:
                hits.append((vid, t))
    for s in slides:
        for t in TUM:
            if t in (s.get("prompt_hi") or ""):
                hits.append((s["id"] + ":prompt_hi", t))
    if hits:
        sys.exit("X  guard_register: तुम forms found, but this lesson is आप throughout: %s"
                 % hits[:8])
    print("  OK  register guard: आप throughout (%d clips + %d headings)"
          % (len(AUDIO_TEXT), len(slides)))


def guard_word_build(slides):
    for s in slides:
        if s["type"] != "WORD_BUILD":
            continue
        d = s["data"]
        for sl in d["slots"]:
            if sl["answer"] + sl["post"] != sl["word"]:
                sys.exit("X  guard_word_build: %r + %r != %r — the completed word would not be\n"
                         "     the word the picture shows"
                         % (sl["answer"], sl["post"], sl["word"]))
            if sl["answer"] not in d["options"]:
                sys.exit("X  guard_word_build: answer %r is not among the options" % sl["answer"])
        extra = [o for o in d["options"] if o not in [x["answer"] for x in d["slots"]]]
        if len(extra) < 1:
            sys.exit("X  guard_word_build: no distractor options — a child could finish by "
                     "elimination without reading")
        print("  OK  word-build guard: %d slots, %d options (%d distractors)"
              % (len(d["slots"]), len(d["options"]), len(extra)))


def guard_sentences(slides):
    for s in slides:
        if s["type"] != "SENTENCE_COMPLETE":
            continue
        d = s["data"]
        words = [o["word"] for o in d["options"]]
        if d["answer"] not in words:
            sys.exit("X  guard_sentences: answer %r not among its own options" % d["answer"])
        if len(set(words)) != len(words):
            sys.exit("X  guard_sentences: duplicate option in %s" % s["id"])
        # every option must be a word the child has actually met in this lesson
        for w in words:
            key_of(w)
    n = sum(1 for s in slides if s["type"] == "SENTENCE_COMPLETE")
    mats = [s["data"]["matra"] for s in slides if s["type"] == "SENTENCE_COMPLETE"]
    print("  OK  sentence guard: %d screens, answers split %d ए / %d ऐ"
          % (n, mats.count(E), mats.count(AI)))


def guard_mechanics(slides):
    # SENTENCE_COMPLETE is DRAG — the SME's note says the card «snaps into the blank space»
    # and on a miss «returns to its original position». Both are drag language.
    fam = {"TRAIN_TAP": "pick", "TRAIN_SORT": "drag", "WORD_BUILD": "drag",
           "SENTENCE_COMPLETE": "drag"}
    tests = [s for s in slides if s["type"] in fam]
    counts = {}
    for s in tests:
        f = fam[s["type"]]
        counts[f] = counts.get(f, 0) + 1
    if len(counts) < 2:
        sys.exit("X  mechanic gate: fewer than 2 gesture families")
    for f, c in counts.items():
        if c / len(tests) > 0.60:
            if not MECHANIC_SKEW_ACCEPTED:
                sys.exit("X  mechanic gate: %s is %d%% of test slides"
                         % (f, round(100 * c / len(tests))))
            print("  !!  MECHANIC SKEW ACCEPTED: %s is %d%% of test slides (gate is 60%%)."
                  % (f, round(100 * c / len(tests))))
            print("      %s" % MECHANIC_SKEW_REASON)
    print("  OK  mechanic gate: %d test slides — %s"
          % (len(tests), " · ".join("%s %d (%d%%)" % (f, c, round(100 * c / len(tests)))
                                    for f, c in sorted(counts.items()))))


def guard_pictures(slides, card):
    declared = set(card["assets"]["image"])
    used = set()
    for s in slides:
        d = s.get("data") or {}
        for k in ("result_img", "scene_img"):
            if d.get(k):
                used.add(d[k])
        for lst in ("examples", "options", "cards", "slots"):
            for it in (d.get(lst) or []):
                if isinstance(it, dict) and it.get("img"):
                    used.add(it["img"])
    missing = used - declared
    if missing:
        sys.exit("X  picture guard: used but not declared: %s" % sorted(missing))
    unused = declared - used
    if unused:
        sys.exit("X  picture guard: declared but never used: %s" % sorted(unused))
    print("  OK  picture guard: %d images, all declared and all used" % len(declared))


def guard_hints(src, slides, card):
    """The hint ladder must exist ONCE, and the idle hint must have a knob that is read.

    Both halves are here because both failed silently. The ladder had been hand-copied into six
    modules and drifted in five: `hint_shown` is in signals_expected but only TRAIN_TAP ever
    emitted it, so the dashboard showed zero hints on 8 of the 11 test screens while the child
    was in fact being helped. And the idle hint reads `idle_hint_ms`, NOT `nudge_timeout_ms` --
    a first cut of makeHints read the latter, fired at 6s and talked straight over the engine's
    own 7s prompt replay ([27f]). Neither fault shows in a screenshot, a click-through or an
    asset check, which is why they have to be build guards.
    """
    if "function makeHints(" not in src:
        sys.exit("X  hint guard: makeHints() is missing from engine_local. Re-run "
                 "engine_local/inject_train.py; do NOT hand-edit the monolith.")
    if "idle_hint_ms" not in src:
        sys.exit("X  hint guard: nothing in the engine reads scaffold_rules.idle_hint_ms.\n"
                 "     The card would declare an idle hint that never fires.")
    if "nudge_timeout_ms" in src[src.index("function makeHints("):]:
        sys.exit("X  hint guard: makeHints reads nudge_timeout_ms. That is the engine's HAND\n"
                 "     timer -- using it for the idle VO fires at 6s, over the engine's own\n"
                 "     7s prompt replay. Use idle_hint_ms.")
    for sig in ("hint_shown", "idle_cue"):
        if ('"%s"' % sig) not in src:
            sys.exit("X  hint guard: the engine never emits %r" % sig)

    # ONE ladder. A module that speaks hint1 itself has forked it again.
    body = src[src.index("function makeHints("):]
    end = body.index("SlideModules.")
    strays = [m.start() for m in re.finditer(r'A\(slide, "hint1"\)', body[end:])]
    if strays:
        sys.exit("X  hint guard: %d module(s) still play hint1 directly instead of going "
                 "through makeHints(). That is exactly how the ladder drifted last time."
                 % len(strays))

    r = card["scaffold_rules"]
    phases = {s["phase"] for s in slides if s["type"] in TEST_TYPES}
    if not r.get("idle_hint_ms"):
        sys.exit("X  hint guard: no idle_hint_ms, so a child who stalls on any of the %d test\n"
                 "     screens would get the prompt once from the engine and nothing after."
                 % len(phases and [x for x in slides if x["type"] in TEST_TYPES]))
    for sig in ("hint_shown", "idle_cue"):
        if sig not in card["signals_expected"]:
            sys.exit("X  hint guard: %r is emitted but not in signals_expected" % sig)
    print("  OK  hint guard: one ladder (makeHints); idle hint %dms after the engine's own"
          % r["idle_hint_ms"])


def guard_audio(slides, card):
    declared = set(card["assets"]["audio"])
    for s in slides:
        for k, v in (s.get("audio") or {}).items():
            if isinstance(v, str) and v not in declared:
                sys.exit("X  audio guard: %s/%s -> %r is not declared" % (s["id"], k, v))
        d = s.get("data") or {}
        for lst in ("examples", "cards", "slots", "options", "pairs"):
            for it in (d.get(lst) or []):
                if isinstance(it, dict):
                    for kk in ("audio", "audio_line", "matra_audio"):
                        if it.get(kk) and it[kk] not in declared:
                            sys.exit("X  audio guard: %s data %s -> %r not declared"
                                     % (s["id"], kk, it[kk]))
        for v in (d.get("option_audio") or {}).values():
            if v not in declared:
                sys.exit("X  audio guard: %s option_audio -> %r not declared" % (s["id"], v))
        if s["type"] in TEST_TYPES:
            for need in ("prompt", "hint1", "hint2", "correct"):
                if not (s.get("audio") or {}).get(need):
                    sys.exit("X  audio guard: test slide %s has no %s clip" % (s["id"], need))
    print("  OK  audio guard: every id declared; every test slide has prompt+hint1+hint2+correct")


# ---------------------------------------------------------------- emit
def main():
    os.makedirs(BUNDLE, exist_ok=True)
    if not os.path.exists(ENGINE):
        sys.exit("X  no engine_local/lesson_template.html — copy it from the sibling and run "
                 "engine_local/inject_train.py first")
    src = open(ENGINE, encoding="utf-8").read()

    ver = guard_engine(src)
    guard_single_matra()
    slides = build_slides()
    guard_flow(slides)
    guard_prompts(slides)
    guard_register(slides)
    guard_word_build(slides)
    guard_sentences(slides)
    guard_mechanics(slides)
    card = build_card(slides)
    guard_pictures(slides, card)
    guard_hints(src, slides, card)
    guard_audio(slides, card)

    # ---- chrome + fixed clips from the sibling (never generated, always copied)
    for sub in ("UI", "Audio", "Images"):
        os.makedirs(os.path.join(BUNDLE, "assets", sub), exist_ok=True)
    ui_src = os.path.join(SIBLING, "assets", "UI")
    n_ui = 0
    if os.path.isdir(ui_src):
        for f in os.listdir(ui_src):
            s_, d_ = os.path.join(ui_src, f), os.path.join(BUNDLE, "assets", "UI", f)
            if os.path.isfile(s_) and not os.path.exists(d_):
                shutil.copy2(s_, d_); n_ui += 1
    n_fix = 0
    for v in COPY_AUDIO:
        s_ = os.path.join(SIBLING, "assets", "Audio", v + ".ogg")
        d_ = os.path.join(BUNDLE, "assets", "Audio", v + ".ogg")
        if os.path.exists(s_) and not os.path.exists(d_):
            shutil.copy2(s_, d_); n_fix += 1
    print("  OK  chrome copied: %d UI files, %d/%d fixed clips" % (n_ui, n_fix, len(COPY_AUDIO)))

    # ---- card.json + injected html
    cj = os.path.join(BUNDLE, "card.json")
    with open(cj, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)

    payload = json.dumps(card, ensure_ascii=False, indent=2)
    if not CARD_TAG.search(src):
        sys.exit("X  no cardData script tag in engine_local")
    out = CARD_TAG.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), src, count=1)
    with open(os.path.join(BUNDLE, CODE + ".html"), "w", encoding="utf-8") as f:
        f.write(out)

    print("  OK  card:   %d slides  %s" % (len(slides), card["phase_distribution"]))
    print("  OK  audio:  %d to record + %d copied" % (len(AUDIO_TEXT), len(COPY_AUDIO)))
    print("  OK  images: %d objects + %d scenes" % (len(OBJ), len(SCENE)))
    print("  OK  html:   %s.html  (engine %s)" % (CODE, ver))


if __name__ == "__main__":
    main()
