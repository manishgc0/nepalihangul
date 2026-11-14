#!/usr/bin/env python3
"""Bake the app's speakable Korean into audio/lib/ so nothing needs a server.

Why this exists
---------------
`say()` used to route every word and sentence through `/api/tts`, a Python
endpoint in server.py. Open index.html straight off disk — `file://` — and that
endpoint does not exist, so every syllable past the 40 letter clips went silent
and fell through to whatever `speechSynthesis` happened to have installed.

The set of strings the app can speak is finite and known at build time: 140
syllables from the assembly grid, 980 batchim combinations, and ~200 curated
words, phrases and sentences. So they get synthesised once, here, and shipped as
static files. `say()` tries `audio/lib/<slug>.mp3` first; only genuinely
unbounded input (the writing studio, user-typed text) still reaches the server.

Slug scheme
-----------
Every codepoint in hex, joined by '-'. `각` -> ac01.mp3, `한국어` ->
d55c-ad6d-c5b4.mp3. Deterministic, so the browser computes the same name with no
lookup table and no index to download — which matters, because `fetch()` of a
local JSON is blocked on file://.

Usage
-----
    python3 gen_audio.py              # fetch what is missing, then encode
    python3 gen_audio.py --force      # refetch everything
    python3 gen_audio.py --list       # print the target set and exit
    python3 gen_audio.py --source edge  # offline fallback voice

Source endpoint and auth are the same as gen_pron.py — Bunpo's Cloud Run TTS
with a Firebase anonymous token. See that file for the RE notes.
"""
import argparse
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "audio", "lib")
RAW = os.path.join(BASE, "audio", "lib_raw")
SPOKEN = "/tmp/opencode/spoken.json"

BUNPO_TTS = "https://bunpo-basic-283414158288.us-central1.run.app/v3/text_to_speech"
FIREBASE_KEY = "AIzaSyAxg8aXqILmTAN_OOAGIRt0IL6nkQyj3p8"
FIREBASE_SIGNUP = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FIREBASE_KEY

EDGE_VOICE = "ko-KR-SunHiNeural"

# ---------------------------------------------------------------- jamo tables
CI = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
VI = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
FI = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

CONS_BASIC = ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
VOWELS_BASIC = ["ㅏ","ㅑ","ㅓ","ㅕ","ㅗ","ㅛ","ㅜ","ㅠ","ㅡ","ㅣ"]
FINALS = ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅇ"]          # the 7 terminal batchim
VOWELS_COMPOUND = ["ㅐ","ㅒ","ㅔ","ㅖ","ㅘ","ㅙ","ㅚ","ㅝ","ㅞ","ㅟ","ㅢ"]

JAMO_SPOKEN = {
    "ㅏ":"아","ㅑ":"야","ㅓ":"어","ㅕ":"여","ㅗ":"오","ㅛ":"요","ㅜ":"우","ㅠ":"유","ㅡ":"으","ㅣ":"이",
    "ㅐ":"애","ㅒ":"얘","ㅔ":"에","ㅖ":"예","ㅘ":"와","ㅙ":"왜","ㅚ":"외","ㅝ":"워","ㅞ":"웨","ㅟ":"위","ㅢ":"의",
    "ㄱ":"가","ㄴ":"나","ㄷ":"다","ㄹ":"라","ㅁ":"마","ㅂ":"바","ㅅ":"사","ㅇ":"아","ㅈ":"자","ㅊ":"차",
    "ㅋ":"카","ㅌ":"타","ㅍ":"파","ㅎ":"하",
    "ㄲ":"까","ㄸ":"따","ㅃ":"빠","ㅆ":"싸","ㅉ":"짜",
}


def syl(c, v):
    return chr(0xAC00 + (CI.index(c) * 21 + VI.index(v)) * 28)


def syl3(c, v, f):
    return chr(0xAC00 + (CI.index(c) * 21 + VI.index(v)) * 28 + FI.index(f))


def normalize(txt):
    """Mirror normalizeKorean() in the app exactly."""
    txt = str(txt).strip()
    if txt in JAMO_SPOKEN:
        return JAMO_SPOKEN[txt]
    if len(txt) >= 2 and txt[0] in CI and txt[1] in VI:
        if len(txt) == 2:
            return syl(txt[0], txt[1])
        if txt[2] in FI:
            return syl3(txt[0], txt[1], txt[2])
    return txt


def slug(txt):
    return "-".join("%x" % ord(ch) for ch in txt)


# ---------------------------------------------------------------- target set
HANGUL = re.compile(r"[\uAC00-\uD7A3]")
DEVANAGARI = re.compile(r"[\u0900-\u097F]")


def scrape_source():
    """Data-driven strings that the runtime harvest can miss (quiz answers,
    lesson audio fields, sample lists, and any literal say('…') call)."""
    src = open(os.path.join(BASE, "build_bilingual.py"), encoding="utf-8").read()
    found = set()
    for pat in (r'audio:\s*"([^"]{1,60})"', r'audioPrompt:\s*"([^"]{1,60})"',
                r'answer:\s*"([^"]{1,60})"',
                r'ko:\s*"([^"]{1,60})"', r'word:\s*"([^"]{1,60})"',
                r'npcKo:\s*"([^"]{1,90})"', r'goalKo:\s*"([^"]{1,90})"',
                r'samples:\s*\[([^\]]{1,400})\]'):
        for m in re.finditer(pat, src):
            chunk = m.group(1)
            for piece in re.findall(r'"([^"]{1,60})"', chunk) or [chunk]:
                if HANGUL.search(piece) and not DEVANAGARI.search(piece):
                    found.add(piece)
    # literal say('…') / sayPron('…') arguments, including template-free ones
    for m in re.finditer(r"""say(?:Pron)?\(\s*['"]([^'"\\\n]{1,80})['"]""", src):
        piece = m.group(1)
        if HANGUL.search(piece) and not DEVANAGARI.search(piece) and "$" not in piece:
            found.add(piece)
    # [ "한글", "gloss" ] pairs — every vocabulary table in the app is this shape,
    # including SEJONG_1A's words. Without this rule a whole unit's vocabulary
    # ships silent: no clip, /api/tts absent on a static server, and a Linux
    # speechSynthesis with no Korean voice, which reads to the user as "no sound".
    # The trailing bracket is deliberately not required, so the three-field rows
    # in the books reference (hangul, devanagari, meaning) are caught as well.
    for m in re.finditer(r'\[\s*"([\uAC00-\uD7A3][^"]{0,40})"\s*,\s*"', src):
        found.add(m.group(1))
    # the counter tables name their unit in a field rather than an array, and a
    # learner taps the unit itself to hear what 시 or 그릇 sounds like alone
    for m in re.finditer(r'unit:\s*"([\uAC00-\uD7A3][^"]{0,20})"', src):
        found.add(m.group(1))
    return found


def build_targets():
    t = set()
    for c in CONS_BASIC:
        for v in VOWELS_BASIC:
            t.add(syl(c, v))                                   # step 3: 140
            for f in FINALS:
                t.add(syl3(c, v, f))                           # step 4: 980

    # The books screen lets a learner compose any consonant against any vowel,
    # including the tense consonants and the compound vowels, so those blocks
    # have to be baked too — 19 x 21 = 399 rather than the 140 the assembly
    # grid shows. A composer whose result is silent is worse than no composer.
    for c in CONS_BASIC + ["ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]:
        for v in VOWELS_BASIC + VOWELS_COMPOUND:
            t.add(syl(c, v))

    if os.path.exists(SPOKEN):
        for s in json.load(open(SPOKEN, encoding="utf-8")):
            t.add(s)

    t |= scrape_source()

    # normalise, drop empties and anything that is not actually Korean text
    out = set()
    for s in t:
        n = normalize(s)
        if n and HANGUL.search(n) and len(n) <= 80:
            out.add(n)
    return out


# ---------------------------------------------------------------- fetching
def token():
    body = json.dumps({"returnSecureToken": True}).encode()
    req = urllib.request.Request(FIREBASE_SIGNUP, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["idToken"]


def fetch_one(tok, txt):
    body = json.dumps({"language": "ko", "model": "standard",
                       "text": txt, "voiceName": ""}).encode()
    req = urllib.request.Request(BUNPO_TTS, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tok,
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_all(texts, force):
    todo = [t for t in sorted(texts)
            if force or not (os.path.exists(os.path.join(RAW, slug(t) + ".wav"))
                             and os.path.getsize(os.path.join(RAW, slug(t) + ".wav")) > 2000)]
    if not todo:
        print("bunpo: all %d clips already cached" % len(texts))
        return
    print("bunpo: %d to fetch (%d cached)" % (len(todo), len(texts) - len(todo)))
    tok = token()
    done = [0]

    def work(t):
        try:
            data = fetch_one(tok, t)
        except urllib.error.HTTPError as e:
            print("  !! %-14s %s %s" % (t, e.code, e.read()[:120]))
            return
        except Exception as e:
            print("  !! %-14s %s" % (t, repr(e)[:100]))
            return
        with open(os.path.join(RAW, slug(t) + ".wav"), "wb") as f:
            f.write(data)
        done[0] += 1
        if done[0] % 50 == 0:
            print("  %4d/%d" % (done[0], len(todo)))

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(work, todo))
    print("  %d fetched, %d failed" % (done[0], len(todo) - done[0]))


def fetch_edge(texts, force):
    try:
        import edge_tts
    except ImportError:
        raise SystemExit("edge-tts missing — pip install --target=<dir> edge-tts")

    todo = [t for t in sorted(texts)
            if force or not os.path.exists(os.path.join(RAW, slug(t) + ".wav"))]

    async def run():
        for t in todo:
            mp3 = os.path.join(RAW, slug(t) + ".mp3")
            wav = os.path.join(RAW, slug(t) + ".wav")
            await edge_tts.Communicate(t, EDGE_VOICE).save(mp3)
            subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
                            "-i", mp3, "-ar", "24000", "-ac", "1", wav], check=True)
            os.remove(mp3)

    asyncio.run(run())


# ---------------------------------------------------------------- encoding
def peak_dbfs(path):
    # No -v error here: astats reports on stderr at info level, so suppressing it
    # makes this function always return the fallback and gain every clip by +7 dB.
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                        "-af", "astats=metadata=1:reset=0", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Peak level dB" in line:
            try:
                return float(line.split(":")[-1].strip())
            except ValueError:
                pass
    return -10.0


def encode(txt):
    src = os.path.join(RAW, slug(txt) + ".wav")
    dst = os.path.join(OUT, slug(txt) + ".mp3")
    # Normalise to -3 dBFS peak in both directions. Bunpo's raw WAVs arrive hot
    # (many already near 0 dBFS) and MP3 encoding overshoots on top of that, so
    # clamping gain at zero left 485 clips clipping at up to +6 dBFS — audible as
    # grit on the plosives. Attenuating fixes it.
    gain = -3.0 - peak_dbfs(src)
    af = ("silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,"
          "areverse,"
          "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB,"
          "areverse,"
          "volume=%.2fdB,"
          "adelay=30|30" % gain)
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", src,
                    "-af", af, "-ac", "1", "-ar", "24000",
                    "-codec:a", "libmp3lame", "-b:a", "48k", dst], check=True)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=("bunpo", "edge"), default="bunpo")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="exit non-zero if any string the app can speak has no clip")
    args = ap.parse_args()

    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    texts = build_targets()
    print("target set: %d distinct strings" % len(texts))
    if args.list:
        for t in sorted(texts):
            print("  %-30s %s" % (t, slug(t)))
        return

    # Verify runs against audio/lib/, not the raw cache: the raw WAV being
    # present proves nothing about whether the MP3 the browser asks for exists.
    if args.verify:
        gap = [t for t in sorted(texts)
               if not os.path.exists(os.path.join(OUT, slug(t) + ".mp3"))]
        if gap:
            print("MISSING %d clips — these will fall through to /api/tts and go silent:" % len(gap))
            for t in gap[:40]:
                print("  %-30s %s.mp3" % (t, slug(t)))
            if len(gap) > 40:
                print("  … and %d more" % (len(gap) - 40))
            sys.exit(1)
        print("OK — all %d strings have a clip" % len(texts))
        return

    if args.source == "bunpo":
        fetch_all(texts, args.force)
    else:
        fetch_edge(texts, args.force)

    rows = []
    missing = 0
    for i, t in enumerate(sorted(texts), 1):
        src = os.path.join(RAW, slug(t) + ".wav")
        if not os.path.exists(src):
            missing += 1
            continue
        dst = encode(t)
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip()
        rows.append({"text": t, "file": os.path.basename(dst), "duration": round(float(dur), 3)})
        if i % 100 == 0:
            print("  encoded %d/%d" % (i, len(texts)))

    total = sum(os.path.getsize(os.path.join(OUT, r["file"])) for r in rows)
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"source": args.source, "count": len(rows),
                   "slug": "hex codepoints joined by '-'",
                   "clips": rows}, f, ensure_ascii=False, indent=0)

    print("\n%d clips, %.2f MB%s" % (len(rows), total / 1048576,
                                     (", %d missing" % missing) if missing else ""))


main()
