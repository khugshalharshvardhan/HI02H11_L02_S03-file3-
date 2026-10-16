# -*- coding: utf-8 -*-
"""One-shot: turn S02's builder (copied alongside) into S03's. Logic, guards, flow and every engine
hook stay S02's; only the CONTENT changes (words, pictures, scenes, Hindi lines) — taken from the S03
SME deck (1_SPEC/_SME_RECOMMENDATIONS.md). Kept in the folder so the conversion is reviewable."""
import re, io

P = "build_skill_HI02H11_L02_S03.py"
s = io.open(P, encoding="utf-8").read()


def between(start, end, new):
    """replace s[start_marker : end_marker) with `new` (end marker kept)"""
    global s
    i = s.index(start); j = s.index(end, i)
    s = s[:i] + new + s[j:]


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)


# ---- header ----------------------------------------------------------------------------------
rep('"""Build HI02H11_L02_S02 (भाग 1, उ / ऊ) — «मात्राओं की रेल», the SME\'s train flow.',
    '"""Build HI02H11_L02_S03 (ए / ऐ) — «मात्राओं की रेल».\n\n'
    '[S03 · 2026-10-16] THIS FILE IS HI02H11_L02_S02\'s BUILDER (github CodeWithPiyush0/\n'
    'HI02H11_L02_S02_DEV_HANDOFF @ 992e684) WITH THE S03 CONTENT SWAPPED IN. The flow, the screen\n'
    'logic, the guards, the gate / celebration / runner wiring are S02\'s, unchanged, as asked: "make my\n'
    'file look exactly similar and functional with the logics of that file". The words, pictures and\n'
    'Hindi lines are the S03 SME deck\'s. The S02 notes below are kept for the reasoning behind each rule.\n'
    'Converted by 1_SPEC/_make_s03_builder.py.\n')
rep('CODE     = "HI02H11_L02_S02"', 'CODE     = "HI02H11_L02_S03"')
rep('U, UU = "ु", "ू"',
    '# [S03] the two slots keep S02\'s names so every rule below reads unchanged: U is ए\'s matra, UU ऐ\'s\n'
    'U, UU = "े", "ै"')

# ---- content tables --------------------------------------------------------------------------
between("OBJ = {", "# Full illustrated SCENES", '''OBJ = {
    "obj_seb":    ("सेब",  "\\U0001F34E", U),
    "obj_ped":    ("पेड़",  "\\U0001F333", U),
    "obj_mez":    ("मेज़",  "\\U0001FA91", U),
    "obj_sher":   ("शेर",  "\\U0001F981", U),
    "obj_ber":    ("बेर",  "\\U0001FAD2", U),
    "obj_rail":   ("रेल",  "\\U0001F682", U),     # page 8 lists it (word only, no picture shown)
    "obj_pair":   ("पैर",  "\\U0001F9B6", UU),
    "obj_bail":   ("बैल",  "\\U0001F402", UU),
    "obj_bag":    ("बैग",  "\\U0001F392", UU),
    "obj_pen":    ("पैन",  "\\U0001F58A", UU),
    "obj_bhains": ("भैंस", "\\U0001F403", UU),
    "obj_thaila": ("थैला", "\\U0001F45C", UU),    # carries ा too - the SME: keep ा navy, compare े/ै
    "obj_paisa":  ("पैसा", "\\U0001FA99", UU),
}

''')
between("SCENE = {", "MATRA_VO   =", '''SCENE = {
    "scn_likhna":    "\\U0001F58A",
    "scn_bageecha":  "\\U0001F333",
    "scn_seb_khana": "\\U0001F34E",
}

''')
between("MATRA_VO   =", "AUDIO_TEXT = {}", '''MATRA_VO   = {U: "vo_matra_e", UU: "vo_matra_ai"}
LETTER_VO  = {U: "vo_letter_e", UU: "vo_letter_ai"}
LETTER_TEXT = {"vo_letter_e": "ए", "vo_letter_ai": "ऐ"}
# rung-2 scene glow, as fractions of the artwork (cx, cy, rx, ry) - read off the shipped 1024² scenes
SCENE_GLOW = {
    "scn_likhna":    [[0.410, 0.430, 0.075, 0.090]],   # the pen in his writing hand
    "scn_bageecha":  [[0.500, 0.450, 0.300, 0.370]],   # the big tree, trunk and canopy
    "scn_seb_khana": [[0.590, 0.480, 0.085, 0.090]],   # the apple at his mouth
}
MATRA_TEXT = {"vo_matra_e": "ए की मात्रा", "vo_matra_ai": "ऐ की मात्रा"}
MATRA_TEXT.update(LETTER_TEXT)
MATRA_NAME = {U: "ए", UU: "ऐ"}      # the deck: «ए की मात्रा» / «ऐ की मात्रा», never छोटी / बड़ी
LETTER     = {U: "ए", UU: "ऐ"}

''')
between("BASE_OBJ = {", "def key_of_opt", '''BASE_OBJ = {
    "सब": ("obj_sab", "🧒"),   # three children in one soft outline (page 3)
    "पर": ("obj_par", "📘"),   # a book resting on a table (page 5)
}


''')

# ---- screens -------------------------------------------------------------------------------
rep('''    p = "आज हम छोटी उ और बड़ी ऊ की मात्रा वाले शब्द पढ़ेंगे।"
    heading = "आज हम उ और ऊ की मात्रा वाले शब्द पढ़ेंगे।"''',
    '''    p = "आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।"
    heading = p''')
rep('''    _u_line  = "यह है उ। इसकी मात्रा है — ु।"
    _uu_line = "यह है ऊ। इसकी मात्रा है — ू।"''',
    '''    _u_line  = "यह है ए। इसकी मात्रा देखिए।"      # [S03] the deck's page-2 lines
    _uu_line = "यह है ऐ। इसकी मात्रा देखिए।"''')
rep('''    pairs = [_pair("उ", U, "vo_pair_u", _u_line),
             _pair("ऊ", UU, "vo_pair_uu", _uu_line)]''',
    '''    pairs = [_pair("ए", U, "vo_pair_e", _u_line),
             _pair("ऐ", UU, "vo_pair_ai", _uu_line)]''')
# the build screen: the deck's base line carries a second sentence that names the picture
rep('def s_build(sid, base_word, base_slug, consonant, matra, syllable, result_word, sounds):',
    'def s_build(sid, base_word, base_slug, consonant, matra, syllable, result_word, sounds, base_more=""):')
rep('''        "base": vo("vo_base_" + base_slug, "यह शब्द देखिए, %s।" % base_word),''',
    '''        # [S03] «यह शब्द देखिए — सब। ये सब बच्चे हैं।» (em-dash -> comma, the measured TTS rule)
        "base": vo("vo_base_" + base_slug, ("यह शब्द देखिए, %s। %s" % (base_word, base_more)).strip()),''')

# tap screens: S02's mechanics, the S03 deck's lines
between("def s_tap(sid, words, target, matra, correct_line):", "def s_sort(", '''def s_tap(sid, words, target, matra, correct_line):
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


''')

between("def s_word_build(sid):", "SC_HEADING =", '''def s_word_build(sid):
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
                      "hint3_audio": vo("vo_p1_h3_" + slug(k),
                                        "%s लगाने से %s %s है। %s को खाली जगह में डालिए।"
                                        % (head, word, verb, head)),
                      "correct_audio": vo("vo_wb_" + slug(k),
                                          "शाबाश! %s बन %s।" % (word, gone))})
        opts.append({"akshar": head, "audio": vo("vo_ak_" + slug(k), head)})
    opts.append({"akshar": "बै", "audio": vo("vo_ak_bai", "बै")})
    opts.append({"akshar": "बे", "audio": vo("vo_ak_be", "बे")})
    return {"id": sid, "phase": "practice", "eis": "enactive", "type": "WORD_BUILD",
            "prompt_hi": "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।",
            "audio": {
                "prompt": vo("vo_%s_prompt" % sid.lower(), "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"),
                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से देखिए। चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"),
                "hint2": vo("vo_%s_prompt" % sid.lower(), "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"),
                "hint3": vo("vo_%s_h3_any" % sid.lower(),
                            "जो अक्षर चमक रहा है, उसे उसी डिब्बे में डालिए।")},
            "data": {"slots": slots, "options": opts}}


''')

rep('def s_sentence(sid, scene, pre, post, answer, options, correct_line, ask, text_only=False):',
    'def s_sentence(sid, scene, pre, post, answer, options, correct_line, h3_line, text_only=False):')
rep('''                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से पढ़िए। चित्र देखिए, %s? सही शब्द चुनकर वाक्य पूरा कीजिए।" % ask),
                "hint2": once("vo_sc_h2", "जो वाक्य सही लग रहा है, वही शब्द चुनिए।"),
                "hint3": vo("vo_%s_h3" % sid.lower(),
                            "%s %s चुनिए।" % ((pre + answer + post).replace("  ", " ").strip(),
                                              answer)),''',
    '''                # [S03] the deck's lines: one shared rung 1 and rung 2, a per-screen rung 3
                "hint1": once("vo_sc_h1", "फिर से देखिए। चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।"),
                "hint2": once("vo_sc_prompt", "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।"),
                "hint3": vo("vo_%s_h3" % sid.lower(), h3_line),''')

# ---- the flow ------------------------------------------------------------------------------
between("def build_slides():", "def build_card(slides):", '''def build_slides():
    S = []
    # ---- TUTORIAL · deck pages 2-6 -----------------------------------------------------------
    S.append(s_intro("T1"))                                                   # page 2
    S.append(s_build("T2", "सब", "sab", "स", U, "से", "सेब", "स। से। सेब।",     # page 3
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

    g4_h1 = vo("vo_g4_h1", "फिर से पढ़िए। इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।")
    p2_h1 = vo("vo_p2_h1", "फिर से सुनिए। चित्र को सही मात्रा वाले डिब्बे में डालिए।")
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
    g4_h2 = once("vo_g4_h2", "इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।")
    g4_cards = []
    for w in ["शेर", "बेर", "थैला", "पैसा"]:
        c = sort_card(w, vo("vo_ok_%s" % slug(key_of(w)),
                            "शाबाश! %s शब्द में %s की मात्रा है।" % (w, LETTER[matra_of(w)])))
        c["hint2_audio"] = g4_h2
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
    p2_h2 = once("vo_p2_h2", "मात्रा देखिए। चित्र को सही मात्रा वाले डिब्बे में डालिए।")
    p2_cards = []
    for w in ["पैन", "मेज़", "शेर", "बैग"]:                                    # page 13
        c = sort_card(w, vo("vo_okp_%s" % slug(key_of(w)),
                            "शाबाश! %s में %s की मात्रा है।" % (w, LETTER[matra_of(w)])))
        c["hint2_audio"] = p2_h2
        c["hint3_audio"] = vo("vo_p2_h3_%s" % slug(key_of(w)),
                              "%s में %s की मात्रा है। इसे %s वाले डिब्बे में डालिए।"
                              % (w, LETTER[matra_of(w)], LETTER[matra_of(w)]))
        p2_cards.append(c)
    S.append(s_sort("P2", "practice", "picture", g4_bins, p2_cards,
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    p2_h1, None))
    # three sentences - the SME deleted page 15 (मेरे ___ में दर्द है). Order = the deck's reorder.
    S.append(s_sentence("P3", "scn_likhna", "मैं ", " से लिखता हूँ।", "पैन",       # page 17
                        ["पैन", "पेड़", "बैल"], "शाबाश! मैं पैन से लिखता हूँ।",
                        "चित्र में बच्चा पैन से लिख रहा है। पैन को खाली जगह में डालिए।"))
    S.append(s_sentence("P4", "scn_bageecha", "बगीचे में एक बड़ा ", " है।", "पेड़",  # page 14
                        ["पेड़", "बैल", "पैन"], "शाबाश! बगीचे में एक बड़ा पेड़ है।",
                        "चित्र में बगीचे में एक बड़ा पेड़ है। पेड़ को खाली जगह में डालिए।"))
    S.append(s_sentence("P5", "scn_seb_khana", "मुझे ", " खाना अच्छा लगता है।", "सेब",  # page 16
                        ["सेब", "बैग", "मेज़"], "शाबाश! मुझे सेब खाना अच्छा लगता है।",
                        "चित्र में बच्चा सेब खा रहा है। सेब को खाली जगह में डालिए।"))

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


''')

# ---- card ----------------------------------------------------------------------------------
rep('vo("vo_landing", "नमस्ते दोस्त! मैं हूँ स्विफ्टी। आज हम छोटी उ और बड़ी ऊ की मात्रा वाले शब्द पढ़ेंगे।")',
    '# [S03] the deck\'s greeting + page 2\'s line, merged onto the cover the way S02 r134 merged its own\n'
    '    vo("vo_landing", "हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे।")')
rep('"part_label": "भाग 1", "medium": "hi",', '"part_label": "", "medium": "hi",')
rep('"title": {"hi": "मात्राओं की रेल", "en": "Matra train — the u / oo matras"},',
    '"title": {"hi": "मात्राओं की रेल", "en": "Matra train — the e / ai matras"},')
rep('''        "skill_description_hi": ("उ, ऊ मात्रा वाले शब्द पढ़ता है। "''',
    '''        "skill_description_hi": ("ए, ऐ मात्रा वाले शब्द पढ़ता है। "''')
rep('''                     "letters": ["उ", "ऊ"]},''', '''                     "letters": ["ए", "ऐ"]},''')

# ---- guards --------------------------------------------------------------------------------
rep('''            "SENTENCE_COMPLETE", "SENTENCE_COMPLETE", "SENTENCE_COMPLETE", "SENTENCE_COMPLETE",
            "MINI_GAME",''', '''            "SENTENCE_COMPLETE", "SENTENCE_COMPLETE", "SENTENCE_COMPLETE",   # [S03] page 15 deleted
            "MINI_GAME",''')
rep('print("  OK  flow guard: 18 screens (landing + %d slides), in Yasir\'s r134 order"',
    'print("  OK  flow guard: landing + %d slides, in S02\'s r134 order"')
rep('''        if "मी" in [o["akshar"] for o in d["options"]]:
            sys.exit("X  word-build: मी is still an option — the SME asked for it to be removed")''',
    '''        if "रे" in [o["akshar"] for o in d["options"]]:
            sys.exit("X  word-build: रे is still an option — the SME asked for it to be removed")''')
rep('''        print("  OK  word-build audit: %d coaches, exactly 1 option each, distractor %s (मी removed)"''',
    '''        print("  OK  word-build audit: %d coaches, exactly 1 option each, distractors %s (रे removed)"''')
rep('''            sys.exit("X  %r is in RIGHT_SPACING_MATRAS. It is BELOW-BASE: it shares its\\n"''',
    '''            sys.exit("X  %r is in RIGHT_SPACING_MATRAS. It is ABOVE-BASE with no advance: it shares its\\n"''')
rep('''    print("      train styles present; ु/ू correctly excluded from the in-word highlight")''',
    '''    if "ABOVE_MATRAS" not in src:
        sys.exit("X  the े/ै above-line highlight is missing from the engine - re-run inject_train.py")
    print("      train styles present; े/ै on the above-line highlight path")''')

# art briefs belong to S02's pictures
between("ART_BRIEFS = {", "def write_art_manifest", "ART_BRIEFS = {}\n\n\n")
rep('''        f.write("# %s (भाग 1 — उ / ऊ) · «मात्राओं की रेल» — VO recording list (ROUND 3)\\n\\n" % CODE)''',
    '''        f.write("# %s (ए / ऐ) · «मात्राओं की रेल» — VO recording list\\n\\n" % CODE)''')

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("converted", P)
