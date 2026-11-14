#!/usr/bin/env python3
import os
import sys
import time
import hashlib
import urllib.request
import urllib.parse

AUDIO_DIR = "/home/manish/projects/nepalihangul/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# List of all essential Korean learning texts
VOWELS_BASIC = ["아", "야", "어", "여", "오", "요", "우", "유", "으", "이"]
VOWELS_COMPOUND = ["애", "얘", "에", "예", "와", "왜", "외", "워", "웨", "위", "의"]
CONSONANTS_SYL = ["가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "타", "파", "하"]
CONSONANTS_DOUBLE = ["까", "따", "빠", "싸", "짜"]
CONSONANT_NAMES = [
    "기역", "니은", "디귿", "리을", "미음", "비읍", "시옷", "이응", "지읒", "치읓", "키읔", "티읕", "피읖", "히읗",
    "쌍기역", "쌍디귿", "쌍비읍", "쌍시옷", "쌍지읒"
]
BATCHIM_EXAMPLES = ["각", "간", "갇", "갈", "감", "갑", "강", "밥", "옷", "꽃", "빛", "낮", "잎", "닭", "삶", "값", "앉다"]
READING_RULES = ["한국어", "같이", "국물", "독립", "십육", "신라", "옷이", "감사합니다", "어떻게", "학문", "난로"]
NUM_SINO = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구", "십", "백", "천", "만"]
NUM_NATIVE = ["하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "열", "스물"]
VOCAB = [
    "안녕하세요", "감사합니다", "죄송합니다", "네", "아니요", "괜찮아요", "안녕히 가세요", "안녕히 계세요",
    "물", "밥", "김치", "고기", "빵", "우유", "커피", "차",
    "시장", "가게", "회사", "공장", "병원", "약국", "집", "방", "화장실", "식당",
    "사람", "친구", "선생님", "의사", "가족", "아버지", "어머니", "동생",
    "오늘", "내일", "어제", "지금", "시간", "돈", "일", "공부", "한국", "네팔"
]

ALL_TEXTS = sorted(list(set(
    VOWELS_BASIC + VOWELS_COMPOUND + CONSONANTS_SYL + CONSONANTS_DOUBLE +
    CONSONANT_NAMES + BATCHIM_EXAMPLES + READING_RULES + NUM_SINO + NUM_NATIVE + VOCAB
)))

def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def fetch_tts(text):
    h = get_hash(text)
    dest = os.path.join(AUDIO_DIR, f"{h}.mp3")
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        return True
    
    q = urllib.parse.quote(text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ko&client=tw-ob&q={q}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://translate.google.com/"
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(dest, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"Error fetching '{text}': {e}", file=sys.stderr)
        return False

print(f"Starting pre-caching of {len(ALL_TEXTS)} Korean audio phrases...")
success = 0
for i, txt in enumerate(ALL_TEXTS):
    if fetch_tts(txt):
        success += 1
    time.sleep(0.08) # polite throttle

print(f"Finished! Successfully cached {success}/{len(ALL_TEXTS)} audio files in {AUDIO_DIR}")
