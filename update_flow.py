# -*- coding: utf-8 -*-
"""
Script to rebuild the Nepali Hangul app with an intuitive, guided, pedagogical flow.
"""

html = r'''<!DOCTYPE html>
<html lang="ne">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#ffffff" id="tc">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="application-name" content="नेपालीमा हाङ्गुल">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Nepali Hangul">
<meta name="description" content="नेपाली भाषामा कोरियन हाङ्गुल, उच्चारण, शब्दार्थ, वाक्य, गन्ती र व्याकरण सिक्ने सजिलो एप।">
<title>नेपालीमा हाङ्गुल — Nepali Hangul</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#fbfbfc;
  --tile:#ffffff;
  --text:#1a1112;
  --sub:#766769;
  --line:rgba(26,17,18,0.08);
  --fill:#f4ebeb;
  --soft:#fcf7f7;
  --red:#e11d2e;
  --tint:rgba(225,29,46,0.08);
  --green:#1fa85a;
  --gbg:rgba(31,168,90,0.12);
  --rbg:rgba(225,29,46,0.12);
  --blue:#2563eb;
  --bbg:rgba(37,99,235,0.1);
  --grad:linear-gradient(135deg,#9b0e1b 0%,#e11d2e 58%,#ff4d56 100%);
  --dark:linear-gradient(160deg,#2b080d 0%,#0c0406 72%);
  --sh:0 14px 30px -16px rgba(130,12,24,0.28),0 2px 6px rgba(130,12,24,0.05);
  --card-sh:0 4px 16px -2px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
  color-scheme:light;
  box-sizing:border-box;
}
html.dark{
  color-scheme:dark;
  background:#0d0708;
  --bg:#0d0708;
  --tile:#181012;
  --text:#f8eff0;
  --sub:#ad9b9d;
  --line:rgba(255,255,255,0.1);
  --fill:#2b191c;
  --soft:#140c0e;
  --red:#ff4d5c;
  --tint:rgba(255,77,92,0.16);
  --green:#32d277;
  --gbg:rgba(50,210,119,0.16);
  --rbg:rgba(255,77,92,0.18);
  --blue:#60a5fa;
  --bbg:rgba(96,165,250,0.16);
  --grad:linear-gradient(135deg,#910e1a 0%,#db1d2e 58%,#ff4d56 100%);
  --dark:linear-gradient(160deg,#2a080d 0%,#090304 72%);
  --sh:0 14px 30px -16px rgba(0,0,0,0.8),0 2px 6px rgba(0,0,0,0.4);
  --card-sh:0 4px 16px -2px rgba(0,0,0,0.4);
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:"Mukta",-apple-system,"Helvetica Neue",Arial,sans-serif;
  font-size:16.5px;
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
  min-height:100vh;
  display:flex;
  justify-content:center;
  padding:14px 16px 110px;
}
#app{width:100%;max-width:448px;margin:0 auto}
.ko{font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif}

/* Top App Header with Step Breadcrumbs */
.top-bar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:8px 0 16px;
  border-bottom:1px solid var(--line);
  margin-bottom:16px;
}
.back-btn{
  background:var(--soft);
  border:1px solid var(--line);
  color:var(--text);
  border-radius:12px;
  padding:6px 14px;
  font:inherit;
  font-size:14px;
  font-weight:700;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:6px;
}
.back-btn:hover{background:var(--fill)}
.step-badge{
  font-size:12.5px;
  font-weight:700;
  color:var(--red);
  background:var(--tint);
  padding:4px 10px;
  border-radius:99px;
  letter-spacing:0.2px;
}

/* Titles and Hero */
.title{font-size:32px;font-weight:800;line-height:1.2;letter-spacing:-0.4px;margin:2px 0 14px}
.title em{font-style:normal;color:var(--red)}
.title span{color:var(--sub);font-weight:500;font-size:22px}
.hero{
  position:relative;
  overflow:hidden;
  color:#fff;
  background:radial-gradient(110% 90% at 0% 115%,rgba(10,4,5,0.78),transparent 62%),var(--grad);
  border-radius:26px;
  padding:20px 22px 22px;
  box-shadow:var(--sh);
}
.hero::after{
  content:"한";
  position:absolute;
  right:-8px;
  bottom:-32px;
  font:900 155px/1 "Noto Sans KR",sans-serif;
  color:rgba(255,255,255,0.11);
  pointer-events:none;
}
.hero>*{position:relative;z-index:1}
.hero small{display:block;opacity:0.9;font-size:14.5px;font-weight:500}
.hv{font-size:40px;font-weight:800;letter-spacing:-0.5px;line-height:1.2;margin:2px 0}
.meter{display:flex;align-items:center;gap:10px;margin-top:14px}
.meter div{flex:1;height:12px;background:#fff;border-radius:99px;padding:2px}
.meter i{display:block;height:100%;min-width:8px;border-radius:99px;background:linear-gradient(90deg,#30050a,#e11d2e)}
.meter b{font-size:15px}

/* Learning Track / Journey Pathway */
.track-wrap{margin:18px 0}
.track-step{
  position:relative;
  display:flex;
  gap:16px;
  padding-bottom:20px;
}
.track-step:last-child{padding-bottom:0}
.track-line{
  position:absolute;
  left:21px;
  top:44px;
  bottom:0;
  width:2px;
  background:var(--line);
}
.track-icon{
  width:44px;
  height:44px;
  border-radius:50%;
  background:var(--soft);
  border:2px solid var(--line);
  color:var(--text);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:18px;
  font-weight:800;
  flex-shrink:0;
  z-index:1;
}
.track-step.active .track-icon{
  background:var(--red);
  color:#fff;
  border-color:var(--red);
  box-shadow:0 0 0 4px var(--tint);
}
.track-step.done .track-icon{
  background:var(--green);
  color:#fff;
  border-color:var(--green);
}
.track-card{
  flex:1;
  background:var(--tile);
  border:1px solid var(--line);
  border-radius:20px;
  padding:14px 16px;
  box-shadow:var(--card-sh);
  cursor:pointer;
  transition:all .15s;
}
.track-card:hover{
  border-color:var(--red);
  transform:translateY(-1px);
}
.track-card h4{
  margin:0 0 2px;
  font-size:17.5px;
  font-weight:700;
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.track-card p{margin:0;font-size:14px;color:var(--sub)}
.track-tag{
  font-size:11.5px;
  font-weight:700;
  padding:2px 8px;
  border-radius:99px;
  background:var(--soft);
  color:var(--sub);
}
.track-step.active .track-tag{background:var(--tint);color:var(--red)}

/* Flow Control Action Buttons */
.flow-actions{
  margin-top:20px;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.flow-btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  width:100%;
  background:var(--red);
  color:#fff;
  border:0;
  border-radius:18px;
  padding:14px 18px;
  font:inherit;
  font-size:16px;
  font-weight:700;
  cursor:pointer;
  box-shadow:0 8px 18px -4px rgba(225,29,46,0.38);
  transition:all .15s;
}
.flow-btn:hover{transform:translateY(-1px);filter:brightness(1.05)}
.flow-btn.ghost{
  background:var(--soft);
  color:var(--text);
  border:1px solid var(--line);
  box-shadow:none;
}
.flow-btn.ghost:hover{background:var(--fill)}

/* Tiles & Chips */
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
.tile,.itile,.list,.pc,.rc{background:var(--tile);box-shadow:var(--card-sh);border:1px solid var(--line)}
.tile{border-radius:22px;padding:14px 16px}
.tile p{margin:0 0 4px;font-size:14.5px;color:var(--sub);font-weight:500}
.tile b{font-size:28px;font-weight:800;letter-spacing:-0.5px}
.tile small{font-size:14px;color:var(--sub);margin-left:4px}
.seg{display:flex;background:var(--soft);border:1px solid var(--line);border-radius:16px;padding:4px;margin:12px 0 0}
.seg button{
  flex:1 1 0;
  min-width:0;
  border:0;
  background:none;
  color:var(--sub);
  font:inherit;
  font-size:14.5px;
  font-weight:600;
  padding:8px 4px;
  border-radius:12px;
  cursor:pointer;
  transition:all .2s;
}
.seg button.on{background:var(--tile);color:var(--red);box-shadow:0 3px 10px -2px rgba(110,10,22,0.22)}
.head{font-size:17.5px;font-weight:700;margin:18px 0 8px;display:flex;align-items:center;justify-content:space-between}
.head small{font-size:13.5px;color:var(--sub);font-weight:500}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.chip{
  border:1px solid var(--line);
  background:var(--tile);
  border-radius:14px;
  padding:8px 12px;
  font-size:15.5px;
  font-weight:600;
  color:var(--text);
  cursor:pointer;
  box-shadow:var(--card-sh);
  transition:all .15s;
}
.chip:hover{border-color:var(--red)}
.chip.on{background:var(--red);color:#fff;border-color:var(--red);box-shadow:0 6px 14px -3px rgba(225,29,46,0.4)}
.list{border-radius:24px;overflow:hidden;margin:12px 0}
.lrow{
  width:100%;
  display:flex;
  align-items:center;
  gap:14px;
  padding:14px 16px;
  background:none;
  border:0;
  border-bottom:1px solid var(--line);
  font:inherit;
  color:inherit;
  text-align:left;
  cursor:pointer;
  transition:background .15s;
}
.lrow:last-child{border-bottom:0}
.lrow:hover{background:var(--soft)}
.lrow .ln{
  width:42px;
  height:42px;
  border-radius:14px;
  background:var(--tint);
  color:var(--red);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:20px;
  font-weight:700;
  flex-shrink:0;
}
.lrow .lt{flex:1;min-width:0}
.lrow .lt b{display:block;font-size:16.5px;font-weight:700}
.lrow .lt small{display:block;font-size:13.5px;color:var(--sub);margin-top:1px}
.lrow .lg{color:var(--sub);font-size:18px;font-weight:600}
.spk{
  position:absolute;
  right:16px;
  bottom:16px;
  width:44px;
  height:44px;
  border-radius:50%;
  background:rgba(255,255,255,0.22);
  backdrop-filter:blur(6px);
  border:1px solid rgba(255,255,255,0.3);
  color:#fff;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  transition:transform .15s, background .2s;
}
.spk:hover{background:rgba(255,255,255,0.35);transform:scale(1.06)}
.tip{
  background:var(--soft);
  border-left:4px solid var(--red);
  border-radius:0 14px 14px 0;
  padding:10px 14px;
  font-size:14.5px;
  margin:12px 0;
  color:var(--sub);
}
.tip b{color:var(--text)}

/* Audio-Visual Comparative Transformation (Before -> After rule) */
.rule-card{
  background:var(--tile);
  border:1px solid var(--line);
  border-radius:20px;
  padding:16px;
  margin:12px 0;
  box-shadow:var(--card-sh);
}
.rule-flow{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  background:var(--soft);
  border-radius:14px;
  padding:12px 14px;
  margin:10px 0;
}
.rule-box{text-align:center}
.rule-box small{display:block;font-size:12px;color:var(--sub)}
.rule-box b{display:block;font-size:20px;font-weight:800}
.rule-arrow{color:var(--red);font-size:24px;font-weight:800}

/* Canvas writing pad */
.canvas-wrap{
  position:relative;
  width:100%;
  aspect-ratio:1;
  max-width:300px;
  margin:14px auto;
  background:var(--tile);
  border:2px dashed var(--line);
  border-radius:26px;
  box-shadow:var(--card-sh);
  overflow:hidden;
}
.canvas-ghost{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:160px;
  font-weight:900;
  color:rgba(0,0,0,0.06);
  pointer-events:none;
  user-select:none;
}
html.dark .canvas-ghost{color:rgba(255,255,255,0.06)}
canvas#drawPad{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  cursor:crosshair;
  touch-action:none;
}
.draw-tools{display:flex;gap:10px;justify-content:center;margin:12px 0}
.draw-tools button{
  padding:8px 14px;
  border-radius:12px;
  border:1px solid var(--line);
  background:var(--tile);
  font:inherit;
  font-size:13.5px;
  font-weight:600;
  color:var(--text);
  cursor:pointer;
}

/* Exam & Quiz Grid */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}
.opt{
  aspect-ratio:1;
  border:1px solid var(--line);
  border-radius:20px;
  background:var(--tile);
  box-shadow:var(--card-sh);
  font-size:clamp(28px,8.5vw,40px);
  font-weight:600;
  color:var(--text);
  cursor:pointer;
  transition:all .15s;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
}
.opt:hover{border-color:var(--red)}
.opt.ok{background:var(--gbg);border-color:var(--green);color:var(--green)}
.opt.bad{background:var(--rbg);border-color:var(--red);color:var(--red)}

/* Bottom navigation */
#nav{
  position:fixed;
  bottom:0;
  left:0;
  right:0;
  height:66px;
  background:var(--tile);
  border-top:1px solid var(--line);
  box-shadow:0 -6px 20px rgba(0,0,0,0.04);
  display:flex;
  align-items:center;
  justify-content:space-around;
  padding:0 8px env(safe-area-inset-bottom,0px);
  z-index:9999;
}
#nav button{
  flex:1;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  background:none;
  border:0;
  color:var(--sub);
  font:inherit;
  font-size:11.5px;
  font-weight:600;
  cursor:pointer;
  padding:6px 0;
  transition:color .15s;
}
#nav button svg{width:22px;height:22px;margin-bottom:2px;stroke:currentColor;fill:none;stroke-width:2.1}
#nav button.on{color:var(--red)}
</style>
</head>
<body>
<div id="app"></div>
<nav id="nav"></nav>
<script>
/* ========================================================
   नेपालीमा हाङ्गुल — Complete Pedagogical Flow Engine
   ======================================================== */

// Global Navigation Flow Stack
let FLOW_HISTORY = ["home"];
let CURRENT_STEP = 1;

// Korean Alphabet Data
const VOWELS_BASIC = [
  ["ㅏ","आ","a","मुख राम्रोसँग खोलेर 'आ'"],
  ["ㅑ","या","ya","नेपाली 'या'"],
  ["ㅓ","अ","eo","मुख सामान्य खोलेर स्वाभाविक 'अ'"],
  ["ㅕ","य","yeo","नेपाली 'य'"],
  ["ㅗ","ओ","o","ओठ गोलो बनाएर 'ओ'"],
  ["ㅛ","यो","yo","नेपाली 'यो'"],
  ["ㅜ","उ","u","ओठ अगाडि चुच्चो पारेर 'उ'"],
  ["ㅠ","यु","yu","नेपाली 'यु'"],
  ["ㅡ","उ/इ","eu","दाँत जोडेर जिब्रो पछाडि तानी निकालिने स्वर"],
  ["ㅣ","इ","i","नेपाली 'इ'"]
];

const VOWELS_COMPOUND = [
  ["ㅐ","ए (ऐ)","ae","मुख चौडा पारेर 'ए'"],
  ["ㅒ","ये","yae","नेपाली 'ये'"],
  ["ㅔ","ए","e","नेपाली 'ए'"],
  ["ㅖ","ये","ye","नेपाली 'ये'"],
  ["ㅘ","वा","wa","ㅗ + ㅏ = वा"],
  ["ㅙ","वे","wae","ㅗ + ㅐ = वे"],
  ["ㅚ","वे","oe","ㅗ + ㅣ = वे"],
  ["ㅝ","व","wo","ㅜ + ㅓ = व"],
  ["ㅞ","वे","we","ㅜ + ㅔ = वे"],
  ["ㅟ","वि","wi","ㅜ + ㅣ = वि"],
  ["ㅢ","उइ","ui","ㅡ + ㅣ = उइ वा इ"]
];

const CONSONANTS_BASIC = [
  ["ㄱ","ख / ग","g/k","शब्दको सुरुमा 'ख', बीचमा 'ग'"],
  ["ㄴ","न","n","नेपाली 'न'"],
  ["ㄷ","थ / द","d/t","शब्दको सुरुमा 'थ', बीचमा 'द'"],
  ["ㄹ","र / ल","r/l","सुरु/बीचमा 'र', अन्त्यमा 'ल'"],
  ["ㅁ","म","m","नेपाली 'म'"],
  ["ㅂ","फ / ब","b/p","शब्दको सुरुमा 'फ', बीचमा 'ब'"],
  ["ㅅ","स / शि","s","नेपाली 'स'"],
  ["ㅇ","मौन / ङ","ng","सुरुमा मौन, अन्त्यमा 'ङ'"],
  ["ㅈ","छ / ज","j/ch","शब्दको सुरुमा 'छ', बीचमा 'ज'"],
  ["ㅊ","छ (कडा)","ch","कडा सास फालेर बोलिने 'छ'"],
  ["ㅋ","ख (कडा)","k","कडा सास फालेर बोलिने 'ख'"],
  ["ㅌ","थ (कडा)","t","कडा सास फालेर बोलिने 'थ'"],
  ["ㅍ","फ (कडा)","p","कडा सास फालेर बोलिने 'फ'"],
  ["ㅎ","ह","h","नेपाली 'ह'"]
];

const CONSONANTS_DOUBLE = [
  ["ㄲ","क","kk","घाँटीमा बल दिएर बोलिने कडा 'क'"],
  ["ㄸ","त","tt","जिब्रो दाँतमा ठोकेर बोलिने कडा 'त'"],
  ["ㅃ","प","pp","ओठ थिचेर निकालिने कडा 'प'"],
  ["ㅆ","स","ss","कडा 'स'"],
  ["ㅉ","च","jj","कडा 'च'"]
];

const CI = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
const VI = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"];
const FI = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];

const syl = (c, v) => String.fromCharCode(0xAC00 + (CI.indexOf(c) * 21 + VI.indexOf(v)) * 28);
const syl3 = (c, v, f) => String.fromCharCode(0xAC00 + (CI.indexOf(c) * 21 + VI.indexOf(v)) * 28 + FI.indexOf(f));

// Active Selection States
let SEL_VOWEL = VOWELS_BASIC[0];
let SEL_CONS = CONSONANTS_BASIC[0];
let LR = { c: "ㄱ", v: "ㅏ" };
let BR = { c: "ㄱ", v: "ㅏ", f: "ㄱ" };
let DRAW_TARGET = "가";

// Audio Utterance
let _audio = null;
function say(txt) {
  try {
    if ("speechSynthesis" in window && window.SpeechSynthesisUtterance) {
      const vs = speechSynthesis.getVoices();
      const kv = vs.find(x => x.lang === "ko-KR" || x.lang === "ko_KR" || /^ko/i.test(x.lang));
      const u = new SpeechSynthesisUtterance(txt);
      u.lang = "ko-KR";
      u.rate = 0.82;
      if (kv) u.voice = kv;
      let started = false;
      u.onstart = () => { started = true; };
      u.onerror = () => { if (!started) sayWeb(txt); };
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
      setTimeout(() => {
        if (!started && !speechSynthesis.speaking) {
          speechSynthesis.cancel();
          sayWeb(txt);
        }
      }, 550);
      return;
    }
  } catch (e) {}
  sayWeb(txt);
}
function sayWeb(txt) {
  try {
    if (_audio) { _audio.pause(); _audio = null; }
    const au = new Audio("https://translate.google.com/translate_tts?ie=UTF-8&tl=ko&client=tw-ob&q=" + encodeURIComponent(txt));
    _audio = au;
    au.play().catch(e => {});
  } catch (e) {}
}

// Navigation Flow Control
function navigateTo(screenId) {
  if (FLOW_HISTORY[FLOW_HISTORY.length - 1] !== screenId) {
    FLOW_HISTORY.push(screenId);
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
  renderApp();
}

function goBack() {
  if (FLOW_HISTORY.length > 1) {
    FLOW_HISTORY.pop();
    const prev = FLOW_HISTORY[FLOW_HISTORY.length - 1];
    window.scrollTo({ top: 0, behavior: "smooth" });
    renderApp();
  } else {
    FLOW_HISTORY = ["home"];
    renderApp();
  }
}

function currentScreen() {
  return FLOW_HISTORY[FLOW_HISTORY.length - 1] || "home";
}

/* ========================================================
   VIEWS: Guided Step-by-Step Architecture
   ======================================================== */

// Top Bar with Breadcrumbs & Back
function renderTopBar(stepNumber, stepTitle) {
  return `
    <div class="top-bar">
      <button class="back-btn" onclick="goBack()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        फर्कनुहोस्
      </button>
      <span class="step-badge">चरण ${stepNumber}: ${stepTitle}</span>
    </div>
  `;
}

// Home: Master Curriculum Roadmap
function viewHome() {
  const steps = [
    { num: 1, id: "vowels", title: "स्वरवर्ण (Vowels)", desc: "१० मूल स्वर र ११ संयुक्त स्वरहरूको उच्चारण", icon: "ㅏ", tag: "पहिलो आधार" },
    { num: 2, id: "consonants", title: "व्यञ्जनवर्ण (Consonants)", desc: "१४ मूल व्यञ्जन र ५ कडा (तनावयुक्त) व्यञ्जन", icon: "ㄱ", tag: "दोस्रो आधार" },
    { num: 3, id: "syllables", title: "अक्षर निर्माण (Syllables)", desc: "स्वर र व्यञ्जन जोडेर बाह्रखरी जस्तै अक्षर बनाउने विधि", icon: "가", tag: "अक्षर ज्ञान" },
    { num: 4, id: "batchim", title: "फाछिम (Batchim 받침)", desc: "अक्षरको फेदमा झुण्डिने व्यञ्जनका ७ ध्वनि नियमहरू", icon: "한", tag: "अति महत्वपूर्ण" },
    { num: 5, id: "reading_rules", title: "वाचनका ५ सुनौला नियम", desc: "लेखाइ र बोलाइ फरक पर्ने ध्वनि परिवर्तनका नियमहरू", icon: "입", tag: "शुद्ध उच्चारण" },
    { num: 6, id: "numbers", title: "कोरियन गन्ती र पैसा (Won)", desc: "सिनो कोरियन, मौलिक कोरियन र किनमेल गन्ती", icon: "일", tag: "दैनिक जीवन" },
    { num: 7, id: "vocabulary", title: "दैनिक तथा EPS शब्दभण्डार", desc: "कारखाना, खाना, अस्पताल र यातायात शब्दहरू", icon: "단", tag: "शब्द ज्ञान" },
    { num: 8, id: "grammar", title: "नेपाली-कोरियन व्याकरण सेतु", desc: "SOV वाक्य रचना, विभक्ति र क्रियापद रूपान्तरण", icon: "문", tag: "वाक्य कला" },
    { num: 9, id: "writing_studio", title: "हातले लेख्ने अभ्यास (Canvas)", desc: "स्क्रिनमा औंला वा माउसले अक्षर लेख्ने अभ्यास", icon: "✍", tag: "लेखन कला" },
    { num: 10, id: "quiz", title: "क्विज तथा आत्ममूल्याङ्कन", desc: "आवाज सुनेर अक्षर चिन्ने र अभ्यास गर्ने परीक्षा", icon: "✓", tag: "जाँच" }
  ];

  return `
    <div class="title">नेपालीमा <em>हाङ्गुल</em> <span>मार्गचित्र</span></div>
    <div class="hero">
      <small>सिकाइको व्यवस्थित यात्रा</small>
      <div class="hv">० बाट सुरु गरौं</div>
      <p style="margin:6px 0 0;font-size:15px;opacity:0.95">तल दिइएका १० वटा चरणहरू क्रमैसँग पूरा गर्नुहोस्। कुनै पनि पाइला नछुटाई सिक्दा ७ दिनमै कोरियन पढ्न र लेख्न सकिन्छ!</p>
      <div class="meter">
        <div><i style="width:30%"></i></div>
        <b>चरण १ बाट सुरु</b>
      </div>
    </div>

    <div class="head">१०-चरणे पूर्ण सिकाइ मार्गचित्र <small>क्रमबद्ध यात्रा</small></div>
    <div class="track-wrap">
      ${steps.map(s => `
        <div class="track-step ${s.num === 1 ? 'active' : ''}">
          <div class="track-line"></div>
          <div class="track-icon ko">${s.icon}</div>
          <div class="track-card" onclick="navigateTo('${s.id}')">
            <h4>${s.title} <span class="track-tag">${s.tag}</span></h4>
            <p>${s.desc}</p>
          </div>
        </div>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('vowels')">
        चरण १: स्वरवर्णबाट सुरु गर्नुहोस् →
      </button>
    </div>
  `;
}

// Step 1: Vowels
function viewVowels() {
  return `
    ${renderTopBar(1, "स्वरवर्ण (Vowels)")}
    <div class="title">१० मूल <em>स्वरवर्ण</em></div>
    <div class="hero" style="text-align:center">
      <small>हाल छनोट गरिएको स्वर:</small>
      <div class="hv ko" style="font-size:84px;margin:10px 0">${SEL_VOWEL[0]}</div>
      <div style="font-size:24px;font-weight:700">${SEL_VOWEL[1]} (${SEL_VOWEL[2]})</div>
      <p style="margin:4px 0 0;font-size:15px;opacity:0.9">${SEL_VOWEL[3]}</p>
      <button class="spk" onclick="say('${SEL_VOWEL[0]}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="seg">
      <button class="on">१० मूल स्वरवर्ण</button>
      <button onclick="navigateTo('vowels_compound')">११ संयुक्त स्वरवर्ण →</button>
    </div>

    <div class="head">स्वर छान्नुहोस् र आवाज सुन्नुहोस्:</div>
    <div class="chips">
      ${VOWELS_BASIC.map(v => `
        <button class="chip ko ${v[0] === SEL_VOWEL[0] ? 'on' : ''}" onclick="SEL_VOWEL=VOWELS_BASIC.find(x=>x[0]==='${v[0]}');renderApp();say('${v[0]}')">
          ${v[0]} (${v[1]})
        </button>
      `).join("")}
    </div>

    <div class="tip">
      <b>💡 नेपाली भाषाको शक्ति:</b> कोरियन स्वर <b>ㅓ (eo)</b> र <b>ㅗ (o)</b> मा धेरै विदेशी झुक्किन्छन्। तर नेपालीमा <b>ㅓ = स्वाभाविक 'अ'</b> (जस्तै 'घर' को अ) र <b>ㅗ = ओठ गोलो पारेर निकालिने 'ओ'</b> (जस्तै 'ओढ्ने' को ओ) हो!
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('consonants')">
        अर्को चरण: व्यञ्जनवर्ण सिक्नुहोस् (Step 2) →
      </button>
      <button class="flow-btn ghost" onclick="DRAW_TARGET='${SEL_VOWEL[0]}';navigateTo('writing_studio')">
        ✍ यो स्वर हातले कोरेर अभ्यास गर्नुहोस्
      </button>
    </div>
  `;
}

// Step 1b: Compound Vowels
function viewVowelsCompound() {
  return `
    ${renderTopBar(1, "संयुक्त स्वर (Compound Vowels)")}
    <div class="title">११ संयुक्त <em>स्वरवर्ण</em></div>
    <div class="hero" style="text-align:center">
      <small>संयुक्त स्वर:</small>
      <div class="hv ko" style="font-size:84px;margin:10px 0">${SEL_VOWEL[0]}</div>
      <div style="font-size:24px;font-weight:700">${SEL_VOWEL[1]} (${SEL_VOWEL[2]})</div>
      <p style="margin:4px 0 0;font-size:15px;opacity:0.9">${SEL_VOWEL[3]}</p>
      <button class="spk" onclick="say('${SEL_VOWEL[0]}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="seg">
      <button onclick="navigateTo('vowels')">← १० मूल स्वरवर्ण</button>
      <button class="on">११ संयुक्त स्वरवर्ण</button>
    </div>

    <div class="head">संयुक्त स्वर छान्नुहोस्:</div>
    <div class="chips">
      ${VOWELS_COMPOUND.map(v => `
        <button class="chip ko ${v[0] === SEL_VOWEL[0] ? 'on' : ''}" onclick="SEL_VOWEL=VOWELS_COMPOUND.find(x=>x[0]==='${v[0]}');renderApp();say('${v[0]}')">
          ${v[0]} (${v[1]})
        </button>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('consonants')">
        अर्को चरण: व्यञ्जनवर्ण सिक्नुहोस् (Step 2) →
      </button>
    </div>
  `;
}

// Step 2: Consonants
function viewConsonants() {
  return `
    ${renderTopBar(2, "व्यञ्जनवर्ण (Consonants)")}
    <div class="title">१४ मूल <em>व्यञ्जनवर्ण</em></div>
    <div class="hero" style="text-align:center">
      <small>व्यञ्जनवर्ण:</small>
      <div class="hv ko" style="font-size:84px;margin:10px 0">${SEL_CONS[0]}</div>
      <div style="font-size:24px;font-weight:700">${SEL_CONS[1]}</div>
      <p style="margin:4px 0 0;font-size:15px;opacity:0.9">${SEL_CONS[3]}</p>
      <button class="spk" onclick="say('${SEL_CONS[0]}ㅏ')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="seg">
      <button class="on">१४ मूल व्यञ्जन</button>
      <button onclick="navigateTo('consonants_double')">५ कडा व्यञ्जन (Double) →</button>
    </div>

    <div class="head">व्यञ्जन छान्नुहोस् र स्थान हेर्नुहोस्:</div>
    <div class="chips">
      ${CONSONANTS_BASIC.map(c => `
        <button class="chip ko ${c[0] === SEL_CONS[0] ? 'on' : ''}" onclick="SEL_CONS=CONSONANTS_BASIC.find(x=>x[0]==='${c[0]}');renderApp();say('${c[0]}ㅏ')">
          ${c[0]} (${c[1]})
        </button>
      `).join("")}
    </div>

    <div class="tip">
      <b>💡 स्थान भेदको नियम:</b> कोरियन व्यञ्जन <b>ㄱ, ㄷ, ㅂ, ㅈ</b> शब्दको सुरुमा आउँदा नेपालीको महाप्राण (ख, थ, फ, छ) जस्तो बोलिन्छ, तर शब्दको बीच वा अन्त्यमा आउँदा अल्पप्राण (ग, द, ब, ज) सुनिन्छ!
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('syllables')">
        अर्को चरण: अक्षर बनाउने विधि (Step 3) →
      </button>
      <button class="flow-btn ghost" onclick="DRAW_TARGET='${SEL_CONS[0]}';navigateTo('writing_studio')">
        ✍ यो व्यञ्जन हातले लेख्नुहोस्
      </button>
    </div>
  `;
}

// Step 2b: Double Consonants
function viewConsonantsDouble() {
  return `
    ${renderTopBar(2, "कडा व्यञ्जन (Double Consonants)")}
    <div class="title">५ कडा <em>व्यञ्जनवर्ण</em></div>
    <div class="hero" style="text-align:center">
      <small>कडा (तनावयुक्त) व्यञ्जन:</small>
      <div class="hv ko" style="font-size:84px;margin:10px 0">${SEL_CONS[0]}</div>
      <div style="font-size:24px;font-weight:700">${SEL_CONS[1]}</div>
      <p style="margin:4px 0 0;font-size:15px;opacity:0.9">${SEL_CONS[3]}</p>
      <button class="spk" onclick="say('${SEL_CONS[0]}ㅏ')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="seg">
      <button onclick="navigateTo('consonants')">← १४ मूल व्यञ्जन</button>
      <button class="on">५ कडा व्यञ्जन</button>
    </div>

    <div class="head">कडा व्यञ्जन छान्नुहोस्:</div>
    <div class="chips">
      ${CONSONANTS_DOUBLE.map(c => `
        <button class="chip ko ${c[0] === SEL_CONS[0] ? 'on' : ''}" onclick="SEL_CONS=CONSONANTS_DOUBLE.find(x=>x[0]==='${c[0]}');renderApp();say('${c[0]}ㅏ')">
          ${c[0]} (${c[1]})
        </button>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('syllables')">
        अर्को चरण: अक्षर बनाउने विधि (Step 3) →
      </button>
    </div>
  `;
}

// Step 3: Syllables
function viewSyllables() {
  const c = CONSONANTS_BASIC.find(x => x[0] === LR.c) || CONSONANTS_BASIC[0];
  const v = VOWELS_BASIC.find(x => x[0] === LR.v) || VOWELS_BASIC[0];
  const sy = syl(c[0], v[0]);

  return `
    ${renderTopBar(3, "अक्षर निर्माण (Syllables)")}
    <div class="title">स्वर र व्यञ्जनको <em>संयोजन</em></div>
    <div class="hero" style="text-align:center">
      <small>${c[0]} (${c[1]}) + ${v[0]} (${v[1]})</small>
      <div class="hv ko" style="font-size:84px;margin:8px 0">${sy}</div>
      <div style="font-size:22px;font-weight:700">${c[2]} + ${v[2]}</div>
      <button class="spk" onclick="say('${sy}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="head">व्यञ्जन छान्नुहोस्:</div>
    <div class="chips">
      ${CONSONANTS_BASIC.map(x => `
        <button class="chip ko ${x[0] === LR.c ? 'on' : ''}" onclick="LR.c='${x[0]}';renderApp();say('${syl(x[0], LR.v)}')">${x[0]}</button>
      `).join("")}
    </div>

    <div class="head">स्वर छान्नुहोस्:</div>
    <div class="chips">
      ${VOWELS_BASIC.map(x => `
        <button class="chip ko ${x[0] === LR.v ? 'on' : ''}" onclick="LR.v='${x[0]}';renderApp();say('${syl(LR.c, x[0])}')">${x[0]}</button>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('batchim')">
        अर्को चरण: फाछिम नियम सिक्नुहोस् (Step 4) →
      </button>
      <button class="flow-btn ghost" onclick="DRAW_TARGET='${sy}';navigateTo('writing_studio')">
        ✍ यो अक्षर हातले लेख्ने अभ्यास गर्नुहोस्
      </button>
    </div>
  `;
}

// Step 4: Batchim
function viewBatchim() {
  const FIN = [
    ["ㄱ","k","क आवाज (ㄱ, ㅋ, ㄲ, ㄳ, ㄺ)","उदा: 책 (छेक=किताब), सुबाक (खरबुजा)"],
    ["ㄴ","n","न आवाज (ㄴ, ㄵ, ㄶ)","उदा: 눈 (नुन=आँखा/हिउँ), सान (पहाड)"],
    ["ㄷ","t","त आवाज (ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ)","उदा: 옷 (ओत=कपडा), कोत (फूल)"],
    ["ㄹ","l","ल आवाज (ㄹ, ㄼ, ㄽ, ㄾ, ㅀ)","उदा: 물 (मुल=पानी), दाल (चन्द्रमा)"],
    ["ㅁ","m","म आवाज (ㅁ, ㄻ)","उदा: 밤 (बाम=रात), माइम (मन)"],
    ["ㅂ","p","प आवाज (ㅂ, ㅍ, ㅄ, ㄿ)","उदा: 밥 (बाप=भात), चिप (घर)"],
    ["ㅇ","ng","ङ आवाज (ㅇ)","उदा: 강 (गाङ=नदी), बाङ (कोठा)"]
  ];
  const f = FIN.find(x => x[0] === BR.f) || FIN[0];
  const sy = syl3(BR.c, BR.v, f[0]);

  return `
    ${renderTopBar(4, "फाछिम (Batchim 받침)")}
    <div class="title">अन्तिम व्यञ्जन <em>(받침)</em></div>
    <div class="hero" style="text-align:center">
      <small>${BR.c} + ${BR.v} + तल्लो व्यञ्जन (${f[0]})</small>
      <div class="hv ko" style="font-size:80px;margin:8px 0">${sy}</div>
      <div style="font-size:22px;font-weight:700">${f[2]}</div>
      <button class="spk" onclick="say('${sy}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="head">७ मुख्य फाछिम ध्वनि समूह छान्नुहोस्:</div>
    <div class="chips">
      ${FIN.map(x => `
        <button class="chip ko ${x[0] === BR.f ? 'on' : ''}" onclick="BR.f='${x[0]}';renderApp();say('${syl3(BR.c, BR.v, x[0])}')">
          ${x[0]} (${x[1]})
        </button>
      `).join("")}
    </div>

    <div class="tile" style="margin-top:14px">
      <p style="font-size:16.5px;font-weight:700;color:var(--red);margin:0 0 4px">${f[0]} को नियम: ${f[2]}</p>
      <p style="font-size:15px;margin:0">${f[3]}</p>
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('reading_rules')">
        अर्को चरण: वाचनका ५ नियमहरू (Step 5) →
      </button>
    </div>
  `;
}

// Step 5: Reading & Sound Change Rules
function viewReadingRules() {
  const rules = [
    {
      name: "१. 연음 (सरेर जोडिने नियम - Liaison)",
      desc: "तल्लो फाछिम पछि स्वर (ㅇ) आएमा फाछिम खाली ठाउँमा सरेर उच्चारण हुन्छ।",
      before: "한국어",
      after: "[ हान्गुग ]",
      meaning: "कोरियन भाषा (हान्-गुक्-अ होइन)"
    },
    {
      name: "२. 비음화 (नासिक्यीकरण - Nasalization)",
      desc: "ㅂ, ㄷ, ㄱ पछि ㄴ वा ㅁ आएमा ㅂ को उच्चारण 'म' र ㄱ को उच्चारण 'ङ' हुन्छ।",
      before: "감사합니다",
      after: "[ खामसाम्निदा ]",
      meaning: "धन्यवाद (खामसाहब्निदा होइन)"
    },
    {
      name: "३. 격음화 (ह सँग जोडिँदा महाप्राण - Aspiration)",
      desc: "ㄱ, ㄷ, ㅂ, ㅈ अगाडि वा पछाडि ㅎ आएमा ख, थ, फ, छ बन्दछन्।",
      before: "축하",
      after: "[ छुखा ]",
      meaning: "बधाई (छुक-हा होइन)"
    },
    {
      name: "४. 경음화 (कडा हुने नियम - Tensification)",
      desc: "दुई व्यञ्जन ठोकिँदा पछिल्लो व्यञ्जन कडा (ㄲ, ㄸ, ㅃ, ㅆ, ㅉ) उच्चारण हुन्छ।",
      before: "학교",
      after: "[ हाक्क्यो ]",
      meaning: "विद्यालय"
    }
  ];

  return `
    ${renderTopBar(5, "वाचनका ५ सुनौला नियम")}
    <div class="title">उच्चारणका <em>५ सुनौला नियम</em></div>
    <p class="sub" style="color:var(--sub);margin:0 0 12px">यी नियमहरू जानेपछि तपाईंले जुनसुकै कोरियन शब्द पनि स्वदेशी कोरियन नागरिकले जस्तै शुद्ध पढ्न सक्नुहुन्छ:</p>

    ${rules.map(r => `
      <div class="rule-card">
        <h4 style="margin:0 0 4px;font-size:17.5px;color:var(--red)">${r.name}</h4>
        <p style="margin:0;font-size:14.5px;color:var(--sub)">${r.desc}</p>
        <div class="rule-flow">
          <div class="rule-box">
            <small>लेखाइ (Text)</small>
            <b class="ko">${r.before}</b>
          </div>
          <div class="rule-arrow">➔</div>
          <div class="rule-box">
            <small>बोलाइ (Sound)</small>
            <b class="ko" style="color:var(--red)">${r.after}</b>
          </div>
          <button class="chip" onclick="say('${r.before}')" style="margin:0">🔊</button>
        </div>
        <small style="color:var(--sub)">अर्थ: ${r.meaning}</small>
      </div>
    `).join("")}

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('numbers')">
        अर्को चरण: कोरियन गन्ती र पैसा (Step 6) →
      </button>
    </div>
  `;
}

// Step 6: Numbers
function viewNumbers() {
  return `
    ${renderTopBar(6, "कोरियन गन्ती र पैसा")}
    <div class="title">कोरियन <em>गन्ती प्रणाली</em></div>
    <div class="seg">
      <button class="on" id="tabS" onclick="setNumTab('S')">सिनो कोरियन (일,이,삼)</button>
      <button id="tabN" onclick="setNumTab('N')">मौलिक कोरियन (하나,둘)</button>
    </div>

    <div id="numContent" style="margin-top:14px"></div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('vocabulary')">
        अर्को चरण: दैनिक तथा EPS शब्दभण्डार (Step 7) →
      </button>
    </div>
  `;
}

let CURRENT_NUM_MODE = "S";
function setNumTab(mode) {
  CURRENT_NUM_MODE = mode;
  document.getElementById("tabS").classList.toggle("on", mode === "S");
  document.getElementById("tabN").classList.toggle("on", mode === "N");
  renderNumContent();
}

function renderNumContent() {
  const el = document.getElementById("numContent");
  if (!el) return;
  if (CURRENT_NUM_MODE === "S") {
    el.innerHTML = `
      <div class="tip"><b>सिनो कोरियन (일, 이, 삼):</b> मिति, मिनेट, फोन नम्बर र पैसा (वोन) गन्ती गर्दा प्रयोग हुन्छ।</div>
      <div class="list">
        ${[
          ["일","il","१ (एक)","इल"],
          ["이","i","२ (दुई)","इ"],
          ["삼","sam","३ (तीन)","साम"],
          ["사","sa","४ (चार)","सा"],
          ["오","o","५ (पाँच)","ओ"],
          ["십","sip","१० (दश)","शिप"],
          ["백","baek","१०० (सय)","बेक"],
          ["천","cheon","१,००० (हजार)","छन"],
          ["만","man","१०,००० (मान)","मान"]
        ].map(n => `
          <div class="lrow" onclick="say('${n[0]}')">
            <span class="ln ko">${n[0]}</span>
            <span class="lt"><b>${n[2]}</b><small>${n[3]} (${n[1]})</small></span>
            <span class="lg">🔊</span>
          </div>
        `).join("")}
      </div>
    `;
  } else {
    el.innerHTML = `
      <div class="tip"><b>मौलिक कोरियन (하나, 둘, 셋):</b> वस्तु, उमेर, मानिस र घडीको घण्टा गन्ती गर्दा प्रयोग हुन्छ।</div>
      <div class="list">
        ${[
          ["하나","hana","१ (एउटा)","हाना"],
          ["둘","dul","२ (दुइटा)","दुल"],
          ["셋","set","३ (तीनवटा)","सेत"],
          ["넷","net","४ (चारवटा)","नेत"],
          ["다섯","daseot","५ (पाँचवटा)","थासत"],
          ["열","yeol","१० (दशवटा)","योल"],
          ["스물","seumul","२० (बीसवटा)","सुमुल"]
        ].map(n => `
          <div class="lrow" onclick="say('${n[0]}')">
            <span class="ln ko">${n[0]}</span>
            <span class="lt"><b>${n[2]}</b><small>${n[3]} (${n[1]})</small></span>
            <span class="lg">🔊</span>
          </div>
        `).join("")}
      </div>
    `;
  }
}

// Step 7: Vocabulary
function viewVocabulary() {
  const words = [
    { ko: "안녕하세요", ne: "नमस्ते / नमस्कार", pron: "आन्न्योङ हासेयो", cat: "अभिवादन" },
    { ko: "감사합니다", ne: "धन्यवाद", pron: "खामसाम्निदा", cat: "सभ्यता" },
    { ko: "죄송합니다", ne: "माफ गर्नुहोस्", pron: "छेसोङ हाम्निदा", cat: "सभ्यता" },
    { ko: "공장", ne: "कारखाना / फ्याक्ट्री", pron: "खोङजाङ", cat: "EPS" },
    { ko: "작업", ne: "काम / कार्य", pron: "छागप", cat: "EPS" },
    { ko: "월급", ne: "मासिक तलब", pron: "वल्गुप", cat: "EPS" },
    { ko: "안전모", ne: "सुरक्षा हेलमेट", pron: "आन्जनमो", cat: "सुरक्षा" },
    { ko: "물 주세요", ne: "पानी दिनुहोस्", pron: "मुल छुसेयो", cat: "रेस्टुरेन्ट" },
    { ko: "얼마예요?", ne: "कति रुपैयाँ हो?", pron: "ओलमायेयो?", cat: "बजार" }
  ];

  return `
    ${renderTopBar(7, "दैनिक तथा EPS शब्दभण्डार")}
    <div class="title">महत्वपूर्ण <em>शब्दार्थ</em></div>
    <div class="tip">प्रत्येक शब्दमा छुँदा शुद्ध कोरियन उच्चारण सुन्न सकिन्छ:</div>
    <div class="list">
      ${words.map(w => `
        <div class="lrow" onclick="say('${w.ko}')">
          <span class="ln ko" style="font-size:18px">▶</span>
          <span class="lt">
            <b class="ko" style="font-size:19px">${w.ko}</b>
            <small style="font-size:15px;color:var(--text)">${w.ne}</small>
            <small style="color:var(--sub)">[${w.pron}] · <span style="color:var(--red)">${w.cat}</span></small>
          </span>
          <span class="lg">🔊</span>
        </div>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('grammar')">
        अर्को चरण: नेपाली-कोरियन व्याकरण सेतु (Step 8) →
      </button>
    </div>
  `;
}

// Step 8: Grammar
function viewGrammar() {
  return `
    ${renderTopBar(8, "नेपाली-कोरियन व्याकरण सेतु")}
    <div class="title">नेपाली र कोरियन <em>व्याकरण</em></div>
    
    <div class="rule-card">
      <h4 style="margin:0 0 6px;color:var(--red);font-size:18px">१. वाक्य संरचना (SOV Structure)</h4>
      <p style="margin:0 0 8px;font-size:14.5px;color:var(--sub)">नेपाली र कोरियन वाक्य संरचना १००% एकै हो:</p>
      <div style="background:var(--soft);padding:10px 14px;border-radius:12px;font-size:15px">
        <b>म (S) + कोरियन भाषा (O) + सिक्छु (V)।</b><br>
        <span class="ko" style="color:var(--red);font-weight:700">저는 한국어를 배워요.</span>
      </div>
    </div>

    <div class="rule-card">
      <h4 style="margin:0 0 6px;color:var(--red);font-size:18px">२. विभक्तिहरू (Particles - 조사)</h4>
      <div style="font-size:14.5px;line-height:1.7">
        • <b>은 / 는</b> = त / चाहिं (विषय)<br>
        • <b>이 / 가</b> = ले (कर्ता कारक)<br>
        • <b>을 / 를</b> = लाई (कर्म कारक)<br>
        • <b>에 / 에서</b> = मा / बाट (स्थान कारक)
      </div>
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('writing_studio')">
        अर्को चरण: हातले लेख्ने अभ्यास (Step 9) →
      </button>
    </div>
  `;
}

// Step 9: Writing Studio
function viewWritingStudio() {
  setTimeout(initCanvas, 50);
  return `
    ${renderTopBar(9, "हातले लेख्ने अभ्यास")}
    <div class="title">हातले <em>लेख्ने</em> क्यानभास</div>
    <div style="text-align:center;margin:6px 0">
      <span style="font-size:15px;color:var(--sub)">अभ्यास वर्ण: </span>
      <b class="ko" style="font-size:32px;color:var(--red)">${DRAW_TARGET}</b>
      <button class="chip" onclick="say('${DRAW_TARGET}')" style="margin-left:8px">🔊</button>
    </div>

    <div class="canvas-wrap">
      <div class="canvas-ghost ko" id="ghostChar">${DRAW_TARGET}</div>
      <canvas id="drawPad" width="300" height="300"></canvas>
    </div>

    <div class="draw-tools">
      <button onclick="clearCanvas()">मेटाउनुहोस् (Clear)</button>
      <button onclick="changeDrawTarget()">अर्को वर्ण (Next)</button>
    </div>

    <div class="flow-actions">
      <button class="flow-btn" onclick="navigateTo('quiz')">
        अन्तिम चरण: आत्ममूल्याङ्कन परीक्षा (Step 10) →
      </button>
    </div>
  `;
}

// Step 10: Quiz & Evaluation
let QUIZ_SCORE = 0;
let QUIZ_CURRENT = 0;
let QUIZ_LOCKED = false;
let QUIZ_ITEMS = [];

function viewQuiz() {
  if (QUIZ_ITEMS.length === 0) startQuiz();
  const q = QUIZ_ITEMS[QUIZ_CURRENT];
  const progress = Math.round((QUIZ_CURRENT / 10) * 100);

  return `
    ${renderTopBar(10, "आत्ममूल्याङ्कन क्विज")}
    <div class="title">सुनाइ तथा <em>अक्षर परीक्षा</em></div>
    <div class="hero">
      <small>प्रश्नोत्तर (${QUIZ_CURRENT + 1} / 10)</small>
      <div class="hv">${QUIZ_SCORE} अंक</div>
      <div class="meter">
        <div><i style="width:${progress}%"></i></div>
        <b>${progress}%</b>
      </div>
    </div>

    <div style="text-align:center;margin:20px 0 10px">
      <p style="font-size:15px;color:var(--sub);margin:0">आवाज सुन्नुहोस् र सही अक्षर रोज्नुहोस्:</p>
      <button class="flow-btn" style="margin:10px auto;width:auto;padding:10px 22px" onclick="say('${q.answer}')">
        🔊 उच्चारण सुन्नुहोस्
      </button>
    </div>

    <div class="grid">
      ${q.options.map(opt => `
        <button class="opt ko" onclick="checkQuizAnswer(this, '${opt}', '${q.answer}')">
          ${opt}
        </button>
      `).join("")}
    </div>

    <div class="flow-actions">
      <button class="flow-btn ghost" onclick="navigateTo('home')">
        मार्गचित्रमा फर्कनुहोस्
      </button>
    </div>
  `;
}

function startQuiz() {
  const pool = ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅇ","ㅈ","ㅎ","ㅏ","ㅓ","ㅗ","ㅜ","ㅡ","ㅣ","가","나","다","라"];
  QUIZ_ITEMS = [];
  QUIZ_SCORE = 0;
  QUIZ_CURRENT = 0;
  QUIZ_LOCKED = false;
  for (let i = 0; i < 10; i++) {
    const ans = pool[Math.floor(Math.random() * pool.length)];
    const opts = [ans];
    while (opts.length < 3) {
      const r = pool[Math.floor(Math.random() * pool.length)];
      if (!opts.includes(r)) opts.push(r);
    }
    opts.sort(() => Math.random() - 0.5);
    QUIZ_ITEMS.push({ answer: ans, options: opts });
  }
}

function checkQuizAnswer(btn, sel, correct) {
  if (QUIZ_LOCKED) return;
  QUIZ_LOCKED = true;
  if (sel === correct) {
    btn.classList.add("ok");
    QUIZ_SCORE += 10;
  } else {
    btn.classList.add("bad");
  }
  setTimeout(() => {
    QUIZ_CURRENT++;
    QUIZ_LOCKED = false;
    if (QUIZ_CURRENT >= 10) {
      alert("परीक्षा सम्पन्न भयो! तपाईंको अंक: " + QUIZ_SCORE + " / 100");
      startQuiz();
      navigateTo("home");
    } else {
      renderApp();
    }
  }, 850);
}

// Canvas Implementation
let isDrawing = false;
let canvasCtx = null;
function initCanvas() {
  const cvs = document.getElementById("drawPad");
  if (!cvs) return;
  canvasCtx = cvs.getContext("2d");
  canvasCtx.strokeStyle = "#e11d2e";
  canvasCtx.lineWidth = 14;
  canvasCtx.lineCap = "round";
  canvasCtx.lineJoin = "round";

  const getPos = e => {
    const rect = cvs.getBoundingClientRect();
    const scaleX = cvs.width / rect.width;
    const scaleY = cvs.height / rect.height;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: (clientX - rect.left) * scaleX, y: (clientY - rect.top) * scaleY };
  };

  cvs.onmousedown = cvs.ontouchstart = e => {
    e.preventDefault();
    isDrawing = true;
    const p = getPos(e);
    canvasCtx.beginPath();
    canvasCtx.moveTo(p.x, p.y);
  };
  cvs.onmousemove = cvs.ontouchmove = e => {
    if (!isDrawing) return;
    e.preventDefault();
    const p = getPos(e);
    canvasCtx.lineTo(p.x, p.y);
    canvasCtx.stroke();
  };
  window.onmouseup = window.ontouchend = () => { isDrawing = false; };
}
function clearCanvas() {
  const cvs = document.getElementById("drawPad");
  if (cvs && canvasCtx) canvasCtx.clearRect(0, 0, cvs.width, cvs.height);
}
function changeDrawTarget() {
  const chars = ["가","나","다","라","마","바","사","아","자","차","카","타","파","하","한","글","밥","물","산","강"];
  DRAW_TARGET = chars[Math.floor(Math.random() * chars.length)];
  renderApp();
}

// Bottom Navigation Bar
function renderBottomNav() {
  const nav = document.getElementById("nav");
  const s = currentScreen();
  const items = [
    { id: "home", label: "मार्गचित्र", icon: '<path d="M3 10.5L12 3l9 7.5v9.5a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>' },
    { id: "vowels", label: "कखरा", icon: '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M6 6h10M6 10h10"/>' },
    { id: "reading_rules", label: "उच्चारण", icon: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>' },
    { id: "vocabulary", label: "शब्दार्थ", icon: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>' },
    { id: "quiz", label: "क्विज", icon: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>' }
  ];
  nav.innerHTML = items.map(it => `
    <button class="${s === it.id ? 'on' : ''}" onclick="navigateTo('${it.id}')">
      <svg viewBox="0 0 24 24">${it.icon}</svg>
      <span>${it.label}</span>
    </button>
  `).join("");
}

// Master Render Dispatcher
function renderApp() {
  const app = document.getElementById("app");
  const s = currentScreen();
  renderBottomNav();

  if (s === "home") app.innerHTML = viewHome();
  else if (s === "vowels") app.innerHTML = viewVowels();
  else if (s === "vowels_compound") app.innerHTML = viewVowelsCompound();
  else if (s === "consonants") app.innerHTML = viewConsonants();
  else if (s === "consonants_double") app.innerHTML = viewConsonantsDouble();
  else if (s === "syllables") app.innerHTML = viewSyllables();
  else if (s === "batchim") app.innerHTML = viewBatchim();
  else if (s === "reading_rules") app.innerHTML = viewReadingRules();
  else if (s === "numbers") { app.innerHTML = viewNumbers(); setTimeout(renderNumContent, 10); }
  else if (s === "vocabulary") app.innerHTML = viewVocabulary();
  else if (s === "grammar") app.innerHTML = viewGrammar();
  else if (s === "writing_studio") app.innerHTML = viewWritingStudio();
  else if (s === "quiz") app.innerHTML = viewQuiz();
}

// Boot
renderApp();
</script>
</body>
</html>
'''

with open('/home/manish/projects/nepalihangul/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Flow update complete. Written to /home/manish/projects/nepalihangul/index.html")
