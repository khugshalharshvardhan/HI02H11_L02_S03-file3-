# -*- coding: utf-8 -*-
"""Gemini TTS (voice Kore) for whole lines, with a length check and retries; writes 24 kHz mono WAV under
the .ogg name the lesson uses, then levels it to -16 LUFS (S02's VO level).
  python tts_lines.py <todo.json {"assets":{"audio_text":{id:text}}}> <audio_dir>"""
import os, sys, json, base64, wave, time, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["GEMINI_KEY"]
MODELS = ["gemini-2.5-flash-preview-tts"] * 4 + ["gemini-2.5-pro-preview-tts"] * 2
def synth(text, model):
    body = {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}}}
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model, KEY)
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(body).encode(),
                       headers={"Content-Type": "application/json"}), timeout=90).read())
        ps = d["candidates"][0].get("content", {}).get("parts", [])
        if ps and "inlineData" in ps[0]: return base64.b64decode(ps[0]["inlineData"]["data"])
    except Exception as e:
        print("   retry", model[14:18], str(e)[:60], flush=True); time.sleep(3)
    return None
def floor(t): return 0.10 * len(t.replace(" ", "").replace("।", "").replace(",", "").replace("!", "").replace("…", ""))
def one(item):
    k, t, out = item; best = None
    for m in MODELS:
        pcm = synth(t, m)
        if not pcm: continue
        dur = len(pcm) / 48000
        if not best or dur > best[0]: best = (dur, pcm, m)
        if dur >= floor(t): break
    if not best:
        print("FAILED", k, t, flush=True); return k, False
    raw = os.path.join(out, k + ".raw.wav")
    w = wave.open(raw, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(best[1]); w.close()
    dst = os.path.join(out, k + ".ogg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-16:TP=-3:LRA=11", "-ar", "24000",
                    "-ac", "1", "-c:a", "pcm_s16le", "-f", "wav", dst], check=True)
    os.remove(raw)
    ok = best[0] >= floor(t)
    print("%-18s %.2fs %s%s  «%s»" % (k, best[0], best[2][14:18], "" if ok else "  !! SHORT", t), flush=True)
    return k, ok
if __name__ == "__main__":
    todo = json.load(open(sys.argv[1], encoding="utf-8"))["assets"]["audio_text"]
    with ThreadPoolExecutor(5) as ex: res = list(ex.map(one, [(k, t, sys.argv[2]) for k, t in todo.items()]))
    print("DONE", len(res), "short/failed:", [k for k, ok in res if not ok])
