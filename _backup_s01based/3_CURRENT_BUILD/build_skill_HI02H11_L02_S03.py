# -*- coding: utf-8 -*-
"""Build HI02H11_L02_S03 — «मात्राओं की रेल» · ए / ऐ.

Skill: "ए, ऐ मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।"  (G2 · HI02H11_L02)

REVISION 2026-10-06 — SME deck `HI02H11_L02_S03_SME_Review.pptx` applied (verbatim notes in
../1_SPEC/_SME_RECOMMENDATIONS.md; row-by-row checklist in CHANGES.md next to this file).

ENGINE: this lesson now runs on the SAME per-game engine as its finished sibling
HI02H11_L02_S01 (the train cover, TrainChrome, the train screens, the Swiftie gate and the
celebration), copied to ../4_ENGINE/lesson_template.html, plus the S03 additions recorded in
../4_ENGINE/CHANGES.md (े/ै in-word highlight, SENTENCE_COMPLETE, अक्षर mode on MATRA_FILL, and
data-flagged ladder tweaks). The draft's injected train_modules.js is retired to
../4_ENGINE/_superseded_draft1/. The guard below checks for the FEATURES, as the sibling's does.

Run:  PYTHONUTF8=1 python build_skill_HI02H11_L02_S03.py
"""
import array, contextlib, json, os, re, sys, wave

HERE   = os.path.dirname(os.path.abspath(__file__))          # .../3_CURRENT_BUILD
ROOT   = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "4_ENGINE", "lesson_template.html")
CODE   = "HI02H11_L02_S03"
OUT    = HERE
_CARD_TAG = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)

E, AI = "े", "ै"

# ---------------------------------------------------------------------------------------------
# ENGINE FEATURE GUARD — refuse to build on a drifted or re-copied engine.
# ---------------------------------------------------------------------------------------------
REQUIRED_FEATURES = [
    ("const TrainChrome",            "TRAIN_CHROME missing — the train screens have no shell"),
    ("SlideModules.MATRA_PAIRS",     "MATRA_PAIRS missing (deck page 2)"),
    ("SlideModules.MATRA_BUILD",     "MATRA_BUILD missing (deck pages 3, 5)"),
    ("SlideModules.MEET_PAIR",       "MEET_PAIR missing (deck pages 4, 6)"),
    ("SlideModules.TRAIN_TAP",       "TRAIN_TAP missing (deck pages 7-9)"),
    ("SlideModules.TRAIN_SORT",      "TRAIN_SORT missing (deck pages 10, 11, 13)"),
    ("SlideModules.MATRA_FILL",      "MATRA_FILL missing (deck page 12, अक्षर mode)"),
    ("SlideModules.SENTENCE_COMPLETE", "SENTENCE_COMPLETE missing (deck pages 14, 16, 17)"),
    ("function hintHold",            "the hint ladder's screen-hold is missing"),
    ("ladder3: { demo: tapDemo",     "TRAIN_TAP is not passing the three-rung ladder"),
    ('const INWORD_MATRAS = new Set(["ा", "ी", "ि", "े", "ै"])',
     "े/ै are not in INWORD_MATRAS — every in-word highlight on this lesson would be blank"),
    ("asc = fontPx * 1.30",          "the in-word raster headroom fix is gone — े/ै tops would be clipped"),
    ("belongs to the bindu",         "the bindu exclusion is gone — भैंस's ं would turn red"),
    ("d.keep_hl",                    "rung-2 'retain the highlights' flag missing"),
    ("d.h2_show_word",               "page 13 rung-2 temporary word support missing"),
    ("d.akshar",                     "MATRA_FILL अक्षर mode missing (page 12)"),
    ("d.base_hl_ms",                 "MATRA_BUILD base-picture highlight missing (pages 3, 5)"),
    ("train_spritesheet.webp",       "the cover is off the spritesheet train"),
    ("window.__landingTrainEnter",   "the cover train entrance is not deferred"),
    ('const VO_DIR  = "assets/Audio/VO/"', "the engine is back on a flat Audio folder"),
    ('const SFX_DIR = "assets/Audio/SFX/"', "the engine is back on a flat Audio folder"),
]


def require_engine():
    if not os.path.exists(ENGINE):
        raise SystemExit(f"  X  ENGINE GUARD: per-game engine missing: {ENGINE}")
    mono = open(ENGINE, encoding="utf-8").read()
    ev = re.search(r'ENGINE_VERSION\s*=\s*["\']([^"\']+)["\']', mono)
    if not ev:
        raise SystemExit("  X  ENGINE GUARD: engine is UNSTAMPED")
    missing = [why for needle, why in REQUIRED_FEATURES if needle not in mono]
    if missing:
        for why in missing:
            print(f"  X  MISSING FEATURE: {why}", file=sys.stderr)
        raise SystemExit("  X  ENGINE GUARD failed — nothing was written.")
    print(f"  OK  engine guard: {ev.group(1)} + all {len(REQUIRED_FEATURES)} required features present")
    return mono


# =============================================================================================
# VOICE-OVER — the SME's own wording from the deck. One systematic substitution, as on S01:
#   em-dash -> comma (an em-dash before a short final word truncates the TTS clip).
# =============================================================================================
VO = {
    # ---- landing (page 1) — same line as S01, so S01's take is reused ------------------------
    "vo_landing": "हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।",

    # ---- page 2 · MATRA_PAIRS -----------------------------------------------------------------
    "vo_s1_prompt": "आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।",
    "vo_pair_e":    "यह है ए। इसकी मात्रा देखिए।",
    "vo_pair_ai":   "यह है ऐ। इसकी मात्रा देखिए।",
    "vo_matra_e":   "ए की मात्रा",
    "vo_matra_ai":  "ऐ की मात्रा",

    # ---- page 3 · MATRA_BUILD सब -> से -> सेब --------------------------------------------------
    "vo_mb_seb_intro":   "आइए, देखें कि ए की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।",
    "vo_mb_seb_base":    "यह शब्द देखिए, सब। ये सब बच्चे हैं।",
    "vo_mb_seb_onset":   "स के साथ ए की मात्रा लगाने पर, से बनता है।",
    "vo_mb_seb_explain": "अब ब जुड़ने पर, सेब बनता है।",
    "vo_mb_seb_sounds":  "स, से, सेब।",

    # ---- page 4 · MEET_PAIR मेज़ / पेड़ ---------------------------------------------------------
    "vo_ex_e_intro": "आइए, ए की मात्रा वाले कुछ शब्द देखें।",
    "vo_ex_mez":     "मेज़, बोलकर देखिए। इसमें म पर ए की मात्रा लगी है।",
    "vo_ex_ped":     "पेड़, बोलकर देखिए। इसमें प पर ए की मात्रा लगी है।",

    # ---- page 5 · MATRA_BUILD पर -> पै -> पैर --------------------------------------------------
    "vo_mb_pair_intro":   "आइए, देखें कि ऐ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।",
    "vo_mb_pair_base":    "यह शब्द देखिए, पर। मेज़ पर किताब रखी है।",
    "vo_mb_pair_onset":   "प के साथ ऐ की मात्रा लगाने पर, पै बनता है।",
    "vo_mb_pair_explain": "अब र जुड़ने पर, पैर बनता है।",
    "vo_mb_pair_sounds":  "प, पै, पैर।",

    # ---- page 6 · MEET_PAIR बैल / भैंस --------------------------------------------------------
    "vo_ex_ai_intro": "आइए, ऐ की मात्रा वाले कुछ शब्द देखें।",
    "vo_ex_bail":     "बैल, बोलकर देखिए। इसमें ब पर ऐ की मात्रा लगी है।",
    "vo_ex_bhains":   "भैंस, बोलकर देखिए। इसमें भ पर ऐ की मात्रा लगी है।",

    # ---- pages 7-9 · TRAIN_TAP ----------------------------------------------------------------
    "vo_tt_e_prompt":   "जिस डिब्बे में “ए” की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।",
    "vo_tt_e_hint1":    "फिर से पढ़िए। ए की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_e_hint2":    "ए की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_e_correct":  "शाबाश! सेब शब्द में ए की मात्रा है।",
    "vo_tt_e_hint3":    "सेब शब्द में ए की मात्रा है। सेब पर टैप कीजिए।",
    "vo_tt_ai_prompt":  "जिस डिब्बे में ऐ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।",
    "vo_tt_ai_hint1":   "फिर से पढ़िए। ऐ की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_ai_hint2":   "ऐ की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_bag_correct": "शाबाश! बैग शब्द में ऐ की मात्रा है।",
    "vo_tt_bag_hint3":   "बैग शब्द में ऐ की मात्रा है। बैग पर टैप कीजिए।",
    "vo_tt_pen_correct": "शाबाश! पैन शब्द में ऐ की मात्रा है।",
    "vo_tt_pen_hint3":   "पैन शब्द में ऐ की मात्रा है। पैन पर टैप कीजिए।",

    # ---- the drag demonstration before the first drag (carried over from S01's flow) ----------
    "vo_ts0_prompt":    "देखिए, शब्द को उसकी सही मात्रा वाले डिब्बे में इस तरह ले जाते हैं।",
    "vo_ts0_ok_pair":   "शाबाश! पैर शब्द में ऐ की मात्रा है।",

    # ---- page 10 · TRAIN_SORT words -> ए / ऐ coach --------------------------------------------
    "vo_ts1_prompt":   "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_hint1":    "फिर से पढ़िए। इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_hint2":    "इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_ok_sher":  "शाबाश! शेर शब्द में ए की मात्रा है।",
    "vo_ts1_ok_ber":   "शाबाश! बेर शब्द में ए की मात्रा है।",
    "vo_ts1_ok_thaila": "शाबाश! थैला शब्द में ऐ की मात्रा है।",
    "vo_ts1_ok_paisa": "शाबाश! पैसा शब्द में ऐ की मात्रा है।",
    "vo_ts1_h3_sher":  "शेर शब्द में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।",
    "vo_ts1_h3_ber":   "बेर शब्द में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।",
    "vo_ts1_h3_thaila": "थैला शब्द में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए।",
    "vo_ts1_h3_paisa": "पैसा शब्द में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए।",

    # ---- page 11 · TRAIN_SORT matra -> letter coach -------------------------------------------
    "vo_ts2_prompt":  "सही मात्रा को सही डिब्बे में डालिए।",
    "vo_ts2_hint1":   "फिर से देखिए। सही मात्रा को सही डिब्बे में डालिए।",
    "vo_ts2_hint2":   "मात्रा का आकार ध्यान से देखिए। इसे सही डिब्बे में डालिए।",
    "vo_ts2_ok_e":    "शाबाश! यह ए की मात्रा है।",
    "vo_ts2_ok_ai":   "शाबाश! यह ऐ की मात्रा है।",
    "vo_ts2_h3_e":    "यह ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।",
    "vo_ts2_h3_ai":   "यह ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए।",

    # ---- page 12 · WORD_BUILD (MATRA_FILL, अक्षर mode) ----------------------------------------
    "vo_wb_prompt":   "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।",
    "vo_wb_hint1":    "फिर से देखिए। चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।",
    "vo_wb_ok_seb":   "शाबाश! सेब बन गया।",
    "vo_wb_ok_pair":  "शाबाश! पैर बन गया।",
    "vo_wb_ok_mez":   "शाबाश! मेज़ बन गई।",
    "vo_wb_h3_seb":   "से लगाने से सेब बनता है। से को खाली जगह में डालिए।",
    "vo_wb_h3_pair":  "पै लगाने से पैर बनता है। पै को खाली जगह में डालिए।",
    "vo_wb_h3_mez":   "मे लगाने से मेज़ बनती है। मे को खाली जगह में डालिए।",
    "vo_ak_se": "से।", "vo_ak_bai": "बै।", "vo_ak_me": "मे।", "vo_ak_be": "बे।", "vo_ak_pai": "पै।",

    # ---- page 13 · TRAIN_SORT pictures only --------------------------------------------------
    "vo_ts3_prompt":  "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_hint2":   "मात्रा देखिए। चित्र को सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_h1_pen":  "फिर से सुनिए। पैन। चित्र को सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_h1_mez":  "फिर से सुनिए। मेज़। चित्र को सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_h1_sher": "फिर से सुनिए। शेर। चित्र को सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_h1_bag":  "फिर से सुनिए। बैग। चित्र को सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_ok_pen":  "शाबाश! पैन में ऐ की मात्रा है।",
    "vo_ts3_ok_mez":  "शाबाश! मेज़ में ए की मात्रा है।",
    "vo_ts3_ok_sher": "शाबाश! शेर में ए की मात्रा है।",
    "vo_ts3_ok_bag":  "शाबाश! बैग में ऐ की मात्रा है।",
    "vo_ts3_h3_pen":  "पैन में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए।",
    "vo_ts3_h3_mez":  "मेज़ में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।",
    "vo_ts3_h3_sher": "शेर में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए।",
    "vo_ts3_h3_bag":  "बैग में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए।",

    # ---- pages 17 / 14 / 16 · SENTENCE_COMPLETE ----------------------------------------------
    "vo_sc_prompt":   "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए। शब्द को खाली जगह में डालिए।",
    "vo_sc_hint1":    "फिर से देखिए। चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।",
    "vo_sc_hint2":    "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।",
    # पैन — मैं ___ से लिखता हूँ।
    "vo_sc_pen_sent":    "मैं ... से लिखता हूँ।",
    "vo_sc_pen_correct": "शाबाश! मैं पैन से लिखता हूँ।",
    "vo_sc_pen_hint3":   "चित्र में बच्चा पैन से लिख रहा है। पैन को खाली जगह में डालिए।",
    "vo_sc_pen_s_pen":   "मैं पैन से लिखता हूँ।",
    "vo_sc_pen_s_ped":   "मैं पेड़ से लिखता हूँ।",
    "vo_sc_pen_s_bail":  "मैं बैल से लिखता हूँ।",
    # पेड़ — बगीचे में एक बड़ा ___ है।
    "vo_sc_ped_sent":    "बगीचे में एक बड़ा ... है।",
    "vo_sc_ped_correct": "शाबाश! बगीचे में एक बड़ा पेड़ है।",
    "vo_sc_ped_hint3":   "चित्र में बगीचे में एक बड़ा पेड़ है। पेड़ को खाली जगह में डालिए।",
    "vo_sc_ped_s_ped":   "बगीचे में एक बड़ा पेड़ है।",
    "vo_sc_ped_s_bail":  "बगीचे में एक बड़ा बैल है।",
    "vo_sc_ped_s_pen":   "बगीचे में एक बड़ा पैन है।",
    # सेब — मुझे ___ खाना अच्छा लगता है।
    "vo_sc_seb_sent":    "मुझे ... खाना अच्छा लगता है।",
    "vo_sc_seb_correct": "शाबाश! मुझे सेब खाना अच्छा लगता है।",
    "vo_sc_seb_hint3":   "चित्र में बच्चा सेब खा रहा है। सेब को खाली जगह में डालिए।",
    "vo_sc_seb_s_seb":   "मुझे सेब खाना अच्छा लगता है।",
    "vo_sc_seb_s_bag":   "मुझे बैग खाना अच्छा लगता है।",
    "vo_sc_seb_s_mez":   "मुझे मेज़ खाना अच्छा लगता है।",

    # ---- word names ---------------------------------------------------------------------------
    "vo_name_seb": "सेब।", "vo_name_pair": "पैर।", "vo_name_bail": "बैल।",
    "vo_name_ped": "पेड़।", "vo_name_rail": "रेल।", "vo_name_bag": "बैग।",
    "vo_name_mez": "मेज़।", "vo_name_pen": "पैन।",
    "vo_name_sher": "शेर।", "vo_name_ber": "बेर।", "vo_name_thaila": "थैला।", "vo_name_paisa": "पैसा।",

    # ---- celebration (page 18 · N/C — the draft's line kept) ----------------------------------
    "vo_cel_prompt": "शाबाश! आज हमने सीखा, ए और ऐ की मात्रा पहचानना, और मात्रा वाले शब्द पढ़ना।",

    # ---- phase gates (S01's takes, identical text) -------------------------------------------
    "vo_pt_tutorial": "ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!",
    "vo_pt_guided":   "बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!",
    "vo_pt_practice": "वाह! अब आपकी बारी।",
    "sfx_celebrate":  "celebration sound",
}

# clips whose text is IDENTICAL to a take in the finished sibling S01 (same voice, Kore) — copied
# from there instead of re-synthesised, so the shared lines sound the same across the two lessons
FROM_S01 = {"vo_landing", "vo_ts0_prompt", "vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice"}

IMAGES = {
    "obj_seb": "🍎", "obj_ped": "🌳", "obj_mez": "🪑", "obj_pair": "🦶", "obj_bail": "🐂",
    "obj_bag": "🎒", "obj_pen": "🖊️", "obj_sab": "🧒", "obj_par": "📘", "obj_bhains": "🐃",
    "obj_sher": "🦁", "obj_ber": "🫒", "obj_thaila": "👜", "obj_paisa": "🪙",
    "scn_bageecha": "🌳", "scn_likhna": "🖊️", "scn_seb_khana": "🍎",
}


# =============================================================================================
# CLIP MEASUREMENT — ported unchanged from S01's builder (karaoke pauses + beat cues).
# =============================================================================================
SPEECH_NOISE_DB = -38.0
SPEECH_MIN_SIL  = 0.10
SPEECH_FRAME    = 0.010


def _clip_pcm(path, rate=16000):
    import subprocess
    try:
        out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-acodec", "pcm_s16le",
                              "-ac", "1", "-ar", str(rate), "-"], capture_output=True, timeout=60)
        if out.returncode != 0 or not out.stdout:
            return None, 0
        a = array.array("h"); a.frombytes(out.stdout[: len(out.stdout) // 2 * 2])
        return a, rate
    except Exception:
        return None, 0


def _speech_segments(path):
    import math
    a, rate = _clip_pcm(path)
    if not a or not rate:
        return None, 0.0
    fl = max(1, int(rate * SPEECH_FRAME))
    thr = (10.0 ** (SPEECH_NOISE_DB / 20.0)) * 32768.0
    loud = []
    for i in range(0, len(a) - fl + 1, fl):
        acc = 0
        for v in a[i:i + fl]:
            acc += v * v
        loud.append(math.sqrt(acc / fl) >= thr)
    dur = len(a) / float(rate)
    need = int(round(SPEECH_MIN_SIL / SPEECH_FRAME))
    segs, i, n = [], 0, len(loud)
    while i < n:
        if not loud[i]:
            i += 1; continue
        j = i
        while j < n:
            if loud[j]:
                j += 1; continue
            k = j
            while k < n and not loud[k]:
                k += 1
            if (k - j) < need and k < n:
                j = k; continue
            break
        segs.append([round(i * SPEECH_FRAME, 3), round(min(dur, j * SPEECH_FRAME), 3)])
        i = j
    return (segs or None), round(dur, 3)


def _measure_speech(audio_ids):
    speech, durs = {}, {}
    for aid in sorted(audio_ids):
        p = os.path.join(OUT, "assets", "Audio", "SFX" if aid.startswith("sfx_") else "VO", aid + ".ogg")
        if not os.path.exists(p):
            continue
        segs, dur = _speech_segments(p)
        if dur:
            durs[aid] = dur
        if not segs:
            continue
        if len(segs) == 1 and sum(e - s for s, e in segs) >= 0.95 * dur:
            continue
        speech[aid] = segs
    return speech, durs


def _cue_ms(audio_id, phrase):
    """When, inside the recording of VO[audio_id], `phrase` starts — real duration x text share."""
    line = VO[audio_id]
    path = os.path.join(OUT, "assets", "Audio", "VO", audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            secs = w.getnframes() / float(w.getframerate())
    except Exception:
        return 1300
    i = line.find(phrase)
    if i < 0:
        return int(secs * 1000 * 0.35)
    before = len(line[:i].replace(" ", "")); total = len(line.replace(" ", "")) or 1
    return int(secs * 1000 * (before / float(total)))


def _sound_cues_ms(audio_id, n=3):
    path = os.path.join(OUT, "assets", "Audio", "VO", audio_id + ".ogg")
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
    hop = max(1, int(sr * 0.01)); peak = max(1, max(abs(v) for v in a))
    loud = [max(abs(v) for v in a[i:i + hop]) > peak * 0.10 for i in range(0, len(a) - hop, hop)]
    runs, i, minq = [], 0, int(0.14 / 0.01)
    while i < len(loud):
        if loud[i]:
            j, q = i, 0
            while j < len(loud):
                if loud[j]: q = 0
                else:
                    q += 1
                    if q >= minq: break
                j += 1
            runs.append(i); i = j
        i += 1
    return [int(r * 10) for r in runs] if len(runs) == n else None


def A(**kw):
    return dict(kw)


# =============================================================================================
# SCREENS — final deck order: 1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · 11 · 12 · 13 · 17 · 14 · 16 · 18
# (page 15 «मेरे ___ में दर्द है।» was DELETED by the SME and is not built)
# =============================================================================================
def build_screen(sid, base, base_img, cons, matra, syl, result, result_img, key, base_hl_phrase,
                 outline=False):
    return {
        "id": sid, "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",    # deck: "Keep the screen clean. Avoid unnecessary explanatory text"
        "audio": A(prompt=f"vo_mb_{key}_intro", base=f"vo_mb_{key}_base", onset=f"vo_mb_{key}_onset",
                   result=f"vo_mb_{key}_explain", sounds=f"vo_mb_{key}_sounds",
                   explain=f"vo_mb_{key}_explain"),
        "data": {"auto": True, "no_heading": True,
                 "base_word": base, "base_img": base_img, "base_emoji": IMAGES[base_img],
                 "base_outline": outline,
                 "base_hl_ms": _cue_ms(f"vo_mb_{key}_base", base_hl_phrase),
                 "consonant": cons, "matra": matra, "syllable": syl,
                 "result_word": result, "result_img": result_img, "result_emoji": IMAGES[result_img],
                 "travel": "down",
                 "syl_ms":   _cue_ms(f"vo_mb_{key}_onset", "बनता"),
                 "join_ms":  _cue_ms(f"vo_mb_{key}_explain", result),
                 "sound_ms": _sound_cues_ms(f"vo_mb_{key}_sounds", 3)},
    }


def meet_screen(sid, head, intro, exs):
    out = []
    for word, matra, img, vid in exs:
        out.append({"word": word, "matra": matra, "img": img, "emoji": IMAGES[img],
                    "audio_line": vid, "matra_audio": None,
                    "pic_ms": _cue_ms(vid, "बोलकर"), "matra_ms": _cue_ms(vid, "इसमें")})
    return {"id": sid, "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
            "prompt_hi": head,                      # deck: "Keep the heading"
            "audio": A(prompt=intro), "data": {"auto": True, "examples": out}}


def tap_screen(sid, mname, words, target, prompt, hint1, hint2, correct, hint3):
    M = {"सेब": E, "पैर": AI, "बैल": AI, "पेड़": E, "रेल": E, "बैग": AI, "मेज़": E, "पैन": AI}
    N = {"सेब": "seb", "पैर": "pair", "बैल": "bail", "पेड़": "ped", "रेल": "rail", "बैग": "bag",
         "मेज़": "mez", "पैन": "pen"}
    return {"id": sid, "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
            "prompt_hi": "“%s” की मात्रा वाले शब्द पर टैप कीजिए।" % mname,
            "audio": A(prompt=prompt, correct=correct, hint1=hint1, hint2=hint2, hint3=hint3,
                       try_again=hint1),
            "data": {"signal": "matra_tap_first_try", "keep_hl": True, "hl_on_correct": True,
                     "options": [dict({"word_hi": w, "matra": M[w], "audio": "vo_name_" + N[w]},
                                      **({"correct": True} if w == target else {})) for w in words]},
            "signals": {"on_complete": ["matra_tap_first_try"]}}


BINS = [{"key": "e", "label": "ए"}, {"key": "ai", "label": "ऐ"}]   # deck: "Use only ए and ऐ as the coach labels"


def sentence_screen(sid, key, pre, post, answer, scene, options, focus):
    N = {"पेड़": ("ped", "obj_ped"), "बैल": ("bail", "obj_bail"), "पैन": ("pen", "obj_pen"),
         "सेब": ("seb", "obj_seb"), "बैग": ("bag", "obj_bag"), "मेज़": ("mez", "obj_mez")}
    M = {"पेड़": E, "पैन": AI, "सेब": E}
    return {"id": sid, "phase": "practice", "eis": "symbolic", "type": "SENTENCE_COMPLETE",
            "prompt_hi": "सही शब्द चुनकर वाक्य पूरा कीजिए।",
            "audio": A(prompt="vo_sc_prompt", sentence=f"vo_sc_{key}_sent", correct=f"vo_sc_{key}_correct",
                       hint1="vo_sc_hint1", hint2="vo_sc_hint2", hint3=f"vo_sc_{key}_hint3",
                       try_again="vo_sc_hint1"),
            "data": {"signal": "sentence_complete", "scene_img": scene, "scene_emoji": IMAGES[scene],
                     "sentence_pre": pre, "sentence_post": post, "answer": answer, "matra": M[answer],
                     "focus": focus, "h3_hand": False,
                     "options": [{"word": w, "img": N[w][1], "emoji": IMAGES[N[w][1]],
                                  "audio": "vo_name_" + N[w][0],
                                  "sent_audio": f"vo_sc_{key}_s_{N[w][0]}"} for w in options]},
            "signals": {"on_complete": ["sentence_complete"]}}


def slides():
    S = []
    # ============ TUTORIAL · 5 =================================================================
    S.append({"id": "T1", "phase": "tutorial", "eis": "enactive", "type": "MATRA_PAIRS",
              "prompt_hi": "आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।",   # deck: "Keep the heading"
              "audio": A(prompt="vo_s1_prompt"),
              "data": {"auto": True, "pairs": [
                  {"letter": "ए", "matra": E, "audio": "vo_pair_e", "cue_ms": _cue_ms("vo_pair_e", "इसकी")},
                  {"letter": "ऐ", "matra": AI, "audio": "vo_pair_ai", "cue_ms": _cue_ms("vo_pair_ai", "इसकी")}],
                  "phonemes": {E: "vo_matra_e", AI: "vo_matra_ai"}}})
    S.append(build_screen("T2", "सब", "obj_sab", "स", E, "से", "सेब", "obj_seb", "seb", "ये", outline=True))
    S.append(meet_screen("T3", "ए की मात्रा वाले शब्द पढ़िए।", "vo_ex_e_intro",
                         [("मेज़", E, "obj_mez", "vo_ex_mez"), ("पेड़", E, "obj_ped", "vo_ex_ped")]))
    S.append(build_screen("T4", "पर", "obj_par", "प", AI, "पै", "पैर", "obj_pair", "pair", "मेज़"))
    S.append(meet_screen("T5", "ऐ की मात्रा वाले शब्द पढ़िए।", "vo_ex_ai_intro",
                         [("बैल", AI, "obj_bail", "vo_ex_bail"), ("भैंस", AI, "obj_bhains", "vo_ex_bhains")]))

    # ============ GUIDED · 6 ===================================================================
    S.append(tap_screen("G1", "ए", ["सेब", "पैर", "बैल"], "सेब", "vo_tt_e_prompt", "vo_tt_e_hint1",
                        "vo_tt_e_hint2", "vo_tt_e_correct", "vo_tt_e_hint3"))
    S.append(tap_screen("G2", "ऐ", ["पेड़", "रेल", "बैग"], "बैग", "vo_tt_ai_prompt", "vo_tt_ai_hint1",
                        "vo_tt_ai_hint2", "vo_tt_bag_correct", "vo_tt_bag_hint3"))
    S.append(tap_screen("G3", "ऐ", ["मेज़", "पैन", "सेब"], "पैन", "vo_tt_ai_prompt", "vo_tt_ai_hint1",
                        "vo_tt_ai_hint2", "vo_tt_pen_correct", "vo_tt_pen_hint3"))
    # S01's watch-only drag demonstration, kept in the same place in the flow (before the first drag)
    S.append({"id": "G4D", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
              "prompt_hi": "देखिए, शब्द को उसकी सही मात्रा वाले डिब्बे में इस तरह ले जाते हैं।",
              "audio": A(prompt="vo_ts0_prompt"),
              "data": {"demo": True, "bins": BINS, "items": [
                  {"key": "e", "word_hi": "सेब", "img": "obj_seb", "emoji": IMAGES["obj_seb"],
                   "audio": "vo_name_seb", "correct_audio": "vo_tt_e_correct"},
                  {"key": "ai", "word_hi": "पैर", "img": "obj_pair", "emoji": IMAGES["obj_pair"],
                   "audio": "vo_name_pair", "correct_audio": "vo_ts0_ok_pair"}]},
              "signals": {"on_complete": []}})
    words10 = [("शेर", "e", "sher", E), ("बेर", "e", "ber", E), ("थैला", "ai", "thaila", AI), ("पैसा", "ai", "paisa", AI)]
    S.append({"id": "G4", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
              "prompt_hi": "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
              "audio": A(prompt="vo_ts1_prompt", hint1="vo_ts1_hint1", hint2="vo_ts1_hint2",
                         try_again="vo_ts1_hint1"),
              "data": {"signal": "matra_sort_correct", "multi": True, "announce_items": True,
                       "keep_hl": True, "hl_on_correct": True, "h3_freeze": True, "bins": BINS,
                       "items": [{"key": k, "word_hi": w, "img": "obj_" + n, "emoji": IMAGES["obj_" + n],
                                  "matra": m, "audio": "vo_name_" + n, "correct_audio": "vo_ts1_ok_" + n,
                                  "hint3_audio": "vo_ts1_h3_" + n} for w, k, n, m in words10]},
              "signals": {"on_complete": ["matra_sort_correct"]}})
    S.append({"id": "G5", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
              "prompt_hi": "सही मात्रा को सही डिब्बे में डालिए।",
              "audio": A(prompt="vo_ts2_prompt", hint1="vo_ts2_hint1", hint2="vo_ts2_hint2",
                         try_again="vo_ts2_hint1"),
              # no `audio` on the cards: "Do not announce the matra's name on initial pick-up"
              "data": {"signal": "matra_sort_correct", "hl_on_correct": True, "h2_enlarge": True,
                       "h2_silent_name": True, "h3_freeze": True, "bins": BINS,
                       "items": [{"key": "e", "glyph": E, "matra": E, "correct_audio": "vo_ts2_ok_e",
                                  "hint3_audio": "vo_ts2_h3_e"},
                                 {"key": "ai", "glyph": AI, "matra": AI, "correct_audio": "vo_ts2_ok_ai",
                                  "hint3_audio": "vo_ts2_h3_ai"}]},
              "signals": {"on_complete": ["matra_sort_correct"]}})

    # ============ PRACTICE · 5 =================================================================
    opts = ["से", "बै", "मे", "बे", "पै"]
    S.append({"id": "P1", "phase": "practice", "eis": "enactive", "type": "MATRA_FILL",
              "prompt_hi": "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।",
              "audio": A(prompt="vo_wb_prompt", hint1="vo_wb_hint1", hint2="vo_wb_prompt",
                         try_again="vo_wb_hint1"),
              "data": {"signal": "word_build_correct", "akshar": True, "h3_hand": False,
                       "options": opts,
                       "option_audio": {"से": "vo_ak_se", "बै": "vo_ak_bai", "मे": "vo_ak_me",
                                        "बे": "vo_ak_be", "पै": "vo_ak_pai"},
                       "option_matra": {"से": E, "बै": AI, "मे": E, "बे": E, "पै": AI},
                       "slots": [
                           {"word": "सेब", "parts": ["ब"], "blank_at": 0, "key": "से", "matra": E,
                            "img": "obj_seb", "emoji": IMAGES["obj_seb"], "audio": "vo_name_seb",
                            "correct_audio": "vo_wb_ok_seb", "hint3_audio": "vo_wb_h3_seb"},
                           {"word": "पैर", "parts": ["र"], "blank_at": 0, "key": "पै", "matra": AI,
                            "img": "obj_pair", "emoji": IMAGES["obj_pair"], "audio": "vo_name_pair",
                            "correct_audio": "vo_wb_ok_pair", "hint3_audio": "vo_wb_h3_pair"},
                           {"word": "मेज़", "parts": ["ज़"], "blank_at": 0, "key": "मे", "matra": E,
                            "img": "obj_mez", "emoji": IMAGES["obj_mez"], "audio": "vo_name_mez",
                            "correct_audio": "vo_wb_ok_mez", "hint3_audio": "vo_wb_h3_mez"}]},
              "signals": {"on_complete": ["word_build_correct"]}})
    pics = [("पैन", "ai", "pen", AI), ("मेज़", "e", "mez", E), ("शेर", "e", "sher", E), ("बैग", "ai", "bag", AI)]
    S.append({"id": "P2", "phase": "practice", "eis": "enactive", "type": "TRAIN_SORT",
              "prompt_hi": "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
              "audio": A(prompt="vo_ts3_prompt", hint2="vo_ts3_hint2"),
              "data": {"signal": "matra_sort_correct", "hide_labels": True, "multi": True,
                       "announce_items": True, "h2_show_word": True, "keep_hl": True,
                       "h3_freeze": True, "h3_hand": False, "bins": BINS,
                       "items": [{"key": k, "word_hi": w, "img": "obj_" + n, "emoji": IMAGES["obj_" + n],
                                  "matra": m, "audio": "vo_name_" + n, "correct_audio": "vo_ts3_ok_" + n,
                                  "hint1_audio": "vo_ts3_h1_" + n, "hint3_audio": "vo_ts3_h3_" + n}
                                 for w, k, n, m in pics]},
              "signals": {"on_complete": ["matra_sort_correct"]}})
    # deck order after the SME's reorder: page 17 (पैन) · page 14 (पेड़) · page 16 (सेब)
    S.append(sentence_screen("P3", "pen", "मैं", "से लिखता हूँ।", "पैन", "scn_likhna",
                             ["पैन", "पेड़", "बैल"], {"x": 34, "y": 34, "w": 15, "h": 18}))
    S.append(sentence_screen("P4", "ped", "बगीचे में एक बड़ा", "है।", "पेड़", "scn_bageecha",
                             ["पेड़", "बैल", "पैन"], {"x": 20, "y": 12, "w": 60, "h": 70}))
    S.append(sentence_screen("P5", "seb", "मुझे", "खाना अच्छा लगता है।", "सेब", "scn_seb_khana",
                             ["सेब", "बैग", "मेज़"], {"x": 51, "y": 40, "w": 16, "h": 17}))
    S.append({"id": "CEL", "phase": "practice", "eis": "enactive", "type": "CELEBRATION",
              "prompt_hi": VO["vo_cel_prompt"],
              "audio": A(prompt="vo_cel_prompt", sfx="sfx_celebrate"), "data": {}})
    return S


def card(slides_):
    counts = {}
    for s in slides_:                     # the celebration counts too: sum == #slides (receipt)
        counts[s["phase"]] = counts.get(s["phase"], 0) + 1
    return {
        "version": "0.3", "skill_code": CODE, "lo_code": "HI02H11_L02", "grade": "02",
        "attribute": "H11", "skill_type": "CORE", "part_label": "", "medium": "hi",
        "title": {"hi": "मात्राओं की रेल", "en": "The matra train — ए / ऐ"},
        "subtitle_hi": "",
        "theme": "toybox",
        "skill_description_hi": "ए, ऐ मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।",
        "landing_audio": "vo_landing",
        # deck page 1: "Show only two matra boxes ... 1st box: ‘ए’(◌े) · 2nd box: ‘ऐ’(◌ै)" in train bogies
        "landing_hero": {"kind": "matra_train", "matras": [E, AI], "letters": ["“ए”", "“ऐ”"]},
        "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                                   "practice": "vo_pt_practice"},
        "phase_transition_title": {"tutorial": "चलिए, रेल चलाएँ!", "guided": "साथ में करते हैं।",
                                   "practice": "अब आपकी बारी।"},
        "phase_distribution": counts,
        "scaffold_rules": {"nudge_timeout_ms": {"guided": 6000, "practice": 8000},
                           "max_attempts": 3, "hand_on_attempt": 2, "hint_levels": 3,
                           "hand_on_hint3": True, "silent_on_late_correct": True,
                           "hand_in_practice": True},
        "signals_expected": ["slide_entered", "slide_completed", "matra_tap_first_try",
                             "matra_sort_correct", "word_build_correct", "sentence_complete",
                             "lesson_completed", "mastery_score"],
        "_emoji_fallback": dict(IMAGES),
        "slides": slides_,
    }


def gate_spec():
    peek = os.path.join(OUT, "assets", "UI", "gate_peek.webp")
    if not os.path.isfile(peek):
        return None
    try:
        from PIL import Image, ImageSequence
        ms = sum((f.info.get("duration") or 40) for f in ImageSequence.Iterator(Image.open(peek)))
    except Exception:
        ms = 1520
    return {"img": "assets/UI/gate_peek.webp", "peek": "assets/UI/gate_peek.webp",
            "talk": "assets/UI/gate_talk.webp", "rest": "assets/UI/gate_rest.webp",
            "peek_ms": ms, "hold_ms": 450}


def cel_anim():
    """S01's lip-sync track generator, re-measured on THIS lesson's celebration line."""
    meta_p = os.path.join(OUT, "_cel_sprite.json")
    clip = os.path.join(OUT, "assets", "Audio", "VO", "vo_cel_prompt.ogg")
    if not (os.path.isfile(meta_p) and os.path.isfile(clip)):
        return None
    import math
    meta = json.load(open(meta_p, encoding="utf-8"))
    a, _ = _clip_pcm(clip)
    if not a:
        return None
    step = 400
    rms = [math.sqrt(sum(x * x for x in a[i:i + step]) / step) for i in range(0, len(a) - step, step)]
    if not rms:
        return None
    W = 4
    t = "".join("1" if (r > 0.10 * max(rms) and r >= 0.62 * max(rms[max(0, i - W):i + W + 1])) else "0"
                for i, r in enumerate(rms))
    t = t.replace("101", "111").replace("101", "111").replace("010", "000")
    sh = meta["sheets"]
    return {"cols": meta["cols"], "fw": meta["fw"], "fh": meta["fh"], "step_ms": 25, "bits": t,
            "vo": "vo_cel_prompt",
            "shabaash": {"src": sh["shabaash"]["src"], "pre": list(range(0, 6)),
                         "word": list(range(6, 30)), "post": list(range(30, 36))},
            "talk": {"src": sh["talk"]["src"], "open": sh["talk"]["open"]},
            "idle": {"src": sh["idle"]["src"], "loop": [0, 1, 2, 3, 4] + list(range(24, 36))}}


AUDIO_KEYS = ("audio", "correct_audio", "prompt", "base", "onset", "result", "explain", "sounds",
              "hint1", "hint2", "hint3", "hint", "hint2_audio", "hint3_audio", "hint1_audio",
              "label_audio", "audio_line", "matra_audio", "try_again", "correct", "reveal", "sfx",
              "sentence", "sent_audio")


def main():
    mono = require_engine()
    S = slides()
    C = card(S)

    used = set()
    def walk(o):
        if isinstance(o, list):
            for x in o: walk(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and k in AUDIO_KEYS and re.fullmatch(r"(vo|sfx)_\w+", v):
                    used.add(v)
                elif k in ("phonemes", "option_audio") and isinstance(v, dict):
                    used.update(v.values())
                else:
                    walk(v)
    walk(S)
    used.add(C["landing_audio"]); used.update(C["phase_transition_audio"].values())
    unknown = sorted(used - set(VO))
    if unknown:
        raise SystemExit(f"  X  slides reference audio ids with no text authored: {unknown}")
    # nothing on screen may say छोटी/बड़ी — deck pages 2, 3, 5
    bad = [k for k in used if "छोटी" in VO[k] or "बड़ी" in VO[k]]
    if bad:
        raise SystemExit(f"  X  छोटी/बड़ी found in: {bad}")

    def audio_path(k):
        return f"assets/Audio/{'SFX' if k.startswith('sfx_') else 'VO'}/{k}.ogg"
    C["assets"] = {"audio": {k: audio_path(k) for k in sorted(used)},
                   "audio_text": {k: VO[k] for k in sorted(used)},
                   "image": {k: f"assets/Images/{k}.png" for k in sorted(IMAGES)},
                   "audio_ext": "ogg", "img_ext": "png"}
    g = gate_spec()
    if g: C["gate"] = g
    ce = cel_anim()
    if ce: C["end_anim"] = ce
    sp, du = _measure_speech(used)
    if sp: C["assets"]["audio_speech"] = sp
    if du: C["assets"]["audio_dur"] = du

    cj = json.dumps(C, ensure_ascii=False).replace("</script>", "<\\/script>")
    html, n = _CARD_TAG.subn(lambda m: m.group(1) + "\n" + cj + "\n" + m.group(3), mono, count=1)
    if n != 1:
        raise SystemExit("  X  cardData tag not found in the engine")
    first, seen = [], set()
    def wi(o):
        if isinstance(o, list):
            for x in o: wi(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and k in ("img", "base_img", "result_img") and v not in seen:
                    seen.add(v); first.append(v)
                else: wi(v)
    wi(S[:3])
    on_disk = [k for k in first if os.path.exists(os.path.join(OUT, "assets", "Images", k + ".png"))]
    html = html.replace("</head>", "".join(f'<link rel="preload" as="image" fetchpriority="high" '
                                           f'href="assets/Images/{k}.png">' for k in on_disk) + "</head>", 1)
    with open(os.path.join(OUT, f"{CODE}.html"), "w", encoding="utf-8", newline="") as f:
        f.write(html)
    with open(os.path.join(OUT, "card.json"), "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(C, ensure_ascii=False, indent=2))

    miss_a = [k for k in sorted(used) if not os.path.exists(os.path.join(OUT, audio_path(k)))]
    miss_i = [k for k in sorted(IMAGES) if not os.path.exists(os.path.join(OUT, "assets", "Images", k + ".png"))]
    print(f"  Built {CODE}: {len(S)} slides · {len(used)} audio ids · {len(IMAGES)} images · "
          f"phases {C['phase_distribution']}")
    print(f"  types: {[s['type'] for s in S]}")
    print(f"  PENDING VO  ({len(miss_a)}): {', '.join(miss_a) or 'none'}")
    print(f"  PENDING ART ({len(miss_i)}): {', '.join(miss_i) or 'none'}")
    print(f"  gate: {'yes' if g else 'stock'} · celebration lip-sync: {'yes' if ce else 'stock'} · "
          f"clips measured: {len(du)}")


if __name__ == "__main__":
    main()
