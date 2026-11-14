# चित्र क्विज तस्बिरहरू / Picture Quiz Images

यो फोल्डरमा राखिएका तस्बिरहरू **चित्र शब्द परीक्षा** (Picture Word Quiz) मा
प्रयोग हुन्छन्। तस्बिर नभएसम्म क्विजले इमोजी र "तस्बिर थपिन बाँकी" सन्देश
देखाउँछ, त्यसैले साइट नबिग्रिकन चल्छ।

This folder holds the images used by the **Picture Word Quiz**. Until an image
exists, the quiz shows an emoji placeholder and an "Image coming soon" note, so
the site keeps working with no images.

---

## आवश्यक फाइल नामहरू / Required file names

Exactly these 12 file names, all inside `images/quiz/`:

| File name | Korean word | Nepali meaning | English meaning |
|---|---|---|---|
| `factory.webp` | 공장 | कारखाना | Factory |
| `helmet.webp` | 안전모 | सुरक्षा हेलमेट | Safety helmet |
| `water.webp` | 물 | पानी | Water |
| `rice.webp` | 밥 | भात / खाना | Rice / Meal |
| `bus.webp` | 버스 | बस | Bus |
| `hospital.webp` | 병원 | अस्पताल | Hospital |
| `money.webp` | 돈 | पैसा | Money |
| `machine.webp` | 기계 | मेसिन | Machine |
| `box.webp` | 상자 | बाकस | Box |
| `truck.webp` | 트럭 | ट्रक | Truck |
| `medicine.webp` | 약 | औषधि | Medicine |
| `bag.webp` | 가방 | झोला | Bag |

`.webp` नचाहिने भए `.png` वा `.jpg` पनि चल्छ — तर त्यसो गर्दा
`build_bilingual.py` भित्रको `VOCAB_WORDS` मा भएको `image:` बाटो पनि
त्यही एक्सटेन्सनमा फेर्नुपर्छ।

`.png` or `.jpg` also work, but if you use another extension you must also change
the matching `image:` path in `VOCAB_WORDS` inside `build_bilingual.py`.

---

## तस्बिर कस्तो हुनुपर्छ / Image guidelines

- **आकार / Shape:** 1:1 वर्ग (square). सिफारिस 800×800 px, अधिकतम 1200×1200 px.
- **फाइल साइज / File size:** प्रति तस्बिर 150 KB भन्दा कम (WebP recommended).
- **विषय / Subject:** एउटै स्पष्ट वस्तु, बीचमा, राम्रो उज्यालोमा।
  One clear subject, centered, well lit.
- **पृष्ठभूमि / Background:** सफा र सादा (सेतो, क्रीम वा हल्का रंग)।
  Clean, plain background so the object stands out.
- **पाठ नहुनुहोस् / No text:** तस्बिरमा कोरियन वा अंग्रेजी शब्द नराख्नुहोस्।
  No Korean or English labels in the picture — the learner must recall the word.
- **अर्थ स्पष्ट / Unambiguous:** `밥` का लागि भातको कचौरा, `돈` का लागि
  नोट वा सिक्का — जुनसुकै हेर्दा एउटै अर्थ बुझिने होस्।
  Use a rice bowl for 밥 and notes/coins for 돈 so the meaning is unmistakable.
- **अधिकार / Rights:** तपाईंसँग प्रयोग गर्ने अधिकार भएको तस्बिर मात्र राख्नुहोस्।
  Only use images you have the right to use.

---

## नयाँ शब्द थप्न / Adding more picture words

1. तस्बिर `images/quiz/<slug>.webp` मा राख्नुहोस्।
2. `build_bilingual.py` मा `VOCAB_WORDS` खोज्नुहोस्।
3. त्यो शब्दको लाइनमा `pic: true` र `image: "images/quiz/<slug>.webp"` थप्नुहोस्।
4. `python3 build_bilingual.py` चलाएर `index.html` पुनः बनाउनुहोस्।

Add the image, set `pic: true` and the `image:` path on that word in
`VOCAB_WORDS`, then rebuild with `python3 build_bilingual.py`.
