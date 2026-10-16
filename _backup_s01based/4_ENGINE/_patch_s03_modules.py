# -*- coding: utf-8 -*-
"""S03 module edits on top of the S01 engine copy. Each one is gated on a card data flag, so a
card that does not set the flag renders exactly as S01 did. Run once; asserts refuse a re-run."""
p = "lesson_template.html"
s = open(p, encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)


# ---------------------------------------------------------------- MATRA_BUILD
rep("""    row.appendChild(p1);

    const a1 = document.createElement("div");""",
"""    row.appendChild(p1);
    /* [S03] «सब» is pictured as a GROUP: one soft outline round all three children (page 3).
       And on «ये सब बच्चे हैं।» / «मेज़ पर किताब रखी है।» the picture is lit while it is named. */
    const p1pic = p1.querySelector(".mb-pic");
    if(d.base_outline && p1pic) p1pic.classList.add("mb-group");

    const a1 = document.createElement("div");""")
rep("""      (next)=>{ show(p1); sfxPopSoft();
                setTimeout(()=> sayH(audioFor(slide, "base"), ()=> setTimeout(next, 520)), 260); },""",
"""      (next)=>{ show(p1); sfxPopSoft();
                let _bt = null;
                if(d.base_hl_ms != null && p1pic) _bt = setTimeout(()=>{
                  if(CARD.slides[state.idx] !== slide || myGen !== _voGen) return;
                  p1pic.classList.add("mb-pic-hl"); }, 260 + Math.max(0, d.base_hl_ms));
                setTimeout(()=> sayH(audioFor(slide, "base"), ()=>{ clearTimeout(_bt);
                  if(p1pic) p1pic.classList.remove("mb-pic-hl");
                  setTimeout(next, 520); }), 260); },""")

# ---------------------------------------------------------------- TRAIN_TAP
rep("""      sayH(o.audio, ()=> setTimeout(()=>{
        if(coach) coach.classList.remove("is-read");
        if(typeof matraClear === "function") matraClear(w);
        next();
      }, 260));
    }), fin), done);""",
"""      sayH(o.audio, ()=> setTimeout(()=>{
        if(coach) coach.classList.remove("is-read");
        /* [S03] "Retain the matra highlights in all three words so the child can compare." */
        if(!d.keep_hl && typeof matraClear === "function") matraClear(w);
        next();
      }, 260));
    }), fin), done);""")
rep("""      ladder3: { demo: tapDemo, lock: tapLock },""",
"""      ladder3: { demo: tapDemo, lock: ()=>{ tapLock();
        /* [S03] rung 3 keeps the answer's matra lit inside its coach */
        const cw = train.faceEls[correctIdx] && train.faceEls[correctIdx].querySelector(".coach-word");
        if(d.keep_hl && cw && opts[correctIdx] && opts[correctIdx].matra) matraHLSoon(cw, opts[correctIdx].matra, { glow:true }); } },""")
rep("""    opts.forEach((o, i)=>{
      const face = train.faceEls[i];
      face.innerHTML = '<span class="coach-word ink-glyph">' + (o.word_hi || o.letter || "") + '</span>';
      built.push(train.coachEls[i]);
    });""",
"""    opts.forEach((o, i)=>{
      const face = train.faceEls[i];
      face.innerHTML = '<span class="coach-word ink-glyph">' + (o.word_hi || o.letter || "") + '</span>';
      built.push(train.coachEls[i]);
      /* [S03] "Correct answer ... Highlight only े inside सेब in red." The engine marks the cell
         .correct; we watch for that and light the matra in that coach's word. */
      if(o.correct && o.matra && d.hl_on_correct){
        const c = train.coachEls[i];
        const mo = new MutationObserver(()=>{ if(c.classList.contains("correct")){ mo.disconnect();
          const w = face.querySelector(".coach-word"); if(w) matraHLSoon(w, o.matra, { glow:true }); } });
        mo.observe(c, { attributes:true, attributeFilter:["class"] });
      }
    });""")

# ---------------------------------------------------------------- TRAIN_SORT
rep("""      if(it.hint2_audio) t.dataset.h2 = it.hint2_audio;""",
"""      if(it.hint2_audio) t.dataset.h2 = it.hint2_audio;
      if(it.hint1_audio) t.dataset.h1 = it.hint1_audio;          /* [S03] per-card rung-1 line */
      if(it.word_hi) t.dataset.word = it.word_hi;""")
rep("""      if(!multi) body.classList.add("filled");     // "Only one word can be placed inside each coach" (row #130)""",
"""      if(!multi) body.classList.add("filled");     // "Only one word can be placed inside each coach" (row #130)
      /* [S03] the temporary rung-2 word support goes once the picture is placed; and a placed
         word / matra card shows its target matra in red */
      const _tmp = t.querySelector(".tt-tmp"); if(_tmp) _tmp.remove();
      t.classList.remove("tt-big", "tt-glow");
      if(d.hl_on_correct && t.dataset.matra){
        const _hl = t.querySelector(".tt-lbl") || t.querySelector(".tt-glyph");
        if(_hl) setTimeout(()=> matraHLSoon(_hl, t.dataset.matra, { glow:true }), 60);
      }""")
rep("""            const lbl = t.querySelector(".tt-lbl");
            const steps = [];
            steps.push((next)=>{
              if(lbl && t.dataset.matra && typeof matraHLSoon === "function")
                matraHLSoon(lbl, t.dataset.matra, { glow:true, pulse:true });
              sayH(t.dataset.audio, ()=> setTimeout(()=>{
                if(typeof matraClear === "function") matraClear(lbl);
                next();
              }, 260));
            });
            train.coachEls.forEach((c2)=>{
              const lb = c2.querySelector(".coach-label");
              const b2 = c2.querySelector(".coach-body");
              if(!lb || !b2 || b2.classList.contains("filled")) return;   /* a solved coach is done */""",
"""            let lbl = t.querySelector(".tt-lbl") || t.querySelector(".tt-glyph");
            /* [S03] pictures-only screen: "During Hint 2 only, temporarily show the wrongly dropped
               picture's name and highlight its matra ... Keep this word support visible for the
               next attempt." It is removed when the picture is placed (landCard). */
            if(!lbl && d.h2_show_word && t.dataset.word){
              lbl = document.createElement("span"); lbl.className = "tt-lbl tt-tmp";
              lbl.textContent = t.dataset.word; t.appendChild(lbl);
            }
            const steps = [];
            steps.push((next)=>{
              if(d.h2_enlarge) t.classList.add("tt-big");
              if(lbl && t.dataset.matra && typeof matraHLSoon === "function")
                matraHLSoon(lbl, t.dataset.matra, { glow:true, pulse:true });
              sayH(d.h2_silent_name ? null : t.dataset.audio, ()=> setTimeout(()=>{
                if(!d.keep_hl && typeof matraClear === "function") matraClear(lbl);
                if(d.h2_enlarge) setTimeout(()=> t.classList.remove("tt-big"), 1400);
                next();
              }, d.h2_silent_name ? 1100 : 260));
            });
            train.coachEls.forEach((c2)=>{
              const lb = c2.querySelector(".coach-label");
              const b2 = c2.querySelector(".coach-body");
              if(!lb || !b2 || b2.classList.contains("filled")) return;   /* a solved coach is done */
              if(!b2.dataset.labelAudio) return;     /* [S03] no clip for the label -> nothing to read */""")
rep("""            play((n <= 1 ? (audioFor(slide, "hint1") || audioFor(slide, "try_again"))
                         : midHint(slide)) || null, ()=>{});
            /* the two-rung fallback for a card authored without hint_levels:3 - unchanged */
            if(hintLevels() < 3 && n >= _scafRule("hand_on_attempt", 99)){
              const goal = _goalOf(t);""",
"""            play((n <= 1 ? (clipOf(t.dataset.h1) || audioFor(slide, "hint1") || audioFor(slide, "try_again"))
                         : midHint(slide)) || null, ()=>{});
            /* the two-rung fallback for a card authored without hint_levels:3 - unchanged */
            if(hintLevels() < 3 && n >= _scafRule("hand_on_attempt", 99)){
              const goal = _goalOf(t);""")
rep("""              t.dataset.only = t.dataset.key;            /* see the guard at the top of this handler */
              withHand3(()=> travelNudge(t, gb));""",
"""              t.dataset.only = t.dataset.key;            /* see the guard at the top of this handler */
              /* [S03] "Temporarily disable other unfinished cards until this guided placement is
                 complete." Released in the correct branch. */
              if(d.h3_freeze) [...tray.children].forEach(o2 => { if(o2 !== t && !o2.classList.contains("snapped")){
                o2.style.setProperty("pointer-events","none","important"); o2.style.setProperty("opacity",".45","important"); } });
              t.classList.add("tt-glow");
              if(d.h3_hand !== false) withHand3(()=> travelNudge(t, gb));""")
rep("""            clearHold(tray); clearHold(train.rail);
            state.helpShown = false; state.scaffoldLevel = 0;
          }
          SwiftPAL.emit("matra_sort_item",""",
"""            clearHold(tray); clearHold(train.rail);
            [...tray.children].forEach(o2 => { o2.style.removeProperty("pointer-events"); o2.style.removeProperty("opacity"); });
            state.helpShown = false; state.scaffoldLevel = 0;
          }
          SwiftPAL.emit("matra_sort_item",""")

# ---------------------------------------------------------------- MATRA_FILL (akshar mode = page 12)
rep("""      blank.dataset.key = s.matra;
      blank.dataset.slot = String(i);""",
"""      blank.dataset.key = s.key || s.matra;         /* [S03] akshar mode keys on «से», highlights «े» */
      blank.dataset.slot = String(i);""")
rep("""      train.coachEls[i].dataset.key = s.matra;""",
"""      train.coachEls[i].dataset.key = s.key || s.matra;""")
rep("""    shuffled(d.options || []).forEach(m => {
      const t = document.createElement("div"); t.className = "tt-card";
      t.dataset.key = m;
      t.innerHTML = '<span class="tt-glyph ink-glyph">' + matraGlyph(m) + '</span>';
      tray.appendChild(t);
    });""",
"""    shuffled(d.options || []).forEach(m => {
      const t = document.createElement("div"); t.className = "tt-card" + (d.akshar ? " tt-akshar" : "");
      t.dataset.key = m;
      /* [S03] tapping an अक्षर card speaks only its sound */
      if(d.option_audio && d.option_audio[m]) t.dataset.audio = d.option_audio[m];
      if(d.option_matra && d.option_matra[m]) t.dataset.matra = d.option_matra[m];
      t.innerHTML = '<span class="tt-glyph ink-glyph">' + matraGlyph(m) + '</span>';
      tray.appendChild(t);
    });""")
rep("""          if(state.helpShown){
            stopNudge();
            host.querySelectorAll(".mf-blank.nudge").forEach(b => b.classList.remove("nudge"));
            clearHold(tray);
            state.helpShown = false; state.scaffoldLevel = 0;
          }""",
"""          if(state.helpShown){
            stopNudge();
            host.querySelectorAll(".mf-blank.nudge").forEach(b => b.classList.remove("nudge", "mf-glow"));
            clearHold(tray);
            [...tray.children].forEach(o2 => { o2.style.removeProperty("pointer-events");
              o2.style.removeProperty("opacity"); o2.classList.remove("tt-glow"); delete o2.dataset.only; });
            state.helpShown = false; state.scaffoldLevel = 0;
          }""")
rep("""          if(filled === slots.length){
            state.locked = true;
            SwiftPAL.emit(d.signal || "matra_fill_correct", {""",
"""          if(filled === slots.length){
            state.locked = true;
            /* [S03] "Leave the unused distractors in the tray and disable them." */
            [...tray.children].forEach(o2 => o2.classList.add("tt-spent"));
            SwiftPAL.emit(d.signal || "matra_fill_correct", {""")
rep("""          if(hintLevels() >= 3 && n === 2){
            /* RUNG 2 - DEMONSTRATE. Name each word that still has a hole in it, one at a time,""",
"""          if(hintLevels() >= 3 && n === 2 && d.akshar){
            /* [S03] RUNG 2 for the अक्षर screen: "Read only the wrongly dropped अक्षर. Slightly
               enlarge that card and highlight its matra in red ... After the VO finishes, return
               the card to its normal size." No hand, nothing locked. */
            state.scaffoldLevel = 2; state.hintUsed = true;
            SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 2, phase: slide.phase });
            const g = t.querySelector(".tt-glyph");
            hintHold((fin)=>{
              t.classList.add("tt-big");
              if(g && t.dataset.matra) matraHLSoon(g, t.dataset.matra, { glow:true, pulse:true });
              sayH(t.dataset.audio, ()=> setTimeout(fin, 260));
            }, ()=> play(midHint(slide) || null, ()=>{
              t.classList.remove("tt-big"); if(g) matraClear(g); }));
          }
          else if(hintLevels() >= 3 && n === 2){
            /* RUNG 2 - DEMONSTRATE. Name each word that still has a hole in it, one at a time,""")
rep("""            state.scaffoldLevel = 3; state.hintUsed = true; state.helpShown = true;
            const goal = _goal();
            if(goal){
              goal.classList.add("nudge");
              t.dataset.only = t.dataset.key;    /* see the guard at the top of this handler */
              withHand3(()=> travelNudge(t, goal));
            }
            SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 3, phase: slide.phase });
            play(audioFor(slide, "hint3") || midHint(slide) || null, ()=>{});""",
"""            state.scaffoldLevel = 3; state.hintUsed = true; state.helpShown = true;
            if(d.akshar){
              /* [S03] RUNG 3, अक्षर screen: the counter is THIS blank's, so this blank is the one
                 guided - its correct अक्षर and the blank glow, everything else locks, and the child
                 still drags it in. Works the same whether the miss was a distractor or a real
                 अक्षर dropped on the wrong word. */
              const sl = slots[si] || {};
              const ct = [...tray.children].find(o2 => o2.dataset.key === blank.dataset.key);
              blank.classList.add("nudge", "mf-glow");
              [...tray.children].forEach(o2 => { if(o2 !== ct){
                o2.style.setProperty("pointer-events","none","important"); o2.style.setProperty("opacity",".45","important"); } });
              if(ct){ ct.classList.add("tt-glow"); ct.dataset.only = blank.dataset.key;
                      if(d.h3_hand) withHand3(()=> travelNudge(ct, blank)); }
              SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 3, phase: slide.phase });
              play(clipOf(sl.hint3_audio) || audioFor(slide, "hint3") || null, ()=>{});
            } else {
            const goal = _goal();
            if(goal){
              goal.classList.add("nudge");
              t.dataset.only = t.dataset.key;    /* see the guard at the top of this handler */
              withHand3(()=> travelNudge(t, goal));
            }
            SwiftPAL.emit("hint_shown", { slide_id: slide.id, level: 3, phase: slide.phase });
            play(audioFor(slide, "hint3") || midHint(slide) || null, ()=>{});
            }""")
rep("""      }, {
        onTap: ()=>{ /* a matra card has no word to speak */ }
      });""",
"""      }, {
        onTap: ()=>{ if(tile.dataset.audio && !isPlaying) play(VO_DIR + tile.dataset.audio + "." + AUDIO_EXT, ()=>{}); }
      });""")

open(p, "w", encoding="utf-8", newline="").write(s)
print("patched")
