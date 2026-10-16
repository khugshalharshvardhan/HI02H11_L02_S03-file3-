# Art rules — HI02H11_L02_S03

Two asset classes in this bundle, and they must **not** be generated the same way.

| class | keys | pipeline |
|---|---|---|
| `obj_*` (8) | cut-out objects on transparency | `gen_objects.py` — magenta chroma key + keep-largest + autocrop |
| `scn_*` (4) | full illustrated scenes for `SENTENCE_COMPLETE` | `gen_art.py --no-key` — the background is the point, **never** key these |

## The rules that came from actual failures

Every one of these cost a regeneration on this lesson or the sibling.

1. **ONE SINGLE CONNECTED SHAPE.** `keep_largest` throws away everything but the biggest blob, so
   a subject with detached parts (a sun's rays, a crown's points) ships with the parts missing.
   Say "FUSED ONTO … so the whole X is one connected silhouette" in the prompt.
2. **Saturated colour. Never white, never pale.** A white subject keys out with the background and
   the PNG comes back blank — or, worse, 82% opaque and *looks* fine to a checker while being a
   solid block on screen.
3. **No white panels behind the subject.**
4. **The background must be flat magenta edge to edge**, stated in those words.
5. **Nothing pink.** A pink object fights the magenta key. (Which is why the sunflower, not a rose.)

## NEW, from this lesson: the decorative splash

`obj_seb` came back **three times** with a painterly pink cloud behind the apple. It was not a
keying failure — the model was *painting a decorative splash* as part of the illustration, and
`keep_largest` kept it because it touches the apple's stem.

It survived every automated check: 57% opaque, 29 colour buckets, and my own magenta test counted
only 0.46% of the object, because the splash is **pink (hue 340), not magenta**, and the test wants
`g <= b - 40`.

Prompting against it failed twice, including an explicit "NO paint splash, NO halo, NO decorative
shape". The fix that worked is a post-process: flood-fill inward **from the top border through
pinkish pixels only** (hue 300-348, sat ≥ 0.55), which stops dead at the apple because the apple
sits at hue 350-360. Measured before committing to the thresholds:

| region | hue | sat |
|---|---|---|
| splash | 340 | 0.90 |
| apple body | 350-360 | 0.80 |

26,545 px cleared; leaf, stem, outline and highlights all intact.

**If you regenerate `obj_seb`, look at it.** The detector will pass the splash again.

## Scenes — what to keep an eye on

Both known issues are cosmetic and were left as-is, not missed:

- `scn_pair_dard` has alphabet blocks reading **"A B"** in the background — Latin letters in a
  Hindi reading lesson.
- `scn_likhna`'s notebook page carries **squiggles** rather than the blank page the prompt asked
  for. They are not letters of any script, so they do not compete with the lesson's own text.

Both are small background props. Re-roll only if the SME wants them gone.
