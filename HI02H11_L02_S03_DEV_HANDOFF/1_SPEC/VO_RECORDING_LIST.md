# HI02H11_L02_S03 (ए / ऐ) · «मात्राओं की रेल» — VO recording list

115 clips. Shown text == spoken text; record exactly this.

**Register is आप** — the SME asked for it twice, in as many words. Round 2 was तुम, so most of this list is a re-record, not a new line. `guard_register` in the builder fails the build if a तुम form survives anywhere.

**Only re-record what changed.** The builder deletes exactly the clips whose text moved this round, so `gen_tts.py` (which skips ids that already have a file) regenerates precisely those and leaves every unchanged take alone. Never `--force` the whole card: generated audio is non-deterministic, so re-running an unchanged clip returns a different take — a change the SME never asked for.

## ⚠️ EAR-CHECK — 2 clips a human must listen to before delivery

The TTS model truncates a clip when an **em-dash precedes a short final word** (measured on this lesson: em-dash 0.73–1.05 s vs comma 1.53–2.21 s for the same words), and it does the same to a line built from several short danda-separated pieces. The SME's round-3 MEET_PAIR lines and the new sound-differentiation clips are written in exactly those shapes. Their wording ships as written — rewriting a reviewer's Hindi to dodge a synthesis bug is the worse failure — so the clips are flagged instead. **Truncation is invisible to an existence check and to a file-size check.** `_verify_assets.py` compares each clip against peers of similar text length and is the only thing that catches it. Run it, then listen to every id below.

- `vo_sounds_pair` — प। पै। पैर।
- `vo_sounds_seb` — स। से। सेब।

## All clips

| clip id | spoken text |
|---|---|
| `vo_ak_bai` | बै |
| `vo_ak_be` | बे |
| `vo_ak_mez` | मे |
| `vo_ak_pair` | पै |
| `vo_ak_seb` | से |
| `vo_base_par` | यह शब्द देखिए, पर। मेज़ पर किताब रखी है। |
| `vo_base_sab` | यह शब्द देखिए, सब। ये सब बच्चे हैं। |
| `vo_cel_prompt` | बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया! |
| `vo_g1_correct` | शाबाश! सेब शब्द में ए की मात्रा है। |
| `vo_g1_h3` | सेब शब्द में ए की मात्रा है। सेब पर टैप कीजिए। |
| `vo_g2_correct` | शाबाश! पैन शब्द में ऐ की मात्रा है। |
| `vo_g2_h3` | पैन शब्द में ऐ की मात्रा है। पैन पर टैप कीजिए। |
| `vo_g3_correct` | शाबाश! बैग शब्द में ऐ की मात्रा है। |
| `vo_g3_h3` | बैग शब्द में ऐ की मात्रा है। बैग पर टैप कीजिए। |
| `vo_g4_h1` | फिर से पढ़िए। इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए। |
| `vo_g4_h2` | इस शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए। |
| `vo_g4_h3_ber` | बेर शब्द में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए। |
| `vo_g4_h3_paisa` | पैसा शब्द में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए। |
| `vo_g4_h3_sher` | शेर शब्द में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए। |
| `vo_g4_h3_thaila` | थैला शब्द में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए। |
| `vo_g4_prompt` | हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए। |
| `vo_g4d_end` | अब आप भी ऐसे ही करके देखिए। |
| `vo_g5_h1` | फिर से देखिए। सही मात्रा को सही डिब्बे में डालिए। |
| `vo_g5_h2` | मात्रा का आकार ध्यान से देखिए। इसे सही डिब्बे में डालिए। |
| `vo_g5_h3_ai` | यह ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए। |
| `vo_g5_h3_e` | यह ए की मात्रा है। इसे ए वाले डिब्बे में डालिए। |
| `vo_g5_prompt` | सही मात्रा को सही डिब्बे में डालिए। |
| `vo_g5d_ai` | ऐ की मात्रा इस डिब्बे पर है, इसलिए ऐ इस डिब्बे में गया। |
| `vo_g5d_e` | ए की मात्रा इस डिब्बे पर है, इसलिए ए इस डिब्बे में गया। |
| `vo_g5d_prompt` | देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं। |
| `vo_landing` | हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम ए और ऐ की मात्रा वाले शब्द पढ़ेंगे। |
| `vo_letter_ai` | ऐ |
| `vo_letter_e` | ए |
| `vo_matra_ai` | ऐ की मात्रा |
| `vo_matra_e` | ए की मात्रा |
| `vo_meet_bail` | बैल, इसमें ब पर ऐ की मात्रा लगी है। बोलकर देखिए। |
| `vo_meet_bhains` | भैंस, इसमें भ पर ऐ की मात्रा लगी है। बोलकर देखिए। |
| `vo_meet_mez` | मेज़, इसमें म पर ए की मात्रा लगी है। बोलकर देखिए। |
| `vo_meet_ped` | पेड़, इसमें प पर ए की मात्रा लगी है। बोलकर देखिए। |
| `vo_mg_prompt` | अब एक खेल! ऊपर दी गई मात्रा वाले शब्द पकड़िए। |
| `vo_mic_nudge` | इस बटन पर टैप करिए। |
| `vo_name_bag` | बैग |
| `vo_name_bail` | बैल |
| `vo_name_ber` | बेर |
| `vo_name_mez` | मेज़ |
| `vo_name_pair` | पैर |
| `vo_name_paisa` | पैसा |
| `vo_name_ped` | पेड़ |
| `vo_name_pen` | पैन |
| `vo_name_rail` | रेल |
| `vo_name_seb` | सेब |
| `vo_name_sher` | शेर |
| `vo_name_thaila` | थैला |
| `vo_ok_ber` | शाबाश! बेर शब्द में ए की मात्रा है। |
| `vo_ok_matra_ai` | शाबाश! यह ऐ की मात्रा है। |
| `vo_ok_matra_e` | शाबाश! यह ए की मात्रा है। |
| `vo_ok_paisa` | शाबाश! पैसा शब्द में ऐ की मात्रा है। |
| `vo_ok_sher` | शाबाश! शेर शब्द में ए की मात्रा है। |
| `vo_ok_thaila` | शाबाश! थैला शब्द में ऐ की मात्रा है। |
| `vo_okp_bag` | शाबाश! बैग में ऐ की मात्रा है। |
| `vo_okp_mez` | शाबाश! मेज़ में ए की मात्रा है। |
| `vo_okp_pen` | शाबाश! पैन में ऐ की मात्रा है। |
| `vo_okp_sher` | शाबाश! शेर में ए की मात्रा है। |
| `vo_onset_pair` | प के साथ ऐ की मात्रा लगाने पर पै बनता है। |
| `vo_onset_seb` | स के साथ ए की मात्रा लगाने पर से बनता है। |
| `vo_p1_h1` | फिर से देखिए। चित्र देखकर सही अक्षर से शब्द पूरा कीजिए। |
| `vo_p1_h3_any` | जो अक्षर चमक रहा है, उसे उसी डिब्बे में डालिए। |
| `vo_p1_h3_mez` | मे लगाने से मेज़ बनती है। मे को खाली जगह में डालिए। |
| `vo_p1_h3_pair` | पै लगाने से पैर बनता है। पै को खाली जगह में डालिए। |
| `vo_p1_h3_seb` | से लगाने से सेब बनता है। से को खाली जगह में डालिए। |
| `vo_p1_prompt` | चित्र देखकर सही अक्षर से शब्द पूरा कीजिए। |
| `vo_p2_h1` | फिर से सुनिए। चित्र को सही मात्रा वाले डिब्बे में डालिए। |
| `vo_p2_h2` | मात्रा देखिए। चित्र को सही मात्रा वाले डिब्बे में डालिए। |
| `vo_p2_h3_bag` | बैग में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए। |
| `vo_p2_h3_mez` | मेज़ में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए। |
| `vo_p2_h3_pen` | पैन में ऐ की मात्रा है। इसे ऐ वाले डिब्बे में डालिए। |
| `vo_p2_h3_sher` | शेर में ए की मात्रा है। इसे ए वाले डिब्बे में डालिए। |
| `vo_p2_prompt` | चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए। |
| `vo_p3_correct` | शाबाश! मैं पैन से लिखता हूँ। |
| `vo_p3_h3` | चित्र में बच्चा पैन से लिख रहा है। पैन को खाली जगह में डालिए। |
| `vo_p3_try_bail` | मैं बैल से लिखता हूँ। |
| `vo_p3_try_ped` | मैं पेड़ से लिखता हूँ। |
| `vo_p3_try_pen` | मैं पैन से लिखता हूँ। |
| `vo_p4_correct` | शाबाश! बगीचे में एक बड़ा पेड़ है। |
| `vo_p4_h3` | चित्र में बगीचे में एक बड़ा पेड़ है। पेड़ को खाली जगह में डालिए। |
| `vo_p4_try_bail` | बगीचे में एक बड़ा बैल है। |
| `vo_p4_try_ped` | बगीचे में एक बड़ा पेड़ है। |
| `vo_p4_try_pen` | बगीचे में एक बड़ा पैन है। |
| `vo_p5_correct` | शाबाश! मुझे सेब खाना अच्छा लगता है। |
| `vo_p5_h3` | चित्र में बच्चा सेब खा रहा है। सेब को खाली जगह में डालिए। |
| `vo_p5_try_bag` | मुझे बैग खाना अच्छा लगता है। |
| `vo_p5_try_mez` | मुझे मेज़ खाना अच्छा लगता है। |
| `vo_p5_try_seb` | मुझे सेब खाना अच्छा लगता है। |
| `vo_pair_ai` | यह है ऐ। इसकी मात्रा देखिए। |
| `vo_pair_e` | यह है ए। इसकी मात्रा देखिए। |
| `vo_result_pair` | अब र जुड़ने पर पैर बनता है। |
| `vo_result_seb` | अब ब जुड़ने पर सेब बनता है। |
| `vo_sc_h1` | फिर से देखिए। चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए। |
| `vo_sc_prompt` | चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए। |
| `vo_sounds_pair` | प। पै। पैर। |
| `vo_sounds_seb` | स। से। सेब। |
| `vo_t2_prompt` | आइए, देखें कि ए की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_t3_prompt` | आइए, ए की मात्रा वाले कुछ शब्द देखें। |
| `vo_t4_prompt` | आइए, देखें कि ऐ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_t5_prompt` | आइए, ऐ की मात्रा वाले कुछ शब्द देखें। |
| `vo_tap_h1_ai` | फिर से पढ़िए। ऐ की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h1_e` | फिर से पढ़िए। ए की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h2_ai` | ऐ की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h2_e` | ए की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_prompt_ai` | जिस डिब्बे में ऐ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_tap_prompt_e` | जिस डिब्बे में ए की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_try_again` | एक बार फिर सुनिए। |
| `vo_wb_mez` | शाबाश! मेज़ बन गई। |
| `vo_wb_pair` | शाबाश! पैर बन गया। |
| `vo_wb_seb` | शाबाश! सेब बन गया। |

## Copied, do NOT record

- `vo_pt_tutorial`
- `vo_pt_guided`
- `vo_pt_practice`
- `sfx_celebrate`
- `sfx_correct`
- `sfx_wrong`
- `sfx_tap`
- `sfx_pop`
- `sfx_fb_correct`
- `sfx_fb_incorrect`
- `sfx_play_button`
- `sfx_next_button`
- `sfx_train_arrive`
- `sfx_train_move`
- `sfx_whistle`
