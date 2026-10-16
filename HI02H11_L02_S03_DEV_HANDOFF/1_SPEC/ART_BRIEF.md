# Art brief — HI02H11_L02_S03 · ए / ऐ

12 images: **8 cut-out objects** + **4 illustrated scenes**. Generated, checked and committed.
The rules and the failures that produced them are in [`_ART_RULES.md`](_ART_RULES.md).

## Objects — `gen_objects.py` (magenta key, transparent PNG)

| key | word | matra | what it is |
|---|---|---|---|
| `obj_seb` | सेब | े | scarlet apple, one leaf, one stem |
| `obj_ped` | पेड़ | े | leafy tree, trunk fused to canopy |
| `obj_rail` | रेल | े | red-and-yellow toy steam engine |
| `obj_mez` | मेज़ | े | small wooden table |
| `obj_pair` | पैर | ै | a child's bare foot, side view |
| `obj_bail` | बैल | ै | Indian bullock with a shoulder hump |
| `obj_bag` | बैग | ै | blue school backpack |
| `obj_pen` | पैन | ै | blue ballpoint pen |

Four ए and four ऐ, so every sort screen can be balanced without reusing a word as filler.

## Scenes — `gen_art.py --no-key` (background kept, 1024×1024)

One per `SENTENCE_COMPLETE` screen. These are a different asset class: the background carries the
meaning, so they must never go through the chroma-key pipeline.

| key | sentence | shows |
|---|---|---|
| `scn_bageecha` | बगीचे में एक बड़ा ___ है। | garden, one big tree, child beside it |
| `scn_pair_dard` | मेरे ___ में दर्द है। | child sitting, holding their own foot |
| `scn_seb_khana` | मुझे ___ खाना अच्छा लगता है। | child biting an apple at a table |
| `scn_likhna` | मैं ___ से लिखता हूँ। | child writing with a blue pen |

The scene must make the answer findable **without** reading — that is the point of the screen: the
child confirms meaning from the picture, then picks the word that fits the sentence.

## Why these words and not the obvious ones

केला, थैला, पैसा and मैना were all rejected, and they are exactly the words an SME would reach for
first. Each carries a **second matra** (the trailing ा), and the sort screens ask "which matra does
this word have" — a two-matra word has no single right answer. `guard_single_matra` fails the build
on it, which is the same rule that kept कुत्ता / गुलाब / जूता out of the उ/ऊ lesson.

That constraint is tighter for ए/ऐ than for उ/ऊ: the everyday ऐ nouns that survive it are few, which
is why बैग and पैन (both loanwords in common Indian use) earn their place. **If the SME would rather
avoid loanwords, the honest alternatives are गैस and बैठ — and बैठ is a verb, so it cannot be a
picture card.** Worth a ruling.
