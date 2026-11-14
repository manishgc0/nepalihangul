#!/usr/bin/env python3
import re
import sys

TARGET_FILE = "/home/manish/projects/nepalihangul/build_bilingual.py"

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New VOCAB_WORDS with all 26 Picture words + Sejong 1A Midterm items
NEW_VOCAB_WORDS = '''const VOCAB_WORDS = [
  // Greetings & Politeness
  { ko: "안녕하세요", ne: "नमस्ते / नमस्कार", en: "Hello / Greetings", pron: "An-nyeong-ha-se-yo", cat: "Greetings", neCat: "अभिवादन", emoji: "👋" },
  { ko: "감사합니다", ne: "धन्यवाद", en: "Thank you", pron: "Kam-sa-ham-ni-da", cat: "Politeness", neCat: "शिष्टाचार", emoji: "🙏" },
  { ko: "죄송합니다", ne: "माफ गर्नुहोस्", en: "Sorry / Excuse me", pron: "Joe-song-ham-ni-da", cat: "Politeness", neCat: "शिष्टाचार", emoji: "😔" },
  { ko: "안녕히 가세요", ne: "राम्रोसँग जानुहोस् (विदाई)", en: "Goodbye (to who is leaving)", pron: "An-nyeong-hi ga-se-yo", cat: "Greetings", neCat: "अभिवादन", emoji: "👋" },
  { ko: "안녕히 계세요", ne: "राम्रोसँग बस्नुहोस् (विदाई)", en: "Goodbye (to who is staying)", pron: "An-nyeong-hi gye-se-yo", cat: "Greetings", neCat: "अभिवादन", emoji: "🏠" },

  // Core 12 Picture Quiz Words (with downloaded WebP images)
  { ko: "공장", ne: "कारखाना", en: "Factory", pron: "Gong-jang", cat: "EPS Work", neCat: "कामकाज", emoji: "🏭", pic: true, image: "images/quiz/factory.webp" },
  { ko: "안전모", ne: "सुरक्षा हेलमेट", en: "Safety helmet", pron: "An-jeon-mo", cat: "Safety", neCat: "सुरक्षा", emoji: "🪖", pic: true, image: "images/quiz/helmet.webp" },
  { ko: "물", ne: "पानी", en: "Water", pron: "Mul", cat: "Daily", neCat: "दैनिक", emoji: "💧", pic: true, image: "images/quiz/water.webp" },
  { ko: "밥", ne: "भात / खाना", en: "Rice / Meal", pron: "Bap", cat: "Dining", neCat: "खानपान", emoji: "🍚", pic: true, image: "images/quiz/rice.webp" },
  { ko: "버스", ne: "बस", en: "Bus", pron: "Beo-seu", cat: "Transport", neCat: "यातायात", emoji: "🚌", pic: true, image: "images/quiz/bus.webp" },
  { ko: "병원", ne: "अस्पताल", en: "Hospital", pron: "Byeong-won", cat: "Health", neCat: "स्वास्थ्य", emoji: "🏥", pic: true, image: "images/quiz/hospital.webp" },
  { ko: "돈", ne: "पैसा", en: "Money", pron: "Don", cat: "Daily", neCat: "दैनिक", emoji: "💰", pic: true, image: "images/quiz/money.webp" },
  { ko: "기계", ne: "मेसिन", en: "Machine", pron: "Gi-gye", cat: "EPS Work", neCat: "कामकाज", emoji: "⚙️", pic: true, image: "images/quiz/machine.webp" },
  { ko: "상자", ne: "बाकस", en: "Box", pron: "Sang-ja", cat: "EPS Work", neCat: "कामकाज", emoji: "📦", pic: true, image: "images/quiz/box.webp" },
  { ko: "트럭", ne: "ट्रक", en: "Truck", pron: "Teu-reok", cat: "Transport", neCat: "यातायात", emoji: "🚚", pic: true, image: "images/quiz/truck.webp" },
  { ko: "약", ne: "औषधि", en: "Medicine", pron: "Yak", cat: "Health", neCat: "स्वास्थ्य", emoji: "💊", pic: true, image: "images/quiz/medicine.webp" },
  { ko: "가방", ne: "झोला", en: "Bag / Backpack", pron: "Ga-bang", cat: "Objects", neCat: "सामानहरू", emoji: "🎒", pic: true, image: "images/quiz/bag.webp" },

  // Sejong 1A Objects & Classroom (with downloaded WebP images)
  { ko: "책상", ne: "टेबुल / डेस्क", en: "Desk", pron: "Chaek-sang", cat: "Objects", neCat: "सामानहरू", emoji: "🛋️", pic: true, image: "images/quiz/desk.webp" },
  { ko: "의자", ne: "कुर्सी", en: "Chair", pron: "Ui-ja", cat: "Objects", neCat: "सामानहरू", emoji: "🪑", pic: true, image: "images/quiz/chair.webp" },
  { ko: "시계", ne: "घडी", en: "Clock / Watch", pron: "Si-gye", cat: "Objects", neCat: "सामानहरू", emoji: "⏰", pic: true, image: "images/quiz/clock.webp" },
  { ko: "핸드폰", ne: "मोबाइल फोन", en: "Cellphone", pron: "Haen-deu-pon", cat: "Objects", neCat: "सामानहरू", emoji: "📱", pic: true, image: "images/quiz/phone.webp" },
  { ko: "연필", ne: "सिसाकलम / पेन्सिल", en: "Pencil", pron: "Yeon-pil", cat: "Objects", neCat: "सामानहरू", emoji: "✏️", pic: true, image: "images/quiz/pencil.webp" },
  { ko: "컴퓨터", ne: "कम्प्युटर", en: "Computer", pron: "Keom-pyu-teo", cat: "Objects", neCat: "सामानहरू", emoji: "💻", pic: true, image: "images/quiz/computer.webp" },
  { ko: "모자", ne: "टोपी / क्याप", en: "Hat / Cap", pron: "Mo-ja", cat: "Objects", neCat: "सामानहरू", emoji: "🧢", pic: true, image: "images/quiz/hat.webp" },
  { ko: "칠판", ne: "कालोपाटी / बोर्ड", en: "Blackboard", pron: "Chil-pan", cat: "Objects", neCat: "सामानहरू", emoji: "📋", pic: true, image: "images/quiz/blackboard.webp" },
  { ko: "사진", ne: "तस्बिर / फोटो", en: "Photograph", pron: "Sa-jin", cat: "Objects", neCat: "सामानहरू", emoji: "🖼️", pic: true, image: "images/quiz/photo.webp" },

  // Sejong 1A Places in the City (with downloaded WebP images)
  { ko: "은행", ne: "बैंक", en: "Bank", pron: "Eun-haeng", cat: "Places", neCat: "ठाउँहरू", emoji: "🏦", pic: true, image: "images/quiz/bank.webp" },
  { ko: "카페", ne: "क्याफे / कफी पसल", en: "Cafe", pron: "Ka-pe", cat: "Places", neCat: "ठाउँहरू", emoji: "☕", pic: true, image: "images/quiz/cafe.webp" },
  { ko: "영화관", ne: "सिनेमा हल", en: "Cinema / Movie theater", pron: "Yeong-hwa-gwan", cat: "Places", neCat: "ठाउँहरू", emoji: "🎬", pic: true, image: "images/quiz/cinema.webp" },
  { ko: "식당", ne: "रेस्टुरेन्ट / भोजनालय", en: "Restaurant", pron: "Sik-dang", cat: "Places", neCat: "ठाउँहरू", emoji: "🍽️", pic: true, image: "images/quiz/restaurant.webp" },
  { ko: "교실", ne: "कक्षाकोठा", en: "Classroom", pron: "Gyo-sil", cat: "Places", neCat: "ठाउँहरू", emoji: "🏫", pic: true, image: "images/quiz/classroom.webp" },
  { ko: "회사", ne: "कम्पनी / अफिस", en: "Company / Office", pron: "Hoe-sa", cat: "Places", neCat: "ठाउँहरू", emoji: "🏢" },
  { ko: "옷 가게", ne: "कपडा पसल", en: "Clothing store", pron: "Ot ga-ge", cat: "Places", neCat: "ठाउँहरू", emoji: "👗" },
  { ko: "백화점", ne: "डिपार्टमेन्ट स्टोर", en: "Department store", pron: "Baek-hwa-jeom", cat: "Places", neCat: "ठाउँहरू", emoji: "🏬" },
  { ko: "집", ne: "घर", en: "House / Home", pron: "Jip", cat: "Places", neCat: "ठाउँहरू", emoji: "🏠" },

  // Sejong 1A Occupations & Identity (Sejong 1과)
  { ko: "학생", ne: "विद्यार्थी", en: "Student", pron: "Hak-saeng", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "🧑‍🎓" },
  { ko: "선생님", ne: "शिक्षक / सर", en: "Teacher", pron: "Seon-saeng-nim", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👨‍🏫" },
  { ko: "회사원", ne: "कर्मचारी / अफिस वर्कर", en: "Office worker", pron: "Hoe-sa-won", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "💼" },
  { ko: "요리사", ne: "कुक / भान्से", en: "Chef / Cook", pron: "Yo-ri-sa", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👨‍🍳" },
  { ko: "가수", ne: "गायक / गायिका", en: "Singer", pron: "Ga-su", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "🎤" },
  { ko: "의사", ne: "डाक्टर", en: "Doctor", pron: "Ui-sa", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "🩺" },
  { ko: "경찰", ne: "प्रहरी / पुलिस", en: "Police officer", pron: "Gyeong-chal", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👮" },
  { ko: "친구", ne: "साथी", en: "Friend", pron: "Chin-gu", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "🤝" },
  { ko: "동생", ne: "भाइ / बहिनी", en: "Younger sibling", pron: "Dong-saeng", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👶" },
  { ko: "형", ne: "दाजु (भाइले भन्ने)", en: "Older brother (for males)", pron: "Hyeong", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👦" },
  { ko: "남자친구", ne: "केटा साथी / प्रेमी", en: "Boyfriend", pron: "Nam-ja-chin-gu", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "💑" },
  { ko: "여자친구", ne: "केटी साथी / प्रेमिका", en: "Girlfriend", pron: "Yeo-ja-chin-gu", cat: "People", neCat: "पेशा र सम्बन्ध", emoji: "👩‍❤️‍👨" },

  // Sejong 1A Countries (Sejong 1과)
  { ko: "네팔", ne: "नेपाल", en: "Nepal", pron: "Ne-pal", cat: "Countries", neCat: "देशहरू", emoji: "🇳🇵" },
  { ko: "한국", ne: "दक्षिण कोरिया", en: "South Korea", pron: "Han-guk", cat: "Countries", neCat: "देशहरू", emoji: "🇰🇷" },
  { ko: "베트남", ne: "भियतनाम", en: "Vietnam", pron: "Be-teu-nam", cat: "Countries", neCat: "देशहरू", emoji: "🇻🇳" },
  { ko: "미국", ne: "अमेरिका", en: "USA", pron: "Mi-guk", cat: "Countries", neCat: "देशहरू", emoji: "🇺🇸" },
  { ko: "일본", ne: "जापान", en: "Japan", pron: "Il-bon", cat: "Countries", neCat: "देशहरू", emoji: "🇯🇵" },
  { ko: "중국", ne: "चीन", en: "China", pron: "Jung-guk", cat: "Countries", neCat: "देशहरू", emoji: "🇨🇳" },
  { ko: "스리랑카", ne: "श्रीलंका", en: "Sri Lanka", pron: "Seu-ri-rang-ka", cat: "Countries", neCat: "देशहरू", emoji: "🇱🇰" },

  // Sejong 1A Spatial Locations (Sejong 3과)
  { ko: "위", ne: "माथि", en: "On / Above", pron: "Wi", cat: "Locations", neCat: "स्थान र दिशा", emoji: "⬆️" },
  { ko: "아래", ne: "तल", en: "Under / Below", pron: "A-rae", cat: "Locations", neCat: "स्थान र दिशा", emoji: "⬇️" },
  { ko: "앞", ne: "अगाडि", en: "In front of", pron: "Ap", cat: "Locations", neCat: "स्थान र दिशा", emoji: "▶️" },
  { ko: "뒤", ne: "पछाडि", en: "Behind", pron: "Dwi", cat: "Locations", neCat: "स्थान र दिशा", emoji: "◀️" },
  { ko: "안", ne: "भित्र", en: "Inside", pron: "An", cat: "Locations", neCat: "स्थान र दिशा", emoji: "📥" },
  { ko: "밖", ne: "बाहिर", en: "Outside", pron: "Bak", cat: "Locations", neCat: "स्थान र दिशा", emoji: "📤" },
  { ko: "옆", ne: "छेउमा", en: "Beside / Next to", pron: "Yeop", cat: "Locations", neCat: "स्थान र दिशा", emoji: "↔️" },
  { ko: "사이", ne: "बीचमा", en: "Between", pron: "Sa-i", cat: "Locations", neCat: "स्थान र दिशा", emoji: "🔄" },

  // Practical EPS & Daily Expressions
  { ko: "작업", ne: "काम / कार्य", en: "Work / Task", pron: "Ja-geop", cat: "EPS Work", neCat: "कामकाज", emoji: "🛠️" },
  { ko: "월급", ne: "मासिक तलब", en: "Monthly salary", pron: "Wol-geup", cat: "EPS Work", neCat: "कामकाज", emoji: "💵" },
  { ko: "물 주세요", ne: "पानी दिनुहोस्", en: "Water, please", pron: "Mul ju-se-yo", cat: "Dining", neCat: "खानपान", emoji: "🥛" },
  { ko: "얼마예요?", ne: "कति रुपैयाँ हो?", en: "How much is it?", pron: "Eol-ma-ye-yo?", cat: "Shopping", neCat: "किनमेल", emoji: "🏷️" },
  { ko: "전화번호가 뭐예요?", ne: "फोन नम्बर कति हो?", en: "What is your phone number?", pron: "Jeon-hwa-beon-ho-ga mwo-ye-yo?", cat: "Daily", neCat: "दैनिक", emoji: "📞" }
];'''

# Replace VOCAB_WORDS in content
vocab_pattern = r"const VOCAB_WORDS = \[\s*[\s\S]*?\n\];"
if re.search(vocab_pattern, content):
    content = re.sub(vocab_pattern, NEW_VOCAB_WORDS, content, count=1)
    print("Replaced VOCAB_WORDS successfully.")
else:
    print("Error: Could not locate VOCAB_WORDS pattern in build_bilingual.py", file=sys.stderr)

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated build_bilingual.py with new VOCAB_WORDS.")
