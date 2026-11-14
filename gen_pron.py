#!/usr/bin/env python3
"""Generate the letter-pronunciation clips in audio/pron/.

Two sources:

  --source bunpo  (default)  the real thing: Bunpo's own server-side TTS.
                             POST https://bunpo-basic-283414158288.us-central1.run.app/v3/text_to_speech
                             with a Firebase anonymous ID token. Returns audio/pcm (WAV).
  --source edge              offline fallback: ko-KR-SunHiNeural via edge-tts.

Every Hangul letter is spoken as its canonical example syllable — ㅏ as 아, ㄱ as
가 — because that is how a letter is pronounced in isolation. A bare jamo (ㅏ,
U+314F) is not speakable text, and "ㄱㅏ" is not valid Hangul at all.

How the Bunpo endpoint was found (com.bunpoapp 3.28.0):
  Lc8/g0;->a()  -> "https://bunpo-basic-283414158288.us-central1.run.app/"
  Lc8/g0;->d()  -> a() + "v3/"                        (the API prefix)
  Lc8/p;->u()   -> POST "text_to_speech" with TextToSpeechRequest(language, model, text, voiceName)
                   and reads the response as byte[]  -> raw WAV
  Lc8/P;->t()   -> FirebaseAuth.signInAnonymously()   (no account needed)
  model must be 'standard' or 'gemini'; 'standard' is the crisp single syllable
  (0.23s of speech), 'gemini' is only used by the live roleplay voice. voiceName
  is accepted and ignored by the service.

Usage:
    python3 gen_pron.py                 # fetch from Bunpo, then encode
    python3 gen_pron.py --force         # ignore cached raw WAVs
    python3 gen_pron.py --source edge   # offline fallback

edge-tts, when needed:  pip install --target=<dir> edge-tts
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "audio", "pron")
RAW = os.path.join(BASE, "audio", "pron_raw")

# Bunpo's TTS backend (extracted from com.bunpoapp 3.28.0, see the module docstring).
BUNPO_HOST = "https://bunpo-basic-283414158288.us-central1.run.app"
BUNPO_TTS = BUNPO_HOST + "/v3/text_to_speech"
FIREBASE_KEY = "AIzaSyAxg8aXqILmTAN_OOAGIRt0IL6nkQyj3p8"   # public client key from the APK
FIREBASE_SIGNUP = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FIREBASE_KEY

EDGE_VOICE = "ko-KR-SunHiNeural"
EDGE_RATE = "-15%"

# slug -> the syllable that is actually spoken
VOWELS = [
    ("a", "아"), ("ya", "야"), ("eo", "어"), ("yeo", "여"), ("o", "오"),
    ("yo", "요"), ("u", "우"), ("yu", "유"), ("eu", "으"), ("i", "이"),
    ("ae", "애"), ("yae", "얘"), ("e", "에"), ("ye", "예"), ("wa", "와"),
    ("wae", "왜"), ("oe", "외"), ("wo", "워"), ("we", "웨"), ("wi", "위"),
    ("ui", "의"),
]

# ㅇ has no sound of its own — it takes the vowel's syllable, so it is 아.
CONSONANTS = [
    ("g", "가"), ("n", "나"), ("d", "다"), ("r", "라"), ("m", "마"),
    ("b", "바"), ("s", "사"), ("ng", "아"), ("j", "자"), ("ch", "차"),
    ("k", "카"), ("t", "타"), ("p", "파"), ("h", "하"),
    ("kk", "까"), ("tt", "따"), ("pp", "빠"), ("ss", "싸"), ("jj", "짜"),
]

ALL = VOWELS + CONSONANTS


# ---------------------------------------------------------------- bunpo source

def bunpo_token():
    body = json.dumps({"returnSecureToken": True}).encode()
    req = urllib.request.Request(
        FIREBASE_SIGNUP, data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    tok = payload.get("idToken")
    if not tok:
        raise SystemExit("Firebase anonymous sign-in returned no idToken: %r" % payload)
    return tok


def bunpo_fetch(token, syllable):
    body = json.dumps({
        "language": "ko",
        "model": "standard",
        "text": syllable,
        "voiceName": "",
    }).encode()
    req = urllib.request.Request(
        BUNPO_TTS, data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def bunpo_all(slugs, force):
    todo = [s for s, _ in slugs
            if force or not (os.path.exists(os.path.join(RAW, s + ".wav"))
                             and os.path.getsize(os.path.join(RAW, s + ".wav")) > 4000)]
    if not todo:
        print("bunpo: all %d raw clips already cached" % len(slugs))
        return
    print("bunpo: signing in anonymously...")
    token = bunpo_token()
    print("bunpo: fetching %d clips" % len(todo))
    by_slug = dict(slugs)
    for i, slug in enumerate(todo, 1):
        try:
            data = bunpo_fetch(token, by_slug[slug])
        except urllib.error.HTTPError as e:
            raise SystemExit("bunpo %s failed: %s %s" % (slug, e.code, e.read()[:200]))
        with open(os.path.join(RAW, slug + ".wav"), "wb") as f:
            f.write(data)
        print("  [%2d/%2d] %-4s %-3s %6d B" % (i, len(todo), slug, by_slug[slug], len(data)))


# ----------------------------------------------------------------- edge source

def edge_all(slugs, force):
    try:
        import edge_tts
    except ImportError:
        raise SystemExit("edge-tts missing — pip install --target=<dir> edge-tts")

    async def run():
        for slug, syllable in slugs:
            out = os.path.join(RAW, slug + ".mp3")
            if not force and os.path.exists(out) and os.path.getsize(out) > 2000:
                continue
            await edge_tts.Communicate(syllable, EDGE_VOICE, rate=EDGE_RATE).save(out)

    asyncio.run(run())
    # normalise to the same raw name the encoder expects
    for slug, _ in slugs:
        mp3 = os.path.join(RAW, slug + ".mp3")
        wav = os.path.join(RAW, slug + ".wav")
        if os.path.exists(mp3):
            subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", mp3, wav], check=True)
            os.remove(mp3)


# ---------------------------------------------------------------------- encode

def peak_dbfs(path):
    # astats reports on stderr at info level; -v error hides it and this function
    # then always returns the fallback, gain-ing every clip by +7 dB.
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "astats=metadata=1:reset=0",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r.stderr.splitlines():
        if "Peak level dB" in line:
            try:
                return float(line.split(":")[-1].strip())
            except ValueError:
                pass
    return -10.0


def trim_and_encode(slug):
    src = os.path.join(RAW, slug + ".wav")
    dst = os.path.join(OUT, slug + ".mp3")
    gain = -3.0 - peak_dbfs(src)             # normalise to -3 dBFS peak, both directions
    af = (
        "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,"
        "areverse,"
        "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB,"
        "areverse,"
        f"volume={gain:.2f}dB,"
        "adelay=40|40"
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", src,
         "-af", af, "-ac", "1", "-ar", "44100",
         "-codec:a", "libmp3lame", "-b:a", "96k", dst],
        check=True,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=("bunpo", "edge"), default="bunpo")
    ap.add_argument("--force", action="store_true", help="re-fetch even if cached")
    args = ap.parse_args()

    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    if args.source == "bunpo":
        bunpo_all(ALL, args.force)
    else:
        edge_all(ALL, args.force)

    rows = []
    for slug, syllable in ALL:
        trim_and_encode(slug)
        dur, size = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
             "-of", "csv=p=0", os.path.join(OUT, slug + ".mp3")],
            capture_output=True, text=True,
        ).stdout.strip().split(",")
        rows.append((slug, syllable, float(dur), int(size)))

    for slug, syllable, dur, size in rows:
        print(f"{slug:<6} {syllable}  {dur:.3f}s  {size:>6}B")
    print(f"\n{len(rows)} clips, {sum(r[3] for r in rows) / 1024:.1f} KB total  (source: {args.source})")

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({
            "source": args.source,
            "voice": EDGE_VOICE if args.source == "edge" else "bunpo/v3/text_to_speech (model=standard)",
            "clips": {s: {"syllable": y, "duration": round(d, 3)} for s, y, d, _ in rows},
        }, f, ensure_ascii=False, indent=1)
    print("manifest -> audio/pron/manifest.json")


main()
