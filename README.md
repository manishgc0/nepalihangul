# नेपालीमा हाङ्गुल — Nepali Hangul

A single-page PWA for learning Korean Hangul **from Nepali**. Cream paper theme,
pastel Korean/Nepali glyph background, guided 10-step flow.

Nepali is the default language (`LANG = "ne"`); a saved `hangul_lang_pref` can
switch a returning visitor to English, and the header toggle changes it instantly
without reloading.

## Build

```bash
python3 build_bilingual.py
```

This rewrites `index.html` from the source in `build_bilingual.py`, and
regenerates `sw.js` with the current quiz-image precache list.
To preview with audio:

```bash
python3 server.py          # /api/tts on port 3090, serves the site + cached MP3s
# open http://localhost:3090/index.html
```

`python3 -m http.server 8765` also works for the UI, but `/api/tts` returns 404,
so audio falls back to the browser's Korean speech voice.

## Which file is canonical?

| File | Status |
| --- | --- |
| `build_bilingual.py` | **Canonical.** Guided flow, bilingual UI, current theme, animation, a11y. |
| `index.html` | Generated output. Do not edit by hand. |
| `build_site.py` | Earlier generator (flat minimalist theme). Running it overwrites `index.html` with the old design. |
| `update_flow.py` | Earlier generator (guided flow, old red theme). Running it overwrites `index.html` with the old design. |

## Layout

- **Small phones (≤420px)**: single column, compact two-row header (brand + language, then the speed control), fixed bottom navigation.
- **Mobile/tablet**: single column, fixed bottom navigation.
- **Tablet (≥700px)**: wider single column, same bottom navigation.
- **Desktop (≥1024px)**: fixed left sidebar navigation, two-column roadmap, wider content shell.
- **Wide (≥1400px)**: wider sidebar.

## Opening animation

`index.html` opens on a short, skippable title card: a white circle pops in with `한` and a
Nepali `क` badge, the bilingual wordmark and tagline fade up, and a progress bar fills.
The card fades to the app after about 1.25s, or immediately on click/tap/keypress.
With `prefers-reduced-motion: reduce` the card is skipped entirely.

## Quiz & picture-word memory

Step 10 opens a chooser with two 10-question modes:

| Mode | What it tests |
| --- | --- |
| **चित्र शब्द परीक्षा** (Picture words) | Look at an image, recall the Korean word. Primary mode for long-term memory. |
| **अक्षर सुनाइ** (Letter listening) | Hear a sound, choose the matching Hangul letter. |

Each mode saves its own best score in `localStorage`
(`hangul_quiz_best_pictures`, `hangul_quiz_best_letters`). Wrong picture words
are collected into a "दोहोर्याउनुपर्ने शब्दहरू" review list on the result screen,
and the correct word is spoken when the answer is revealed.

## संख्या पियानो — Interactive Number Piano (Step 6)

Step 6 features an interactive musical **संख्या पियानो (Number Piano)** designed to make mastering Sino-Korean and Native Korean numbers intuitive and fun:

- **10-Key Musical Keyboard**: Spans C4 to E5 (Do, Re, Mi, Fa, Sol, La, Ti, Do, Re, Mi) with realistic ivory key styling, touch depression animations, and keyboard shortcuts (`1` to `9`, `0` = 10).
- **Dual Sound Engine**:
  - **Web Audio API Synth**: Rich harmonic piano note synthesis (fundamental + resonance overtones) with an acoustic decay envelope.
  - **Spoken Korean Audio**: Concurrent clear pronunciation via `say()`, matching the user's selected accent (🇳🇵 Nepali accent or 🇰🇷 Korean native accent).
  - Sound toggles: `🎹+🗣️` (Tone + Voice), `🎹` (Tone Only), or `🗣️` (Voice Only).
- **System Switcher**: One-tap toggle between **सिनो कोरियन (Sino: 일, 이, 삼, 사, 오, 육, 칠, 팔, 구, 십)** and **मौलिक कोरियन (Native: 하나, 둘, 셋, 넷, 다섯, 여섯, 일곱, 여덟, आहोप, 열)**.
- **LED Screen & Sequence Tracker**:
  - Displays large Hangul glyph, digit, Nepali transliteration, musical pitch, and practical usage context.
  - Melody ribbon tracks played note sequences with **🔁 पुनः बजाउनुहोस् (Replay)** and **🗑️ मेट्नुहोस् (Clear)**.
- **Practice Modes & Mini-Games**:
  - 🎵 **१ देखि १० क्रमिक धुन (Scale 1–10)**: Guided counting practice from 1 to 10.
  - 🌟 **ट्विंकल ट्विंकल धुन (Twinkle Melody)**: Plays the classic nursery melody using Korean number keys.
  - 🎯 **सुन्नुहोस् र थिच्नुहोस् (Listen & Press Quiz)**: Voice announces a random number; user presses the correct piano key to earn +10 XP with celebratory sound effects.

### Adding the quiz images

The picture quiz expects 12 images in `images/quiz/`:
`factory`, `helmet`, `water`, `rice`, `bus`, `hospital`, `money`, `machine`,
`box`, `truck`, `medicine`, `bag` — all as `<slug>.webp`.

Until an image exists, the card shows a large emoji and "तस्बिर थपिन बाँकी"
("Image coming soon"), so the quiz is usable with zero images. See
`images/quiz/README.md` for the full size, framing, and naming rules.

## Accessibility & interaction

- Real landmarks and headings: `<main id="app">`, a skip link, one `h1` per screen, `h2` section heads, `h3` card heads.
- Cards, list rows, and the wordmark are native `<button>`s, so keyboard and screen-reader users get the same actions as pointer users.
- Navigation exposes `aria-current="page"`; speed and language controls expose `aria-pressed`.
- Active states use weight, shape, and a rose marker in addition to color.
- Quiz answers show ✓/✕ marks plus a polite live-region message, reveal the correct option, and pause before advancing.
- Accent colors are tuned to WCAG AA on their tinted backgrounds; tap targets grow to 44px on coarse pointers.
- **Type scale.** Body text is `17.5px` and every explicit `font-size` at or below
  `16.5px` in the stylesheet sits one step larger than the original baseline
  (`.sub` 15.5, `.lrow .lt small` 14.5, `.mission-task` 13.5, pills 12.5). Only
  the bottom-nav labels under `430px` were left at `11.5px` — seven tabs on a
  320px screen cannot take a bigger label without truncating.
  Two layouts were reflowed to absorb the extra width: `.flow-btn` lost
  `white-space:nowrap` so long "next step" labels wrap instead of bleeding out of
  the pill, and `.rule-flow` stacks vertically under `380px` so the 19px Hangul
  written→spoken pair stops squeezing.

## Game layer (Bunpo-style progression)

The app now carries a full progression loop, persisted in `localStorage` under
`hangul_game_v1`. Nothing is unlocked by payment — every Bunpo-style premium
pattern is available from the first screen.

| Piece | Behaviour |
| --- | --- |
| **XP & levels** | Every correct answer, lesson and course day grants XP. Level curve: 80 XP, then +40 per level. The HUD ring on the home page and the game screen shows progress to the next level. |
| **Daily goal** | 60 XP per local day, displayed as the conic ring on the HUD. Resets at midnight and refreshes the daily quest set. |
| **Streak** | Consecutive active days, shown with 🔥. One missed day resets it; best streak is kept. |
| **Hearts** | 5 hearts, one lost per wrong review answer, one restored per completed lesson, plus one every 12 minutes. Review is blocked at 0 hearts. |
| **Combo** | Consecutive correct answers multiply review XP (×1 → ×2 at a 20-answer run in 25% steps). Best combo is recorded. |
| **Quests** | Three rotating daily missions drawn from a seven-item pool seeded by the date; progress bars and automatic XP on completion. |
| **Achievements** | 17 stamps (first lesson, 3/7-day streak, levels, combos, 10/50 cards, perfect quiz, 30 words met, 10 course days, first/4/all-8 scenes, runner 10/25). |
| **SRS deck** | Every word met enters a 6-box system (0/1/2/4/8/16 days). Correct answers promote; misses demote and return tomorrow. Picture words show the image, text-only words show the Hangul. |
| **Review deck** | 10 cards per session, pulled from due + unseen vocabulary, with feedback, XP, hearts, and a session summary. |
| **Hangul Runner** | A separate 3-lane canvas game — not a flashcard flow. See below. |
| **Scene Missions** | Bunpo's task-based lesson format, eight scenes in Nepali. See below. |
| **SFX** | Bunpo's own correct / wrong / complete / streak samples. See below. |

Hooks: course day completion (`toggleDayComplete`), lesson completion
(`awardBunpoCompletion`), quiz answers (`checkQuizAnswer`), vocabulary taps
(listen quest), the review deck (`scheduleWord`) and the runner
(`runnerFinish`).

`Escape` closes the lesson or review modal. All motion respects
`prefers-reduced-motion`.

## Hangul Runner (`runner` screen)

A three-lane endless runner built on a 2D canvas — deliberately a *different*
kind of game from the SRS deck. Reachable from the home card, the game hub card
and the game tab (`runner` maps to the `game` nav item).

- **Loop** — a 60-second run. One row of two syllable tiles drops at a time,
  one correct and one decoy; the romanized prompt (`ga`, `nyeo`, `chi`…) sits in
  the top bar.
- **Audio** — every spawn speaks the syllable (`say(item.ch)`), so the ear gets
  the sound at the same moment the eye gets the glyph. The prompt's 🔊 button
  replays the current target on demand. Speech is clipped by the next row on
  purpose — `say()` pauses the previous clip — so the row's syllable lands just
  before you commit to a lane.
- **Mute** — the 🔔/🔕 pill in the score row flips `RUN.muted` and persists to
  `localStorage["hangul_runner_muted"]`, so a muted runner stays muted across
  reloads. Separate from the global `hangul_sfx_off`, because constant speech is
  louder than the rest of the app. Muting cancels the in-flight clip and the
  WebAudio blips with it.
- **Decision** — steer into the lane holding the matching glyph. The judgment
  line is the dashed rule across the player capsule. Correct = score + combo +
  speed (+ramp px/s per hit, capped at the preset's max). Wrong glyph = one of
  three hearts and a screen shake. Dodging into the empty lane breaks the combo.
- **Pace** — three presets, chosen before a run or switched live mid-run:

  | key | pill | scroll speed | per hit | per miss | row gap |
  | --- | --- | --- | --- | --- | --- |
  | `slow` | 0.7x | 125 → 360 px/s | +5 | −22 | 0.46 s |
  | `normal` | 1.0x | 190 → 540 px/s | +8 | −34 | 0.35 s |
  | `fast` | 1.4x | 265 → 780 px/s | +12 | −46 | 0.27 s |

  Set it from the 🏃 pill in the score row (cycles slow → normal → fast) or from
  the three-button chooser on the ready card. Persisted in
  `localStorage["hangul_runner_speed"]`. Switching mid-run retunes the live `RUN`
  object — it snaps `speed` to the new preset's floor and tightens `gap` — rather
  than re-rendering, because `renderApp()` would tear down the canvas and the run
  with it. Slow is genuinely one-handed on a phone.
- **Input** — `←`/`→`, `A`/`D`, click/tap the left or right half of the field,
  horizontal swipe, or the two on-screen arrow pads.
- **Item pool** — 14 basic consonants × 10 basic vowels (140 syllables) with
  spelling-based Revised Romanization; decoys always share the vowel or the
  consonant so the choice is a real discriminator (야 vs 요, 크 vs 카).
- **Rewards** — XP `6 + score*3 + combo*1.5` (cap 140), `runnerBest`,
  `runnerRuns`, `runnerCorrect` in `hangul_game_v1`, plus the `runner_10` /
  `runner_25` achievements and the combo/correct daily quests.
- **Rendering** — DPR-aware canvas, theme colours read from the CSS custom
  properties so it follows light/dark, top fog so rows dissolve into the HUD
  instead of hard-clipping, ambient glyph field for speed feel, WebAudio blips.

## Scene Missions (`mission` screen)

Bunpo's real lesson format is *TaskBased*: a place, a partner, one goal, and a
few concrete tasks you have to accomplish by talking. Eight of those scenarios
are rebuilt here for Nepali learners — the structure is Bunpo's, the Nepali and
the Korean lines are written for this course.

| id | Scene | Goal |
| --- | --- | --- |
| `m_intro` | School orientation | Introduce yourself |
| `m_lunch` | Lunchtime in Seoul | Order a lunch menu |
| `m_directions` | Mokpo station | Ask a stranger for directions |
| `m_coffee` | Angel-in-us | Order a cold drink |
| `m_street` | Street stall | Order street food |
| `m_sick` | College corridor | Describe how you feel |
| `m_pizza` | Yeosu flat | Order a pizza for delivery |
| `m_taxi` | Evening before departure | Book a taxi ride |

Each mission is a `scene` step (place, partner, spoken goal, three task chips)
followed by three `mission` steps. Every step shows the partner's Korean line
with romanization and a Nepali translation, taps to speak it, then asks you for
a reply — four options, shuffled at render so the answer is never always first.
A correct pick gets the explanation of the grammar it used; a wrong pick
re-queues the step at the end of the lesson and shows the correct line.

- **Persistence** — completed scenes are stored in
  `localStorage["hangul_missions_done"]` as an array of ids.
- **Rewards** — a mission runs through the same `awardBunpoCompletion` hook as a
  grammar lesson: XP scaled by step count and accuracy, one heart back, quests
  and achievements updated. Missions increment `stats.missions` and the daily
  `missions` counter, so the `q_mission` daily quest and the `mission_1` /
  `mission_4` / `mission_8` stamps all read from the same completion event.
  Mission completion is recorded *before* the award hook runs, so a scene that
  clears the fourth or eighth mission unlocks its stamp in the same celebration.
- **Marking** — the chosen option is struck through in rose with ✕, the correct
  one is filled sage with ✓, and it scrolls into view so the sticky feedback
  banner never covers the reveal.
- **Entry points** — home feature card, game-hub card, and the खेल nav tab
  (`mission` maps to `game`).

## Sound effects

Every sound in the app is a sample lifted from the Bunpo APK
(`com.bunpoapp.apk`, `res/raw/`), re-encoded to mono 44.1 kHz ~80 kbps MP3 so
they load fast over the static server. There are no synthesized tones left —
the runner used to carry five WebAudio oscillator blips and those are gone.

| File | Bunpo source | Used for |
| --- | --- | --- |
| `audio/sfx/correct.mp3` | `correct.m4a` | correct quiz answer, correct review card, correct lesson/mission step, sound-on confirmation |
| `audio/sfx/wrong.mp3` | `wrong.m4a` | wrong quiz answer, wrong review card |
| `audio/sfx/complete.mp3` | `complete.m4a` | lesson/mission completion, end of a runner |
| `audio/sfx/streak.mp3` | `streak.mp3` | streak milestone (fires once a day at streak ≥ 2) |
| `audio/sfx/correct_soft.mp3` | `sound_correct_soft.mp3` | runner: correct lane |
| `audio/sfx/wrong_soft.mp3` | `sound_wrong_soft.mp3` | runner: wrong lane |
| `audio/sfx/tick.mp3` | `intercom_sent.mp3` | runner: lane change |
| `audio/sfx/start.mp3` | `intercom_received.mp3` | runner: run begins |

The runner gets the soft variants because its events fire every ~1 s and the full
`correct.m4a` jingle would step on itself; `intercom_sent.mp3` is a 0.24 s click,
which is exactly the right length for a lane switch.

Three Bunpo assets are deliberately unused: `intercom_failed.mp3`,
`intercom_operator.mp3`, and `ring.mp3` (a 6.3 s ringtone). None of them map to
an event this app has, and a sound that fires for the wrong reason is worse than
silence.

`sfxPreload()` runs before `renderApp()` at boot, `playSfx(name, volume)` clones
the cached `Audio` element so overlapping plays don't cut each other off, and a
120 ms per-name throttle stops double-fire from rapid taps. Muting is a single
key: `localStorage["hangul_sfx_off"]` (`"1"` = muted), toggled by the 🔔/🔕
button on the game hub and the missions screen.

The runner has its own switch on top of that — `RUN.muted`, the 🔔 pill in the
score row, persisted in `localStorage["hangul_runner_muted"]`. Every runner
sound (lane tick, run start, soft correct/wrong, completion) is guarded by it,
so muting the runner does not mute the rest of the app and vice versa. The
per-row syllable speech respects it too.

## Letter pronunciation audio

Every vowel and consonant button plays a baked clip from `audio/pron/` — 40
files, 218 KB total, one per jamo. **They are Bunpo's own audio**, pulled off its
server-side TTS, not a substitute voice.

Bunpo has no bundled letter audio: its APK ships 11 `res/raw` SFX and nothing
else, and pronunciation is synthesised per request. That backend is reachable —
it is a FastAPI Cloud Run service fronting a TTS model — so the clips are
extracted from it directly. The reverse-engineering chain, from
`com.bunpoapp` 3.28.0 (Ktor over OkHttp, not Retrofit, so there are no
`retrofit2/http` annotations to read):

| Symbol | Role |
| --- | --- |
| `Lc8/g0;->a()` | base URL, `https://bunpo-basic-283414158288.us-central1.run.app/` |
| `Lc8/g0;->d()` | `a() + "v3/"` — the API prefix; paths without it 404 |
| `Lc8/p;->u()` | `POST text_to_speech`, body `TextToSpeechRequest`, response read as `byte[]` |
| `Lc8/P;->t()` | `FirebaseAuth.signInAnonymously()` — no account needed |
| `TextToSpeechRequest` | fields in order: `language`, `model`, `text`, `voiceName` |

```http
POST https://bunpo-basic-283414158288.us-central1.run.app/v3/text_to_speech
Authorization: Bearer <firebase-idToken>
Content-Type: application/json

{"language":"ko","model":"standard","text":"아","voiceName":""}
```

→ `200 audio/pcm`, RIFF/WAVE, `pcm_s16le`, 24 kHz, mono. `model` must be
`standard` or `gemini` (a `422` lists the enum); `standard` gives a crisp
0.23 s syllable and is what the app uses, `gemini` is only for the live
roleplay voice and comes back four times longer. `voiceName` is accepted and
ignored. The token comes from a Firebase anonymous sign-up against the public
client key shipped in the APK — the other key in `resources.arsc` answers
`ADMIN_ONLY_OPERATION`.

`gen_pron.py` does the whole job:

```bash
python3 gen_pron.py                # Bunpo server, then encode
python3 gen_pron.py --force        # ignore the cached raw WAVs
python3 gen_pron.py --source edge  # offline fallback
```

The fallback is `ko-KR-SunHiNeural` at rate `-15%` via edge-tts, for when the
Cloud Run service is unreachable — a substitute voice, clearly audible as one.
`audio/pron/manifest.json` records which source produced the current files.

Each letter is spoken as its canonical example syllable, because that is how a
letter is pronounced in isolation: `ㅏ` → 아, `ㄱ` → 가, `ㄲ` → 까. (`ㅇ` has no
sound of its own, so it takes the vowel's syllable — 아.) Raw responses are
cached in the gitignored `audio/pron_raw/`; output is trimmed of silence,
peak-normalised to −3 dBFS, and encoded mono 44.1 kHz 96 kbps.

Two bugs the earlier `/api/tts` path had:

- The vowel buttons passed a bare compatibility jamo (`ㅏ`, U+314F) to `/api/tts`.
  A bare jamo is not speakable text; the endpoint returned 1.8 s video rips.
- The consonant buttons passed `ㄱㅏ` — a jamo followed by ㅏ, which is not valid
  Hangul at all.

Routing is a single map, `PRON_SLUG` (jamo → slug), plus `sayPron(ch)`. It plays
`audio/pron/<slug>.mp3` at the current `AUDIO_RATE` through the shared
`playClip()` helper, and falls through to the normal `say()` chain for anything
that is not a single jamo — so the same helper serves the lesson steps, the
speed-bar preview, and full words without a special case. The Bunpo lesson's
`audio` fields (`ㅏ`, `ㅓ`, `ㅗ`, `ㅜ`, `ㄱ`, `ㅂ`) go through it too; its word and
sentence fields go through `say()` and land in the baked library below.

All 40 clips are precached by the service worker — `build_bilingual.py` globs
`audio/pron/*.mp3` into `PRON_CLIPS`, so adding a letter to `gen_pron.py` and
rebuilding is the whole workflow.

## Baked audio library (`audio/lib/`)

Open `index.html` straight off disk — `file://` — and there is no server, so
there is no `/api/tts`. Every syllable and word that used to route through that
endpoint fell through to `speechSynthesis`, which on a machine with no Korean
voice installed means *silence*. That was the "why is there no sound" bug.

The set of strings the app can speak is finite and known at build time, so they
are synthesised once and shipped as static files:

| source | count |
| --- | --- |
| 140 syllables — 14 basic consonants × 10 basic vowels | 140 |
| 980 batchim combinations — the same grid × 7 terminal finals | 980 |
| runtime harvest of everything the UI actually says (`/tmp/opencode/spoken.json`) | 430 |
| `scrape_source()` — quiz answers, lesson `audio:` / `audioPrompt:` fields, sample lists, literal `say('…')` calls | — |
| mission `npcKo:` NPC lines and `goalKo:` goal phrases | 32 |
| the CS1 dictionary headwords (pp. 189–233), harvested by the same whole-array scrape | 887 |
| **after dedupe and normalisation** | **3108 clips, 12.4 MB** |

Every file is 24 kHz mono 48 kbps MP3, silence-trimmed, peak-normalised to
−3 dBFS peak in **both** directions, with 30 ms of leading pad so the clip does
not click. Average 3.7 KB.

Watch out for the gain step: `peak_dbfs()` must not run ffmpeg with `-v error`,
because `astats` reports at info level. Suppressing it makes the function return
its `-10.0` fallback and apply **+7 dB to every clip**, which is what made 485 of
the first batch clip at up to +6 dBFS. Measured with `astats` after encoding, the
whole set now sits between −5.5 and −1.9 dBFS.

### What gets spoken where

| screen | speaks |
| --- | --- |
| Letter chips, lesson steps | `sayPron()` → `audio/pron/` |
| Syllable / batchim grids, vocabulary, grammar, numbers, reading rules | `say()` |
| 44-lesson player | `audio:` / `audioPrompt:` fields, plus `answer` on a miss |
| Scene Missions list | `goalKo` on each card's 🔊 goal chip |
| Scene Missions — scene card | `goalKo` |
| Scene Missions — reply step | `npcKo` on render and on tapping the bubble; the correct `answer` is said back after you pick, right or wrong |

The last two rows are why missions used to be silent: `npcKo:` and `goalKo:` were
never scraped, so those clips did not exist and the chain fell through to a dead
`/api/tts`. A runtime harvest that walks all 44 days plus all 8 missions now
reports zero strings missing from the library.

### Slug scheme

Each codepoint in hex, joined by `-`:

```
각        → audio/lib/ac01.mp3
한국어    → audio/lib/d55c-ad6d-c5b4.mp3
축하합니다 → audio/lib/cd95-d558-d569-b2c8-b2e4.mp3
```

Deterministic, so `libSrc()` in the app computes the same name with no lookup
table — which matters, because `fetch()` of a local JSON is blocked on
`file://`. The `manifest.json` in that directory is for humans and tooling, not
for the runtime.

### Voice Accent (नेपाली लवज vs कोरियन लवज)

The app supports authentic **Nepali Accent** (नेपाली लवज) as the primary voice, alongside **Native Korean** (कोरियन लवज).
- **Default Voice**: 🇳🇵 **नेपाली लवज** (Nepali Accent) — speaks Korean characters and words with authentic Nepali EPS-TOPIK pronunciation rules (e.g., initial `ㄱ` as 'ख', medial as 'ग', `ㅏ` as 'आ', `가방` as 'खाबाङ्'), powered by neural Nepali voice synthesis (`ne-NP-SagarNeural`) and Teabreak curriculum recordings.
- **Toggle**: Switchable at any time from the top header bar and the speed bar. Preference is persisted in `localStorage["hangul_accent_pref"]`.
- **Letter Pronunciation**: All 40 letters in `audio/pron/` are baked in clean Nepali accent. The Korean native clips are preserved in `audio/pron_ko/`.
- **Dynamic TTS**: When running `server.py`, `/api/tts?accent=ne&q=...` dynamically converts Hangul text into authentic Nepali phonetic Devanagari and synthesizes via neural Nepali speech, cached in `audio/nepali_cache/`.

### The four tiers

`say()` is now a chain, and the first tier is the only one that works offline:

| tier | source | when |
| --- | --- | --- |
| 0 | `audio/lib/<slug>.mp3` | everything curated — syllables, words, sentences, lessons |
| 1 | `/api/tts?q=…` | free text only: the writing studio, anything the user types |
| 2 | `speechSynthesis` | tier 1 failed *and* a Korean voice is installed |
| 3 | one toast | tier 2 also failed — says there is no recording and no Korean voice |

### Two rules tier 0 has to obey

**A miss expires.** `_libMiss` used to be a permanent latch: one click while a clip
was still missing sent that string to tier 1 for the rest of the page session, so
a rebuilt library never took effect without a reload. It now stores a timestamp
and expires after `LIB_MISS_TTL` (30 s) — long enough not to hammer the network on
a genuinely absent file, short enough that `gen_audio.py` takes effect live.

**Both libraries are not the same size.** `audio/lib` carries the Nepali accent and
`audio/lib_ko` the Korean-native voice, and they are built separately — so a
string added after one build exists in one library only. `playTier1()` tries the
preferred accent, then the other library, then falls through to tier 1. A wrong
accent beats silence. Verified: with the accent set to Korean, `이름` (absent from
`lib_ko`) resolves from `lib/`, while `안녕하세요` (present in both) still prefers
`lib_ko/`.

A missing file is negative-cached in `_libMiss` so a bad slug does not re-attempt
on every click. Only a real load error (`audio.error`) demotes to tier 1 — an
autoplay rejection is a policy issue, not a missing file, and must not send the
chain chasing a different source.

`playClip(src, onMissing)` and `stopAudio()` back both `say()` and `sayPron()`, so
starting any clip cancels the previous one. The old boot `probeTts()` is gone: a
dead `/api/tts` is no longer a problem for curated content, so probing it at
startup only produced a false alarm.

### Regenerating

```bash
python3 gen_audio.py            # fetch only what is missing, then encode
python3 gen_audio.py --force    # refetch everything
python3 gen_audio.py --list     # print the target set and exit
python3 gen_audio.py --verify   # exit non-zero if any speakable string has no clip
python3 gen_audio.py --source edge   # offline fallback voice
```

**Run `--verify` after touching any Korean string in `build_bilingual.py`.**
It is the gate that catches the failure this library exists to prevent: a word
renders fine but has no clip, so `say()` falls to `/api/tts` (absent on a static
server), then to `speechSynthesis` (no Korean voice on most Linux installs), and
the screen is simply silent. 3,108 strings, 12.4 MB.

`scrape_source()` collects the target set from the app source by shape. It reads
each array literal and keeps **every** Korean field in it, not just the first,
because the fields are not in a fixed order: a vocabulary row starts with the
Hangul, a tense row starts with a Nepali label and puts the Korean second. The
old first-field-only rule baked `걷다` but not `걸어요`, which is the form a
learner actually taps. If a new table uses a shape no rule recognises, the words
ship silent — `--verify` is what notices.

Raw WAVs cache in the gitignored `audio/lib_raw/`, so a re-run after adding one
string fetches one string. `normalize()` in `gen_audio.py` must stay in lockstep
with `normalizeKorean()` in `build_bilingual.py` — bare jamo map to their
canonical example syllable (`ㅇ` → 아, `ㄲ` → 까), and two- and three-jamo inputs
compose into the matching syllable block.

The library is **not** precached. 5 MB of clips would make first install slow for
content most learners never open, and the existing service-worker rule already
covers it: anything under `/audio/` is served stale-while-revalidate, so a clip
played once is instant every time after. Only the 40 letter clips are precached,
because those are on the very first screen.

## Sejong 1A practice decks

The midterm PDF's three 1A lessons are rebuilt as interactive decks on the
grammar screen, each with a Nepali explanation, example words, a short reading
passage, a writing prompt and a sentence-building exercise:

1. `sejong_1a_intro` — self-introduction, 이에요/예요, 은/는, jobs & countries
2. `sejong_1a_phone` — phone numbers, Sino-Korean digits, 뭐예요?, 이/가 아니에요
3. `sejong_1a_objects` — objects and location, 이거/그거/저거, 있어요/없어요

## Sejong 1A curriculum spine (`sejong` screen)

The site used to *name* Sejong 1A on three unrelated screens while holding no
unit data at all, so the label was decoration. `SEJONG_1A` in
`build_bilingual.py` is now the one table everything joins against.

**Where it came from.** The Nuri e-book (`nuri.iksi.or.kr`, `ecatalog5.jsp`) is
an SVG flipbook — the pages are painted, not text nodes, so nothing in the
table was scraped from it. It is the published table of contents of 세종한국어
1A: seven units, each with its can-do task, its grammar patterns, its words and
two performance tasks. That provenance is stated in a comment above the table
rather than dressed up as extraction. 1B is deliberately absent — guessing its
contents would be worse than leaving it out.

| # | Unit | Focus | Words |
|---|------|-------|-------|
| 1 | 안녕하세요? | greetings, name, formality | 12 |
| 2 | 저는 한국 사람입니다 | nationality, job | 12 |
| 3 | 이것은 무엇입니까? | objects, 있어요/없어요 | 12 |
| 4 | 오늘은 날씨가 좋습니다 | weather, formal endings | 15 |
| 5 | 내일은 무엇을 하십니까? | routine, time, 을/를, -에 | 16 |
| 6 | 어떻게 오셨습니까? | transport, route, honorific past | 13 |
| 7 | 여기에서 조금 멉니까? | location, distance, direction | 16 |

96 words, 22 grammar patterns, 14 tasks.

**The interlink contract.** Selecting a unit is one write to
`localStorage["hangul_sejong_unit"]`, and five consumers read it:

| Consumer | What the active unit changes |
|---|---|
| `arcPool(id)` / `arcTapPool(id)` | up to 5 unit words that fit the game's syllable window are prepended to the bank |
| `viewQuiz` `"lesson"` mode | the ten questions are drawn from that unit's words, meaning → Korean |
| `viewVocabulary` `sejong` tab | `sjVocabRows()` lists the spine, each row badged with its unit |
| `viewGrammar` | `renderGrammarUnit()` puts that unit's patterns above the six pillars |
| `viewHome` | `renderSejongToday()` shows the unit, its can-do goal and three doors into it |

`sjUnit()` is the single source of truth and returns `0` for "whole book".
Every consumer treats `0` as no filter, so nothing needs a null check.

**Lesson words are the one deliberate exception to bank disjointness.** The six
arcade banks stay pairwise disjoint so each game has its own vocabulary — but a
word you just studied should follow you wherever you practise it, so
`arcLessonSlice()` prepends it. The arcade intro says how many lesson words are
in the round, so the appearance isn't a mystery.

**Adding a unit** means editing `SEJONG_1A` and nothing else. `sjWordSet()`,
`glossOf()`, the quiz, all six games, the vocabulary tab and the home card pick
it up on the next build.

## Books — the Nepali-medium reference shelf (`books` screen)

Three printed Nepali-language Korean textbooks, transcribed by hand into a
six-tab reference: **वर्णमाला**, **उच्चारण नियम**, **गणना**, **अभिवादन**,
**व्याकरण**, **शब्दकोश**.

| tag | file | pages | what it gave |
| --- | --- | --- | --- |
| `BKL` | Basic Korean Language Book | 83 | letter tables, greetings |
| `CS1` | CamScanner 07-28-2026 | 239 | pronunciation rules, the whole grammar half (pp. 46–80), the alphabetical dictionary (pp. 189–233) |
| `CS2` | CamScanner 03-02-2025 | 245 | counters |

All three are image-only scans — no text layer, and `pdftotext` returns nothing
but the CamScanner watermark. Everything here was read off the page images.

**What this screen carries that nothing else does is the Devanagari reading.**
The site's audio has always spoken Korean the way a Nepali learner hears it
(ㅏ → आ, ㅓ → अ), but the spelling of that mapping lived nowhere on screen.
`BOOK_CONS` and `BOOK_VOWEL` make it explicit, and `bkRead()` composes them:

```
ㄱ + ㅏ → 가 → गा        ㅇ + ㅏ → 아 → आ
ㄱ + ㅓ → 거 → ग         ㅇ + ㅓ → 어 → अ
ㄱ + ㅡ → 그 → ग्        ㅅ + ㅣ → 시 → सि
```

That is exactly the arithmetic the books print as a 19 × 21 grid, so the
composer and the printed table cannot disagree.

**Tense consonants have no separate Devanagari letter.** 된소리 is written with
the plain letter and marked कठोर, because inventing a glyph a learner cannot
unlearn is worse than an honest annotation. Same reason ㅐ and ㅔ both read ए —
modern Korean has merged them.

**Provenance is per-section** (`BKL p3 · CS2 p4`, `CS1 p11`, `CS2 p46`), and the
screen says plainly that 567 scanned pages are not all typed up yet. A reference
you cannot check is a rumour.

### व्याकरण — the grammar half

CS1 pages 46–80 are one continuous grammar course, and it is the part a learner
needs the moment the alphabet is done: which ending goes with which listener,
how each tense is built, and the seven classes of verb that refuse to follow the
rule. The tab is four blocks:

| block | source | shape |
| --- | --- | --- |
| registers, negation, questions, tense, `-고 있다`, adnominal, `-고 싶다`, orders, suggestions | p46–67 | 13 cards, `[korean, devanagari, nepali, tag]` rows |
| the six-tense grid | p68 | one `<details>` per verb, six rows inside |
| seven irregular classes | p69–75 | one `<details>` per class, 92 forms total |
| sixteen conjunctions | p76–79 | one card each, form + worked example |

The six-tense table on p68 is seven columns wide. On a 390 px phone that is
unreadable, so the table is **rotated** rather than truncated: the verb is the
card, the tenses are the rows. Same six forms, same order.

Irregular rows are `[dictionary form, informal form, devanagari, meaning]` and
the tap speaks the **informal** form, because that is the one a learner says
out loud; the dictionary form is the one that appears in a word list, so that is
what the row sorts by. Starred verbs in the book are marked in the meaning
column as regular exceptions (`받다`, `믿다`, `닫다`, `얻다` and friends).

Devanagari here follows the same grid as the alphabet tab plus the sound rules
on p11 — final `ㅂ` is प्, final `ㅇ` is ङ्, `ㅂ + ㄴ` is म्न् — so `갑니다` reads
गाम्निदा and not गाब्निदा. Each block states its printed page range, and the
footer says the same thing the other tabs say: this is a sample of the chapter,
not the whole chapter.

The composer composes any of 19 consonants against any of 21 vowels, so
`build_targets()` in `gen_audio.py` bakes all 399 — 140 (the assembly grid) plus
the tense consonants and compound vowels. A composer whose result is silent is
worse than no composer. The `["한글", "…"]` scrape pattern deliberately does not
require a closing bracket, so the three-field rows here (hangul, Devanagari,
meaning) are harvested too.

### शब्दकोश — the alphabetical dictionary

Half of the 239-page scan is not a grammar course. Printed pages 189–233 are a
Korean → Nepali → English dictionary ordered by initial consonant, and for a
Nepali speaker it is the single most useful block in the book. **1,121 entries**
are typed by hand into `BK_DICT` as `[printed_page, korean, nepali, english]`.

Two limits are stated on screen rather than papered over:

- **The ㄹ section is missing from the scan.** The book jumps ㄷ → ㅁ, so the ㄹ
  chip renders dashed and disabled instead of being filled with guessed words.
- **The scan stops at ㅉ** (printed p233). There is no page after 233 in the file,
  so there is no tail to type.

The book prints a romanisation column. It is deliberately not reproduced —
`bkWord()` derives Devanagari from the same 19 × 21 grid the alphabet tab uses,
which serves a Nepali reader better than `gagi` does:

```
갈비 → गाल्बि      건강 보험 → गन्गाङ् बोहम्
닭   → दाक्        없다      → अप्स्दा
휴대폰 → ह्युदेफोन्
```

`bkWord()` decomposes each syllable into `CI` / `VI` / `FI`, reads the body with
`bkRead()`, then hangs the coda off the end from `BOOK_FIN`. Cluster finals
collapse to the sound actually pronounced, the same way the book's own
romanisation does — 닭 is `dak`, not `dalg`.

`bkInit()` exists because a Hangul syllable never starts with a jamo:
`r[1].charAt(0)` returns `갈`, not `ㄱ`, so the initial has to be pulled out of
the code point (`Math.floor((code - 0xAC00) / 588)`). Chips, counts and the
filter all read through it.

The list renders 60 rows at a time (`BK_DICT_CAP`, +80 per "more" tap) — 1,121
rows in one shot is a scroll nobody finishes. Search matches Korean, Nepali,
English **and** the derived Devanagari, so a learner who can only spell the word
in Devanagari can still find it. Rows are deduped on `(korean, nepali)`; where
the book genuinely repeats a headword with a different meaning (`배` = stomach /
boat / pear) both rows survive.


## Offline / PWA

`sw.js` is generated by `build_bilingual.py` (edit the template there, not the
output) and registered at boot from the page:

```js
if ("serviceWorker" in navigator && location.protocol !== "file:") {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js"));
}
```

Cache name `nepalihangul-v3`. The precache list is the app shell — `index.html`,
the manifest, all six icons and the four SFX files — plus every
`images/quiz/*.webp`, read from the directory at build time, so adding an image
and rebuilding is enough. That is 40 entries, about 1.8 MB.

| Request | Strategy |
| --- | --- |
| Navigation (`index.html`, `./?source=pwa`) | **Network-first**, 4.5 s timeout, falls back to the cached shell, then to a small built-in offline page. A rebuild shows up on the next reload without clearing anything. |
| `audio/`, `images/`, `icons/`, Google Fonts | **Stale-while-revalidate** — served from cache instantly, refreshed in the background. |
| `/api/tts` | **Not intercepted.** Every call carries a `Date.now()` cache-buster, so caching it would only fill storage. Offline, `say()` already falls back to `speechSynthesis`. |
| `sw.js`, `manifest.webmanifest` | Left to the network so updates land. |

Per-item `cache.add` is wrapped in try/catch: one missing icon or image cannot
abort the install. Old `nepalihangul-*` caches are deleted on activate, and the
worker takes over immediately (`skipWaiting` + `clients.claim`).

Offline behaviour in the UI: the app keeps working from cache, a toast reports
the state when the network drops or returns, and a boot check fires the same
toast when the page opens already offline (`navigator.onLine === false`, after
the opening card so it doesn't collide).

Verify by hand: load the page once, then DevTools → Network → Offline → reload.
The full app, the nav, the quiz images and the missions all still render.

## Hangul Arcade

Typing.com's student roster, rebuilt around Hangul. Six games sit on three
shared engines so a fix to one benefits its sibling.

| Game | typing.com | Engine | Win condition |
| --- | --- | --- | --- |
| फल निन्जा / Fruit Ninja | Keyboard Ninja | `fall` | 15 slices |
| अन्तरिक्ष रक्षक / ZType | ZType | `fall` | 12 words |
| आकाश जम्प / Sky Jump | Keyboard Jump | `ladder` | 60 s timer |
| हाङ्गुल दौड / Hangul Race | — | `ladder` | 12 words, beat the rival |
| बेलुन फुटाउने / Type a Balloon | Type a Balloon | `tap` | 12 pops |
| लक्ष्य फ्याँक्ने / Type Toss | Type Toss | `tap` | 60 s timer |

- `fall` — words drop, the lowest is the active target; build its syllable on
  the shared pad and hit the action button. Three floor hits ends the round.
  Drop speed scales with field height (`H / 9.5 + wave * 8`), so a 470 px phone
  arena and a 369 px desktop arena feel the same.
- `ladder` — one word at a time; every correct syllable advances the hero or
  the car. Race rival progress is `dt / (goal * 3.4)`, about 41 s of typing.
- `tap` — a Nepali reading is shown at the top; tap the Korean word that
  matches. Balloons rise in shuffled thirds so they never overlap; toss targets
  sit on a shuffled four-quadrant grid.

No image pipeline. Every thumbnail, stage and prop is inline SVG or CSS
gradient.

### Difficulty

Every game runs at one of three tiers, chosen from the arcade header or from
the intro card, and remembered in `localStorage["hangul_arcade_level"]`
(`easy` / `med` / `hard`, default `med`). One table, `ARC_DIFF`, drives all six
games and the lesson Ninja:

| Knob | easy | med | hard |
| --- | --- | --- | --- |
| `slow` — movement speed | **0.42×** | 1× | 1.55× |
| `spawn` — gap between spawns | 2.10× | 1× | 0.70× |
| `time` — clock length | 1.70× | 1× | 0.70× |
| `rival` — opponent's pace | 0.42× | 1× | 1.40× |
| `lives` | 5 | 3 | 3 |
| `bomb` — toss time penalty | 2 s | 4 s | 6 s |

Easy is not a nudge. A Fruit Ninja token falls at 15 px/s instead of 41 — a
word takes over twenty seconds to reach the floor — and the gap between tokens
is 2.1× longer. `arcStart()` reads the tier once and bakes it into the run;
`arcSetDiff()` refuses to switch mid-run, because a live change would only make
the numbers lie.

Best scores are keyed by tier — `localStorage["hangul_arcade_best"]` stores
`{ "ninja:easy": 490 }`, so an easy run never sits on top of a hard one. The
hub card shows the best for whichever tier is selected.

### One vocabulary per game

The six games used to share one 192-word pool, so a player met the same twenty
words in every game. Each game now draws from its own bank, declared in
`ARC_BANK`:

| Game | Bank | Words |
| --- | --- | --- |
| Fruit Ninja | one syllable, from `NJ_BANK` + Daily / Health / People / Locations | 31 |
| ZType | EPS Work, Safety, Transport, Objects, Health | 25 |
| Sky Jump | Places, Locations | 19 |
| Hangul Race | People, Countries | 21 |
| Type a Balloon | food and drink | 20 |
| Type Toss | time, nature, things you carry | 26 |

Nothing in `ARC_BANK` is a gloss. An entry names a category, an `NJ_BANK` index
or a bare word, and `arcGlossMap()` resolves the Nepali reading out of
`VOCAB_WORDS` → `NJ_BANK` → `COURSE_44_DATA`, so a reading can never drift from
the lesson it came from. Words the 44-day course never glossed live in
`ARC_EXTRA`, a hand-checked pair table beside the bank it feeds — deliberately
not in `VOCAB_WORDS`, which drives the vocabulary screen and the picture quiz.
`ARC_BANK.toss.skip` subtracts the three words Race and ZType already own, so
the banks are pairwise disjoint (verified in-page: no word appears twice).

`arcTapPool(id)` is the same bank filtered to entries that carry a reading — a
balloon with no cue is unplayable.

The pad is the Ninja pad: `TC_PAD_CHO` / `TC_PAD_JUNG` / `TC_PAD_JONG`, laid
out as a 7 / 9 / 9 grid at every width. Taps are the primary input, because
Nepali learners rarely have a Korean IME installed.

### Physical keyboard

`kbApply()` sits behind the pad and accepts three input shapes, in order of
preference:

| Input | What arrives | Path |
| --- | --- | --- |
| OS Korean IME | a finished syllable | `compositionend` → `kbSyllable()` |
| QWERTY | plain ASCII | `KB_DUBEOL` → 두벌식 jamo → same state machine |
| Hangul jamo | `ㄱ` `ㅏ` | direct `KB_CHO` / `KB_JUNG` / `KB_JONG` lookup |

`KB_DUBEOL` is the standard two-set layout (`r`→ㄱ, `k`→ㅏ, shift for the
tense consonants and ㅒ/ㅖ), so `r k` composes 가 with no IME installed. The
pad's `step` counter (0–3) tracks cho → jung → jong, and `kbApply()` submits
the instant `njCompose(cho, jung, jong)` equals the character the game wants,
so a three-key syllable needs no Enter. Enter and Space force a submit,
Backspace clears the pad, Escape closes the arena.

Compounds compose the way an IME composes them: `KB_JUNG_PAIR` turns ㅗ + ㅏ
into ㅘ, `KB_JONG_PAIR` turns ㄹ + ㄱ into ㄺ. Without that, every word holding
a compound vowel or batchim would be untypeable — `과` is `r h k`, `닭` is
`e k f r`.

### The keyboard guide

A full ANSI chassis (`kbkHtml()`) sits where the pad sits — number row, tab,
caps lock, shift, enter, backspace, a 15-column bottom row with a real
spacebar — and every letter key carries the 두벌식 jamo over the Latin key
that produces it (`ㄱ` over `r`, `ㅏ` over `k`). It reads as a keyboard
because it is shaped like one, not like a row of buttons.

`KBK_ROWS` is a list of `"key"` / `"key:span"` specs and each row must sum to
15 grid columns; `kbkKeyHtml()` parses the span and picks the right cap class
(`kbk-digit` for the number row with its shifted glyph underneath, `kbk-mod`
for the modifiers, `kbk-space` for the bar). `kbHintPaint()` lights the next
required key and pulses it; `kbkFlash()` flashes green on the key that just
landed. `KB_JUNG_SPLIT` / `KB_JONG_SPLIT` let the guide walk a compound one
keypress at a time, so `과` lights ㅗ then ㅏ rather than pointing at a key
that does not exist.

The guide is also a keyboard you can press: `kbkKeyHtml()` puts
`onclick="kbkPress(this)"` on every jamo cap, and `kbkPress()` feeds exactly
what the cap is showing — the shifted jamo when the cap carries `.shift`, the
base otherwise. Without it a shifted target (`딸`, which needs `⇧E`) lit the
`e` cap and then did nothing when pressed, because the cap's `data-j` is `ㄷ`.
`kbHintPaint()` relabels the Latin legend to `⇧E` while the cap is shifted, so
the glyph and the legend never disagree. On a phone this is the only way to
reach a shifted jamo at all — there is no physical keyboard to hold Shift on.

Two guides can be in the DOM at once (the lesson Ninja's and the arcade's), so
`kbkRoot()` resolves the live one — the arcade when it is open, else the modal
holding `#njField` — instead of trusting a duplicated id.

It replaces the pad rather than stacking on top of it — one input surface at a
time keeps a 390 px phone from overflowing. On boot a fine pointer (desktop,
laptop trackpad) opens on the guide and a coarse one (phone) opens on the pad,
because a keyboard you cannot press is a wall; `hangul_kb_mode` (`"1"`/`"0"`)
records an explicit choice and outranks both. The `प्याड` link in the guide
footer hands the pad back, and `show keyboard` on the pad hint hands it
forward again.

Tap games number their targets instead of asking for a syllable: `arcNumberTargets()`
stamps a number once at spawn and never moves it — a rising balloon must not
reshuffle the key that picks it. Digits 1–9 map straight to that stamp, and the
badges stay hidden (`body:not(.kb-on)`) until the first physical keydown so
touch players never see them.

## Notes

- Moving the pointer gives the background glyphs a small parallax + rotation drift, layered by glyph size.
  The effect is disabled for `prefers-reduced-motion` and on touch-only devices.
- Audio is four tiers, and **tier 0 is static**: `audio/lib/<slug>.mp3` (every
  curated syllable, word and sentence — see **Baked audio library** above), then
  `/api/tts`, then the browser Speech Synthesis API, then a toast. Tier 0 is why
  the app is fully audible when opened as `file:///`, with no server at all. Only
  free text — the writing studio, anything the user types — needs
  `python3 server.py` on `http://localhost:3090/index.html`.
- Tapping free text when tiers 1 and 2 both fail raises one toast, once per tab
  via `sessionStorage["hangul_tts_hint"]`, saying the phrase needs the audio
  server. There is no boot probe: curated content no longer depends on the
  endpoint, so probing it at startup only produced a false alarm.
- `manifest.webmanifest` and `icons/` match the current cream/rose theme.
- `sw.js` is generated by the build — see **Offline / PWA** above. Bump `VERSION`
  in the template when you change a precached asset in place; otherwise
  stale-while-revalidate handles it on the next load.
