# -*- coding: utf-8 -*-
"""Adds SENTENCE_COMPLETE (deck pages 14 / 16 / 17) and the S03 CSS to the per-game engine.

The S01 engine has no sentence screen, so this module is new - written against S01's own
machinery (makeDraggable, hintHold, sayH, withHand3, travelNudge, the .tt-card look) rather than
ported from the draft's makeHints(), so the three-rung ladder behaves exactly like the train
screens around it. Idempotent: refuses to run twice."""
p = "lesson_template.html"
s = open(p, encoding="utf-8").read()
MARK = "SlideModules.SENTENCE_COMPLETE = {"
assert MARK not in s, "already patched"

JS = r"""
/* ==========================================================================================
   [S03] SENTENCE_COMPLETE — deck pages 14, 16, 17 · «सही शब्द चुनकर वाक्य पूरा कीजिए।»
   The step from decoding to MEANING: every option is a real word the child can read, and only
   the sentence (and the picture) says which one belongs.
     scene on the left · the sentence with a dashed blank on the right · three picture+word
     cards under it. A TAP speaks a card's name; a DRAG into the blank answers.
   Ladder (one counter for the whole blank — "switching between बैल and पैन must not reset it"):
     1 · shake, the card goes home, hint1
     2 · the sentence is read with EACH option previewed in the blank, the scene detail that
         answers it is lit, then hint2. Previews are neutral — never success feedback.
     3 · the answer card and the blank glow, the other two lock, hint3. The child still drags it.
         After a rung-3 placement there is no praise line — rung 3 already said it.
   data: { scene_img, scene_emoji, sentence_pre, sentence_post, answer, matra,
           focus:{x,y,w,h} (% of the scene), options:[{word,img,emoji,audio,sent_audio}] }
   ========================================================================================== */
SlideModules.SENTENCE_COMPLETE = {
  mount(host, slide){
    const d = slide.data || {};
    newVoEpoch();
    const myGen = _voGen;
    const alive = ()=> CARD.slides[state.idx] === slide && myGen === _voGen;

    const wrap = document.createElement("div"); wrap.className = "sc-stage";
    const f = d.focus;
    wrap.innerHTML =
      '<div class="sc-scene sc-wait">' + imgOrEmoji(d.scene_img, d.scene_emoji, "sc-img", "sc-emoji") +
        (f ? '<span class="sc-focus" style="left:' + f.x + '%;top:' + f.y + '%;width:' + f.w +
             '%;height:' + f.h + '%"></span>' : "") + '</div>' +
      '<div class="sc-right">' +
        '<div class="sc-card sc-wait">' +
          '<span class="sc-pre">' + (d.sentence_pre || "") + '</span>' +
          '<span class="sc-blank dd-zone"></span>' +
          '<span class="sc-post">' + (d.sentence_post || "") + '</span>' +
        '</div>' +
        '<div class="sc-opts"></div>' +
      '</div>';
    host.appendChild(wrap);
    const scene = wrap.querySelector(".sc-scene"), card = wrap.querySelector(".sc-card");
    const blank = wrap.querySelector(".sc-blank"), row = wrap.querySelector(".sc-opts");
    const opts = (d.options || []).map(o => {
      const t = document.createElement("div"); t.className = "tt-card sc-opt sc-wait";
      t.dataset.word = o.word;
      if(o.audio) t.dataset.audio = o.audio;
      t.innerHTML = imgOrEmoji(o.img, o.emoji, "sc-optpic", "tt-emoji") +
                    '<span class="tt-lbl sc-optlbl">' + o.word + '</span>';
      row.appendChild(t);
      return t;
    });

    state.attempts = 0; state.locked = true; state.ownsAudio = true;
    state.hintUsed = false; state.helpShown = false; state.scaffoldLevel = 0;
    $("navBtn").style.display = "";
    setNavActive(false);
    state.replayAudio = ()=> sayAll([audioFor(slide, "prompt"), audioFor(slide, "sentence")].filter(Boolean), ()=>{});

    let wrongN = 0, viaHint3 = false;
    const maxA = _scafRule("max_attempts", 3);
    const answerEl = ()=> opts.find(t => t.dataset.word === d.answer);
    const pop = (el)=>{ el.classList.remove("sc-wait"); el.classList.remove("sc-in"); void el.offsetWidth; el.classList.add("sc-in"); sfxPopSoft(); };
    const speak = (t)=>{ if(t.dataset.audio && !isPlaying && !state.revealing) play(clipOf(t.dataset.audio), ()=>{}); };

    /* ENTRY: picture · sentence with its empty blank · the three cards one by one · then the
       instruction and the sentence. Nothing can be dragged until both have been heard. */
    state.revealing = true;
    const intro = [
      (n)=>{ pop(scene); setTimeout(n, 520); },
      (n)=>{ pop(card);  setTimeout(n, 520); },
    ].concat(opts.map(t => (n)=>{ pop(t); setTimeout(n, 300); }))
     .concat([
      (n)=> sayH(audioFor(slide, "prompt"), ()=> setTimeout(n, 260)),
      (n)=> sayH(audioFor(slide, "sentence"), n),
    ]);
    hintSeq(intro, ()=>{ if(!alive()) return; state.revealing = false; state.locked = false; });

    const settle = (t)=>{
      state.locked = true; stopNudge();
      blank.classList.remove("sc-glow", "sc-preview");
      blank.classList.add("filled");
      blank.innerHTML = '<span class="sc-fill">' + d.answer + '</span>';
      if(d.matra) matraHLSoon(blank.querySelector(".sc-fill"), d.matra, { glow:true });
      t.classList.remove("sc-glow"); t.classList.add("sc-used", "correct");
      opts.forEach(o => { o.style.removeProperty("pointer-events"); o.style.removeProperty("opacity"); });
      card.classList.add("sc-done");
      sfxSparkle(); fbCorrect(); confettiCannon(); setSwMood("celebrate");
      SwiftPAL.emit(d.signal || "sentence_complete", { slide_id: slide.id, phase: slide.phase, value: true,
        first_try: wrongN === 0, attempts: wrongN + 1, latency_ms: Date.now() - state.slideStart });
      const unlock = ()=> setTimeout(()=>{ if(!alive()) return; setNavActive(true);
        $("navBtn").onclick = ()=> completeSlide(wrongN === 0); }, 400);
      /* after a rung-3 placement: sparkle + chime only — "Hint 3 has already explained it" */
      if(viaHint3) setTimeout(unlock, 900);
      else play(audioFor(slide, "correct") || null, unlock);
    };

    const rung2 = ()=>{
      state.scaffoldLevel = 2; state.hintUsed = true;
      SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 2, phase: slide.phase });
      scene.classList.add("sc-focus-on");
      hintHold((fin)=> hintSeq(opts.map(t => (next)=>{
        const o = (d.options || []).find(x => x.word === t.dataset.word) || {};
        blank.classList.add("sc-preview"); blank.textContent = o.word;
        t.classList.add("is-read");
        sayH(o.sent_audio, ()=> setTimeout(()=>{
          blank.classList.remove("sc-preview"); blank.textContent = "";
          t.classList.remove("is-read");
          setTimeout(next, 300);
        }, 200));
      }), fin), ()=> play(midHint(slide) || null, ()=>{ scene.classList.remove("sc-focus-on"); }));
    };

    const rung3 = ()=>{
      state.scaffoldLevel = 3; state.hintUsed = true; state.helpShown = true; viaHint3 = true;
      const a = answerEl();
      blank.classList.add("sc-glow");
      opts.forEach(o => { if(o !== a){ o.style.setProperty("pointer-events","none","important");
                                       o.style.setProperty("opacity",".45","important"); } });
      if(a){ a.classList.add("sc-glow"); a.dataset.only = "1";
             if(d.h3_hand) withHand3(()=> travelNudge(a, blank)); }
      SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 3, phase: slide.phase });
      play(audioFor(slide, "hint3") || null, ()=>{});
    };

    opts.forEach(t => {
      makeDraggable(t, (zone, tile)=>{
        if(state.locked || zone !== blank) return;
        if(tile.dataset.word === d.answer){ settle(tile); return; }
        /* ---- wrong: the card shakes and goes home, one counter for the whole blank ---- */
        wrongN++; state.attempts = wrongN;
        tile.classList.remove("tt-shake"); void tile.offsetWidth; tile.classList.add("tt-shake");
        setTimeout(()=> tile.classList.remove("tt-shake"), 460);
        sfxShake(); setSwMood("tryagain");
        SwiftPAL.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: wrongN });
        if(hintLevels() >= 3 && wrongN === 2) rung2();
        else if(wrongN >= maxA) rung3();
        else { state.scaffoldLevel = Math.max(state.scaffoldLevel, 1);
               play(audioFor(slide, "hint1") || audioFor(slide, "try_again") || null, ()=>{}); }
      }, {
        onTap: ()=> speak(t),
        onPick: ()=> speak(t)
      });
    });
    /* FAIL-SAFE: never leave the cards dead if the intro chain stalls */
    setTimeout(()=>{ if(alive() && state.revealing && !_hintBusy){ state.revealing = false; state.locked = false; } }, 30000);
  }
};
"""

CSS = r"""
/* ==== [S03] HI02H11_L02_S03 additions ================================================== */
/* MATRA_BUILD «सब»: one soft outline round the whole group, and the picture lit while named */
.mb-pic.mb-group{ border:3px dashed #7FB2F0; border-radius:28px; background:rgba(127,178,240,.08);
  padding:6px; }
.mb-pic{ transition:box-shadow .3s ease, transform .3s ease; border-radius:24px; }
.mb-pic.mb-pic-hl{ box-shadow:0 0 0 6px rgba(255,206,46,.75), 0 0 28px rgba(255,206,46,.55);
  transform:scale(1.04); }
/* TRAIN_SORT / MATRA_FILL rung helpers */
.tt-card.tt-big{ transform:scale(1.18) !important; z-index:30; transition:transform .25s ease; }
.tt-card.tt-glow{ box-shadow:0 0 0 6px rgba(255,206,46,.8), 0 0 26px rgba(255,206,46,.6) !important; }
.tt-card.tt-spent{ opacity:.45; pointer-events:none; filter:grayscale(.3); }
.tt-card .tt-tmp{ animation:scIn .35s ease both; }
.mf-blank.mf-glow{ box-shadow:0 0 0 6px rgba(255,206,46,.8), 0 0 22px rgba(255,206,46,.6); }
.tt-card.tt-akshar .tt-glyph{ font-size:clamp(30px,5.4vh,52px); }

/* SENTENCE_COMPLETE */
.sc-stage{ display:flex; align-items:center; justify-content:center; gap:34px; width:100%;
  height:100%; padding:0 24px 18px; box-sizing:border-box; }
.sc-scene{ position:relative; flex:0 0 auto; line-height:0; border-radius:24px; overflow:hidden;
  background:#fff; border:4px solid #fff; box-shadow:0 10px 26px rgba(11,61,140,.16); }
.sc-img{ width:380px; height:380px; object-fit:cover; display:block; }
.sc-emoji{ font-size:200px; line-height:1; display:block; padding:40px; }
.sc-focus{ position:absolute; border-radius:22px; pointer-events:none; opacity:0;
  transition:opacity .3s ease; box-shadow:0 0 0 5px #FFCE2E, 0 0 0 9999px rgba(11,61,140,.28); }
.sc-scene.sc-focus-on .sc-focus{ opacity:1; animation:scPulse 1.4s ease-in-out infinite; }
@keyframes scPulse{ 0%,100%{ box-shadow:0 0 0 5px #FFCE2E, 0 0 0 9999px rgba(11,61,140,.28);}
  50%{ box-shadow:0 0 0 9px #FFCE2E, 0 0 0 9999px rgba(11,61,140,.28);} }
.sc-right{ display:flex; flex-direction:column; align-items:center; gap:30px; flex:0 1 auto; min-width:0; }
.sc-card{ background:#fff; border:3px solid #CFE3FA; border-radius:22px; padding:20px 28px;
  box-shadow:0 8px 22px rgba(11,61,140,.12); display:flex; align-items:center; justify-content:center;
  gap:12px; flex-wrap:wrap; max-width:640px; font-family:var(--font-hi,'Baloo 2'),sans-serif;
  font-size:42px; font-weight:800; line-height:1.6; color:var(--navy-dk,#0B3D8C);
  transition:border-color .3s, background .3s; }
.sc-card.sc-done{ border-color:#7DD3A8; background:#F4FCF8; }
.sc-blank{ display:inline-flex; align-items:center; justify-content:center; min-width:150px; height:66px;
  border-radius:14px; border:3px dashed #2BA79B; background:#F3FBF9; padding:0 10px; box-sizing:border-box; }
.sc-blank.hover{ outline:4px dashed #2BA79B; outline-offset:3px; background:#EAFBF6; }
.sc-blank.sc-preview{ border-style:dashed; border-color:#9DB4D6; background:#F5F8FD; color:#5B6F92; }
.sc-blank.filled{ border-style:solid; border-color:#4CAF7D; background:#EAFBF6; }
.sc-blank.sc-glow{ box-shadow:0 0 0 6px rgba(255,206,46,.8), 0 0 24px rgba(255,206,46,.6); }
.sc-fill{ display:inline-block; font-size:42px; line-height:1.4; }
.sc-opts{ display:flex; gap:22px; justify-content:center; }
.sc-opt{ position:relative; display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:4px; width:150px; height:168px; background:#fff; border:3px solid #CFE3FA; border-radius:18px;
  box-shadow:0 6px 0 rgba(11,61,140,.10); cursor:grab; touch-action:none; z-index:2; box-sizing:border-box; padding:8px; }
.sc-opt.dragging{ z-index:60; cursor:grabbing; }
.sc-opt .sc-optpic{ width:96px; height:96px; object-fit:contain; }
.sc-opt .sc-optlbl{ font-family:var(--font-hi,'Baloo 2'),sans-serif; font-size:30px; font-weight:800;
  color:var(--navy-dk,#0B3D8C); line-height:1.4; }
.sc-opt.is-read{ border-color:#8BBFFF; box-shadow:0 0 0 5px rgba(139,191,255,.55); }
.sc-opt.sc-glow{ border-color:#F7C948; box-shadow:0 0 0 6px rgba(255,206,46,.8), 0 0 24px rgba(255,206,46,.6); }
.sc-opt.sc-used{ opacity:.35; pointer-events:none; }
.sc-wait{ opacity:0; }
.sc-in{ animation:scIn .45s cubic-bezier(.34,1.56,.64,1) both; }
@keyframes scIn{ from{ opacity:0; transform:scale(.86); } to{ opacity:1; transform:none; } }
@media (prefers-reduced-motion:reduce){ .sc-in{ animation:none; opacity:1; } }
"""

at = s.index("SlideModules.MEET_PAIR = {")
# put the module just before the comment block that introduces MEET_PAIR
cm = s.rfind("/* ================================================================ 5 · MEET_PAIR */", 0, at)
ins = cm if cm > 0 else at
s = s[:ins] + JS + "\n" + s[ins:]
i = s.rfind("</style>")
s = s[:i] + CSS + "\n" + s[i:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("sentence module + css added")
