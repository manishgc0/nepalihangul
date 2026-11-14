#!/usr/bin/env python3
"""Nepali Hangul Audio Server (Port 3090)
Serves static PWA assets and provides /api/tts with authentic Nepali accent support.
"""
import http.server
import socketserver
import urllib.parse
import urllib.request
import hashlib
import os
import sys
import asyncio
import subprocess

PORT = 3090
DIRECTORY = "/home/manish/projects/nepalihangul"
AUDIO_DIR = os.path.join(DIRECTORY, "audio")
YT_AUDIO_DIR = os.path.join(DIRECTORY, "yt_audio")
NEPALI_CACHE_DIR = os.path.join(AUDIO_DIR, "nepali_cache")
KO_CACHE_DIR = os.path.join(AUDIO_DIR, "ko_cache")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(YT_AUDIO_DIR, exist_ok=True)
os.makedirs(NEPALI_CACHE_DIR, exist_ok=True)
os.makedirs(KO_CACHE_DIR, exist_ok=True)

# ---------------------------------------------------- Hangul to Nepali Phonetics
CI = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
VI = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
FI = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

CI_NE = {
    "ㄱ": "ख", "ㄲ": "क", "ㄴ": "न", "ㄷ": "थ", "ㄸ": "त",
    "ㄹ": "र", "ㅁ": "म", "ㅂ": "फ", "ㅃ": "प", "ㅅ": "स",
    "ㅆ": "स", "ㅇ": "",   "ㅈ": "छ", "ㅉ": "च", "ㅊ": "छ",
    "ㅋ": "ख", "ㅌ": "थ", "ㅍ": "फ", "ㅎ": "ह"
}
CI_MID_NE = {
    "ㄱ": "ग", "ㄲ": "क", "ㄴ": "न", "ㄷ": "द", "ㄸ": "त",
    "ㄹ": "र", "ㅁ": "म", "ㅂ": "ब", "ㅃ": "प", "ㅅ": "स",
    "ㅆ": "स", "ㅇ": "",   "ㅈ": "ज", "ㅉ": "च", "ㅊ": "छ",
    "ㅋ": "ख", "ㅌ": "थ", "ㅍ": "फ", "ㅎ": "ह"
}
VOWEL_INDEP = {
    "ㅏ": "आ", "ㅐ": "ए", "ㅑ": "या", "ㅒ": "ये", "ㅓ": "अ", "ㅔ": "ए",
    "ㅕ": "य", "ㅖ": "ये", "ㅗ": "ओ", "ㅘ": "वा", "ㅙ": "वे", "ㅚ": "वे",
    "ㅛ": "यो", "ㅜ": "उ", "ㅝ": "व", "ㅞ": "वे", "ㅟ": "वि", "ㅠ": "यु",
    "ㅡ": "उ", "ㅢ": "उइ", "ㅣ": "इ"
}
VOWEL_DEP = {
    "ㅏ": "ा", "ㅐ": "े", "ㅑ": "्या", "ㅒ": "्ये", "ㅓ": "", "ㅔ": "े",
    "ㅕ": "्य", "ㅖ": "्ये", "ㅗ": "ो", "ㅘ": "्वा", "ㅙ": "्वे", "ㅚ": "्वे",
    "ㅛ": "्यो", "ㅜ": "ु", "ㅝ": "्व", "ㅞ": "्वे", "ㅟ": "्वि", "ㅠ": "्यु",
    "ㅡ": "ु", "ㅢ": "ुइ", "ㅣ": "ि"
}
FI_NE = {
    "": "", "ㄱ": "क्", "ㄲ": "क्", "ㄳ": "क्", "ㄴ": "न्", "ㄵ": "न्",
    "ㄶ": "न्", "ㄷ": "त्", "ㄹ": "ल्", "ㄺ": "क्", "ㄻ": "म्", "ㄼ": "ल्",
    "ㄽ": "ल्", "ㄾ": "ल्", "ㄿ": "प्", "ㅀ": "ल्", "ㅁ": "म्", "ㅂ": "प्",
    "ㅄ": "प्", "ㅅ": "त्", "ㅆ": "त्", "ㅇ": "ङ्", "ㅈ": "त्", "ㅊ": "त्",
    "ㅋ": "क्", "ㅌ": "त्", "ㅍ": "प्", "ㅎ": "त्"
}

JAMO_NE = {
    "ㅏ": "आ", "ㅑ": "या", "ㅓ": "अ", "ㅕ": "य", "ㅗ": "ओ", "ㅛ": "यो",
    "ㅜ": "उ", "ㅠ": "यु", "ㅡ": "उ", "ㅣ": "इ", "ㅐ": "ए", "ㅒ": "ये",
    "ㅔ": "ए", "ㅖ": "ये", "ㅘ": "वा", "ㅙ": "वे", "ㅚ": "वे", "ㅝ": "व",
    "ㅞ": "वे", "ㅟ": "वि", "ㅢ": "उइ",
    "ㄱ": "ख", "ㄴ": "न", "ㄷ": "थ", "ㄹ": "र", "ㅁ": "म", "ㅂ": "फ",
    "ㅅ": "स", "ㅇ": "ङ", "ㅈ": "छ", "ㅊ": "छ", "ㅋ": "ख", "ㅌ": "थ",
    "ㅍ": "फ", "ㅎ": "ह", "ㄲ": "क", "ㄸ": "त", "ㅃ": "प", "ㅆ": "स", "ㅉ": "च"
}

def hangul_to_nepali(txt):
    txt = txt.strip()
    if txt in JAMO_NE:
        return JAMO_NE[txt]
    words = txt.split(" ")
    out_words = []
    for word in words:
        w_res = []
        for j, ch in enumerate(word):
            code = ord(ch)
            if 0xAC00 <= code <= 0xD7A3:
                s_idx = code - 0xAC00
                c = CI[s_idx // 588]
                v = VI[(s_idx % 588) // 28]
                f = FI[s_idx % 28]
                c_map = CI_NE if j == 0 else CI_MID_NE
                c_sound = c_map[c]
                if c == "ㅇ":
                    syl_str = VOWEL_INDEP[v]
                else:
                    syl_str = c_sound + VOWEL_DEP[v]
                syl_str += FI_NE[f]
                w_res.append(syl_str)
            elif ch in JAMO_NE:
                w_res.append(JAMO_NE[ch])
            else:
                w_res.append(ch)
        out_words.append("".join(w_res))
    return " ".join(out_words)

def slug(txt):
    return "-".join("%x" % ord(ch) for ch in txt)

async def synthesize_edge(text, voice, out_path):
    import edge_tts
    comm = edge_tts.Communicate(text, voice)
    await comm.save(out_path)

def generate_nepali_audio(q, out_file):
    ne_text = hangul_to_nepali(q)
    # 1. Try edge-tts with Sagar (Nepali Neural voice)
    try:
        tmp_raw = out_file + ".tmp.mp3"
        asyncio.run(synthesize_edge(ne_text, "ne-NP-SagarNeural", tmp_raw))
        if os.path.exists(tmp_raw) and os.path.getsize(tmp_raw) > 500:
            # Normalize with ffmpeg
            af = (
                "silenceremove=start_periods=1:start_silence=0.01:start_threshold=-40dB,"
                "areverse,"
                "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-40dB,"
                "areverse,"
                "volume=2dB,adelay=30|30"
            )
            subprocess.run([
                "ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", tmp_raw,
                "-af", af, "-ac", "1", "-ar", "24000", "-codec:a", "libmp3lame", "-b:a", "48k", out_file
            ], check=True)
            try: os.remove(tmp_raw)
            except: pass
            return "Edge-Nepali-Sagar"
    except Exception as e:
        print(f"Edge-TTS Nepali error for '{q}' ({ne_text}): {e}", file=sys.stderr)

    # 2. Fallback to Google Translate TTS with Nepali locale (tl=ne)
    try:
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ne&client=tw-ob&q={urllib.parse.quote(ne_text)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://translate.google.com/"
        })
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = resp.read()
            if len(data) > 300:
                with open(out_file, "wb") as f:
                    f.write(data)
                return "Google-Nepali"
    except Exception as e:
        print(f"Google TTS Nepali error for '{q}': {e}", file=sys.stderr)

    return None

def generate_korean_audio(q, out_file):
    try:
        tmp_raw = out_file + ".tmp.mp3"
        asyncio.run(synthesize_edge(q, "ko-KR-SunHiNeural", tmp_raw))
        if os.path.exists(tmp_raw) and os.path.getsize(tmp_raw) > 500:
            subprocess.run([
                "ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", tmp_raw,
                "-ac", "1", "-ar", "24000", "-codec:a", "libmp3lame", "-b:a", "48k", out_file
            ], check=True)
            try: os.remove(tmp_raw)
            except: pass
            return "Edge-Korean-SunHi"
    except Exception as e:
        pass

    try:
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ko&client=tw-ob&q={urllib.parse.quote(q)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://translate.google.com/"
        })
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = resp.read()
            if len(data) > 300:
                with open(out_file, "wb") as f:
                    f.write(data)
                return "Google-Korean"
    except Exception as e:
        pass
    return None

class KoreanTtsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def handle_tts(self, is_head=False):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        q = query.get("q", [""])[0].strip()
        accent = query.get("accent", ["ne"])[0].strip().lower()

        if not q:
            self.send_error(400, "Missing 'q' parameter")
            return

        h = hashlib.md5(q.encode("utf-8")).hexdigest()
        sl = slug(q)
        audio_data = None
        source_type = "unknown"

        if accent == "ne":
            # Priority 1: pre-baked Nepali lib clip
            lib_ne_file = os.path.join(AUDIO_DIR, "lib_ne", f"{sl}.mp3")
            cache_file = os.path.join(NEPALI_CACHE_DIR, f"{h}.mp3")
            yt_file = os.path.join(YT_AUDIO_DIR, f"{h}.mp3")

            if os.path.exists(lib_ne_file) and os.path.getsize(lib_ne_file) > 1000:
                with open(lib_ne_file, "rb") as f:
                    audio_data = f.read()
                source_type = "Baked-Nepali-Accent"
            elif os.path.exists(cache_file) and os.path.getsize(cache_file) > 1000:
                with open(cache_file, "rb") as f:
                    audio_data = f.read()
                source_type = "Cache-Nepali"
            elif os.path.exists(yt_file) and os.path.getsize(yt_file) > 1000:
                with open(yt_file, "rb") as f:
                    audio_data = f.read()
                source_type = "YouTube-Teabreak"
            else:
                src = generate_nepali_audio(q, cache_file)
                if src and os.path.exists(cache_file):
                    with open(cache_file, "rb") as f:
                        audio_data = f.read()
                    source_type = src
        else:
            # Korean Native Voice
            lib_ko_file = os.path.join(AUDIO_DIR, "lib_ko", f"{sl}.mp3")
            cache_file = os.path.join(KO_CACHE_DIR, f"{h}.mp3")

            if os.path.exists(lib_ko_file) and os.path.getsize(lib_ko_file) > 1000:
                with open(lib_ko_file, "rb") as f:
                    audio_data = f.read()
                source_type = "Baked-Korean-Native"
            elif os.path.exists(cache_file) and os.path.getsize(cache_file) > 1000:
                with open(cache_file, "rb") as f:
                    audio_data = f.read()
                source_type = "Cache-Korean"
            else:
                src = generate_korean_audio(q, cache_file)
                if src and os.path.exists(cache_file):
                    with open(cache_file, "rb") as f:
                        audio_data = f.read()
                    source_type = src

        if audio_data and len(audio_data) > 200:
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(audio_data)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Audio-Source", source_type)
            self.send_header("X-Audio-Accent", accent)
            self.end_headers()
            if not is_head:
                self.wfile.write(audio_data)
            return
        else:
            self.send_error(502, "Failed to retrieve audio")
            return

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/tts":
            return self.handle_tts(is_head=True)
        return super().do_HEAD()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/tts":
            return self.handle_tts(is_head=False)
        return super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), KoreanTtsHandler) as httpd:
        print(f"Nepali Hangul server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
