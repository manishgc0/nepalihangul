# -*- coding: utf-8 -*-
import json
import os

html_content = r'''<!DOCTYPE html>
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
  --bg:#fafafa;
  --surface:#ffffff;
  --surface-2:#f4f4f5;
  --text:#141414;
  --muted:#71717a;
  --line:#e6e6e7;
  --accent:#c9182a;
  --accent-soft:#fdf1f2;
  --ok:#16794a;
  --ok-soft:#eff8f3;
  --hero-bg:#151516;
  --hero-text:#fafafa;
  --hero-line:rgba(255,255,255,0.14);
  --hero-soft:rgba(255,255,255,0.10);
  --r:10px;
  --r-sm:8px;
  --r-lg:14px;
  /* legacy aliases referenced by inline styles */
  --red:var(--accent);
  --sub:var(--muted);
  --tile:var(--surface);
  --soft:var(--surface-2);
  --fill:var(--surface-2);
  --green:var(--ok);
  --gbg:var(--ok-soft);
  --rbg:var(--accent-soft);
  --tint:var(--accent-soft);
  color-scheme:light;
}
html.dark{
  color-scheme:dark;
  background:#0c0c0d;
  --bg:#0c0c0d;
  --surface:#151516;
  --surface-2:#1c1c1e;
  --text:#f4f4f5;
  --muted:#9b9ba1;
  --line:#262629;
  --accent:#ff5f66;
  --accent-soft:#221214;
  --ok:#3ecf8e;
  --ok-soft:#0f231b;
  --hero-bg:#1c1c1e;
  --hero-text:#f4f4f5;
  --hero-line:rgba(255,255,255,0.12);
  --hero-soft:rgba(255,255,255,0.08);
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:"Mukta",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:16px;
  line-height:1.55;
  -webkit-font-smoothing:antialiased;
  min-height:100vh;
  display:flex;
  justify-content:center;
  padding:28px 16px 104px;
}
#app{width:100%;max-width:468px;margin:0 auto}
.ko{font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif}

/* ---------- type ---------- */
.title{font-size:28px;font-weight:600;line-height:1.32;letter-spacing:-0.02em;margin:0 0 20px}
.title em{font-style:normal;color:var(--accent)}
.title span{color:var(--muted);font-weight:400;font-size:16px}
.head{
  font-size:15px;
  font-weight:600;
  color:var(--text);
  margin:26px 0 10px;
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap:12px;
}
.head small{font-size:12.5px;color:var(--muted);font-weight:400}
.sub{font-size:14px;line-height:1.6;margin:0 0 16px}

/* ---------- surfaces ---------- */
.tile{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.tile p{margin:0 0 6px;font-size:14px;color:var(--muted)}
.tile p:last-child{margin-bottom:0}
.tile b{color:var(--text);font-weight:600;font-size:16px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}

/* ---------- hero ---------- */
.hero{
  position:relative;
  overflow:hidden;
  background:var(--hero-bg);
  color:var(--hero-text);
  border:1px solid var(--hero-line);
  border-radius:var(--r-lg);
  padding:22px;
}
.hero small{display:block;font-size:12.5px;font-weight:500;opacity:0.6}
.hero p{opacity:0.72;font-size:14.5px;line-height:1.6;margin:8px 0 0}
.hv{font-size:30px;font-weight:600;letter-spacing:-0.02em;line-height:1.3;margin:8px 0 0}
.glyph{font-size:72px;font-weight:500;line-height:1.12;margin:14px 0 6px}
.roman{font-size:13.5px;font-weight:400;color:var(--muted);margin-top:4px}
.hero .roman{color:var(--hero-text);opacity:0.72}

/* ---------- meter ---------- */
.meter{display:flex;align-items:center;gap:12px;margin-top:18px}
.meter div{flex:1;height:4px;background:var(--hero-soft);border-radius:99px;overflow:hidden}
.meter i{display:block;height:100%;border-radius:99px;background:var(--hero-text);transition:width 0.3s ease}
.meter b{font-size:12.5px;font-weight:500;opacity:0.7;font-variant-numeric:tabular-nums}

/* ---------- segmented control ---------- */
.seg{
  display:flex;
  gap:4px;
  background:var(--surface-2);
  border:1px solid var(--line);
  border-radius:var(--r);
  padding:4px;
  margin:16px 0 0;
}
.seg button{
  flex:1 1 0;
  min-width:0;
  border:0;
  background:none;
  color:var(--muted);
  font:inherit;
  font-size:13.5px;
  font-weight:500;
  padding:8px 6px;
  border-radius:7px;
  cursor:pointer;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  transition:background 0.15s,color 0.15s;
}
.seg button.on{background:var(--surface);color:var(--text);font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,0.06)}
.seg.scroll{overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.seg.scroll::-webkit-scrollbar{display:none}
.seg.scroll button{flex:0 0 auto;min-width:max-content}

/* ---------- chips ---------- */
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0}
.chip{
  border:1px solid var(--line);
  background:var(--surface);
  border-radius:var(--r-sm);
  padding:8px 12px;
  font-size:15px;
  font-weight:500;
  color:var(--text);
  cursor:pointer;
  transition:background 0.15s,border-color 0.15s,color 0.15s;
}
.chip:hover{border-color:var(--muted)}
.chip.on{background:var(--text);color:var(--bg);border-color:var(--text)}

/* ---------- list ---------- */
.list{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;margin:0}
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
  transition:background 0.12s;
}
.lrow:last-child{border-bottom:0}
.lrow:hover{background:var(--surface-2)}
.lrow .ln{
  width:38px;
  height:38px;
  border-radius:9px;
  background:var(--surface-2);
  color:var(--text);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:17px;
  font-weight:500;
  flex-shrink:0;
}
.lrow .lt{flex:1;min-width:0}
.lrow .lt b{display:block;font-size:15px;font-weight:600;line-height:1.4}
.lrow .lt small{display:block;font-size:13px;color:var(--muted);margin-top:2px;line-height:1.45}
.lrow .lg{color:var(--muted);font-size:18px;font-weight:400;flex-shrink:0}

/* ---------- buttons ---------- */
button.primary{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  width:100%;
  background:var(--text);
  color:var(--bg);
  border:0;
  border-radius:var(--r);
  padding:13px 18px;
  font:inherit;
  font-size:15px;
  font-weight:600;
  cursor:pointer;
  transition:opacity 0.15s,transform 0.1s;
}
button.primary:hover{opacity:0.88}
button.primary:active{transform:scale(0.995)}
button.primary.ghost{background:none;color:var(--text);border:1px solid var(--line);margin-top:10px}
button.primary.ghost:hover{background:var(--surface-2);opacity:1}

.spk{
  position:absolute;
  right:18px;
  bottom:18px;
  width:40px;
  height:40px;
  border-radius:50%;
  background:var(--hero-soft);
  border:1px solid var(--hero-line);
  color:var(--hero-text);
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  transition:background 0.15s;
}
.spk:hover{background:rgba(255,255,255,0.18)}

/* ---------- misc ---------- */
.tip{
  background:var(--surface-2);
  border-left:2px solid var(--accent);
  border-radius:0 var(--r-sm) var(--r-sm) 0;
  padding:12px 14px;
  font-size:14px;
  line-height:1.6;
  margin:16px 0;
  color:var(--muted);
}
.tip b{color:var(--text);font-weight:600}

/* ---------- quiz ---------- */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}
.opt{
  aspect-ratio:1;
  border:1px solid var(--line);
  border-radius:var(--r);
  background:var(--surface);
  font-size:clamp(28px,8vw,38px);
  font-weight:500;
  color:var(--text);
  cursor:pointer;
  transition:border-color 0.15s,background 0.15s,transform 0.1s;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
}
.opt:hover{border-color:var(--muted)}
.opt:active{transform:scale(0.98)}
.opt.ok{background:var(--ok-soft);border-color:var(--ok);color:var(--ok)}
.opt.bad{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}
.opt small{font-size:12px;color:var(--muted);margin-top:2px;font-family:"Mukta",sans-serif}

.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:0}
.sc{
  border:1px solid var(--line);
  border-radius:var(--r-sm);
  background:var(--surface);
  padding:10px 4px;
  text-align:center;
  cursor:pointer;
  transition:background 0.15s,border-color 0.15s;
}
.sc:hover{border-color:var(--muted)}
.sc.on{background:var(--text);color:var(--bg);border-color:var(--text)}
.sc span{display:block;font-weight:500;font-size:15px}
.sc small{display:block;font-size:11.5px;color:var(--muted);margin-top:2px;font-variant-numeric:tabular-nums}
.sc.on small{color:var(--bg);opacity:0.65}

/* ---------- bottom navigation ---------- */
#nav{
  position:fixed;
  bottom:0;
  left:0;
  right:0;
  background:var(--surface);
  border-top:1px solid var(--line);
  display:flex;
  align-items:stretch;
  justify-content:space-around;
  padding:0 6px env(safe-area-inset-bottom,0px);
  z-index:9999;
}
#nav button{
  flex:1;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:4px;
  background:none;
  border:0;
  color:var(--muted);
  font:inherit;
  font-size:11px;
  font-weight:500;
  cursor:pointer;
  padding:12px 0 10px;
  transition:color 0.15s;
}
#nav button svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
#nav button.on{color:var(--text);font-weight:600}

/* ---------- writing pad ---------- */
.canvas-wrap{
  position:relative;
  width:100%;
  aspect-ratio:1;
  max-width:300px;
  margin:20px auto;
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:var(--r-lg);
  overflow:hidden;
}
.canvas-ghost{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:150px;
  font-weight:500;
  color:var(--text);
  opacity:0.06;
  pointer-events:none;
  user-select:none;
}
html.dark .canvas-ghost{opacity:0.08}
canvas#drawPad{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  cursor:crosshair;
  touch-action:none;
}
.draw-tools{display:flex;gap:8px;justify-content:center;margin:14px 0}
.draw-tools button{
  padding:9px 16px;
  border-radius:var(--r-sm);
  border:1px solid var(--line);
  background:var(--surface);
  font:inherit;
  font-size:13.5px;
  font-weight:500;
  color:var(--text);
  cursor:pointer;
  transition:background 0.15s;
}
.draw-tools button:hover{background:var(--surface-2)}

/* ---------- grammar ---------- */
.gcard{
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:var(--r);
  padding:18px;
  margin:0 0 10px;
}
.gcard h3{margin:0 0 8px;font-size:16px;font-weight:600;color:var(--text);letter-spacing:-0.01em}
.gcard p{margin:0 0 10px;font-size:14px;color:var(--muted);line-height:1.6}
.gex{background:var(--surface-2);border-radius:var(--r-sm);padding:12px 14px;margin-top:8px}
.gex .ko{font-size:16px;font-weight:600;color:var(--text)}
.gex .ne{font-size:13.5px;color:var(--muted);margin-top:4px;line-height:1.5}

/* ---------- a11y ---------- */
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){
  *{transition:none!important;animation:none!important}
}
</style>
</head>
<body>
<div id="app"></div>
<nav id="nav"></nav>
<script>
/* ========================================================
   नेपालीमा हाङ्गुल — Korean Learning via Nepali Engine
   ======================================================== */
const L = [
  ["ㄱ","खियक / गियक","giyeok",1,"शुरुमा 'ख', बीचमा 'ग'"],
  ["ㄴ","निउन","nieun",1,"नेपाली 'न'"],
  ["ㄷ","थिगुत / दिगुत","digeut",1,"शुरुमा 'थ', बीचमा 'द'"],
  ["ㄹ","रिउल","rieul",1,"सुरु/बीचमा 'र', अन्त्यमा 'ल'"],
  ["ㅁ","मिउम","mieum",1,"नेपाली 'म'"],
  ["ㅂ","फिउप / बिउप","bieup",1,"शुरुमा 'फ', बीचमा 'ब'"],
  ["ㅅ","सियोत","siot",1,"नेपाली 'स'"],
  ["ㅇ","इउङ","ieung",1,"सुरुमा मौन, अन्त्यमा 'ङ'"],
  ["ㅈ","छिउत / जिउत","jieut",1,"शुरुमा 'छ', बीचमा 'ज'"],
  ["ㅊ","छिउत (कडा)","chieut",1,"कडा 'छ' (महाप्राण)"],
  ["ㅋ","खिउक (कडा)","kieuk",1,"कडा 'ख' (महाप्राण)"],
  ["ㅌ","थिउत (कडा)","tieut",1,"कडा 'थ' (महाप्राण)"],
  ["ㅍ","फिउप (कडा)","pieup",1,"कडा 'फ' (महाप्राण)"],
  ["ㅎ","हिउत","hieut",1,"नेपाली 'ह'"],
  ["ㄲ","साङगियक","ssang-giyeok",0,"कडा 'क' (क)"],
  ["ㄸ","साङदिगुत","ssang-digeut",0,"कडा 'त' (त्त)"],
  ["ㅃ","साङबिउप","ssang-bieup",0,"कडा 'प' (प्प)"],
  ["ㅆ","साङसियोत","ssang-siot",0,"कडा 'स' (स्स)"],
  ["ㅉ","साङजिउत","ssang-jieut",0,"कडा 'च' (च्च)"],
  // 10 Basic Vowels (१० मूल स्वरवर्ण)
  ["ㅏ","आ","a",1,1,"मुख ठूलो खोलेर 'आ'"],
  ["ㅑ","या","ya",1,1,"नेपाली 'या'"],
  ["ㅓ","अ","eo",1,1,"मुख सामान्य खोलेर 'अ'"],
  ["ㅕ","य","yeo",1,1,"नेपाली 'य'"],
  ["ㅗ","ओ","o",1,1,"ओठ गोलो पारेर 'ओ'"],
  ["ㅛ","यो","yo",1,1,"नेपाली 'यो'"],
  ["ㅜ","उ","u",1,1,"ओठ अगाडि चुच्चो पारेर 'उ'"],
  ["ㅠ","यु","yu",1,1,"नेपाली 'यु'"],
  ["ㅡ","उ/इ (eu)","eu",1,1,"दाँत जोडेर निकालिने 'अ-उ' आवाज"],
  ["ㅣ","इ","i",1,1,"नेपाली 'इ'"],
  // 11 Compound Vowels (११ संयुक्त स्वरवर्ण)
  ["ㅐ","ए (ऐ)","ae",0,1,"मुख चौडा पारेर 'ए'"],
  ["ㅒ","ये (यै)","yae",0,1,"नेपाली 'ये'"],
  ["ㅔ","ए","e",0,1,"नेपाली 'ए'"],
  ["ㅖ","ये","ye",0,1,"नेपाली 'ये'"],
  ["ㅘ","वा","wa",0,1,"नेपाली 'वा' (ㅗ + ㅏ)"],
  ["ㅙ","वै / वे","wae",0,1,"नेपाली 'वे' (ㅗ + ㅐ)"],
  ["ㅚ","वे","oe",0,1,"नेपाली 'वे' (ㅗ + ㅣ)"],
  ["ㅝ","व (wo)","wo",0,1,"नेपाली 'व' (ㅜ + ㅓ)"],
  ["ㅞ","वे (we)","we",0,1,"नेपाली 'वे' (ㅜ + ㅔ)"],
  ["ㅟ","वि (wi)","wi",0,1,"नेपाली 'वि' (ㅜ + ㅣ)"],
  ["ㅢ","उइ / इ","ui",0,1,"'उइ' वा 'इ' (ㅡ + ㅣ)"]
];

const CI = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
const VI = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"];
const FI = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];

const FIN = [
  ["ㄱ","k","क आवाज (ㄱ, ㅋ, ㄲ)","उदा: 책 (छेक=किताब), 수박 (सुबाक=खरबुजा)"],
  ["ㄴ","n","न आवाज (ㄴ, ㄵ, ㄶ)","उदा: 눈 (नुन=आँखा/हिउँ), 산 (सान=पहाड)"],
  ["ㄷ","t","त आवाज (ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ)","उदा: 옷 (ओत=कपडा), 꽃 (कोत=फूल)"],
  ["ㄹ","l","ल आवाज (ㄹ, ㄼ, ㄽ, ㄾ, ㅀ)","उदा: 물 (मुल=पानी), 달 (दाल=चन्द्रमा)"],
  ["ㅁ","m","म आवाज (ㅁ, ㄻ)","उदा: 밤 (बाम=रात), 마음 (माइम=मन)"],
  ["ㅂ","p","प आवाज (ㅂ, ㅍ, ㅄ, ㄿ)","उदा: 밥 (बाप=भात), 집 (चिप=घर)"],
  ["ㅇ","ng","ङ आवाज (ㅇ)","उदा: 강 (गाङ=नदी), 방 (बाङ=कोठा)"]
];

const NUM = {
  numS: {
    n: "सिनो कोरियन गन्ती (일, 이, 삼…)",
    d: "चिनियाँ मूलका संख्याहरू: मिति, मिनेट, फोन नम्बर, ठेगाना र पैसा (Won) गणना गर्दा प्रयोग गरिन्छ।",
    it: [
      [0,"영","yeong","शून्य"],
      [1,"일","il","एक"],
      [2,"이","i","दुई"],
      [3,"삼","sam","तीन"],
      [4,"사","sa","चार"],
      [5,"오","o","पाँच"],
      [6,"육","yuk","छ"],
      [7,"칠","chil","सात"],
      [8,"팔","pal","आठ"],
      [9,"구","gu","नौ"],
      [10,"십","sip","दश"],
      [20,"이십","isip","बीस"],
      [100,"백","baek","सय"],
      [1000,"천","cheon","हजार"],
      [10000,"만","man","दश हजार (मान)"]
    ]
  },
  numN: {
    n: "मौलिक कोरियन गन्ती (하나, 둘, 셋…)",
    d: "कोरियन भाषाको आफ्नै मौलिक संख्या: वस्तु, मान्छे, उमेर र घडीको घण्टा गणना गर्दा प्रयोग हुन्छ।",
    it: [
      [1,"하나","hana","एक (एउटा)"],
      [2,"둘","dul","दुई (दुइटा)"],
      [3,"셋","set","तीन (तीनवटा)"],
      [4,"넷","net","चार (चारवटा)"],
      [5,"다섯","daseot","पाँच"],
      [6,"여섯","yeoseot","छ"],
      [7,"일곱","ilgop","सात"],
      [8,"여덟","yeodeol","आठ"],
      [9,"아홉","ahop","नौ"],
      [10,"열","yeol","दश"],
      [20,"스물","seumul","बीस"],
      [30,"서른","seoreun","तीस"],
      [40,"마흔","maheun","चालीस"],
      [50,"쉰","swin","पचास"]
    ]
  },
  won: {
    n: "कोरियन पैसा (원 - Won) गन्ती",
    d: "कोरियामा चल्ने मुद्रा (वोन): बजारमा सामान किन्दा, तलब बुझ्दा प्रयोग हुने सिनो संख्या गणना।",
    it: [
      [100,"백원","baegwon","१०० वन (सय वन)"],
      [500,"오백원","obaegwon","५०० वन (पाँच सय वन)"],
      [1000,"천원","cheonwon","१,००० वन (एक हजार वन)"],
      [5000,"오천원","ocheonwon","५,००० वन (पाँच हजार वन)"],
      [10000,"만원","manwon","१०,००० वन (एक मान = दश हजार)"],
      [50000,"오만원","omanwon","५०,००० वन (पाँच मान = पचास हजार)"]
    ]
  }
};

const WORDS = [
  ["talk","💬","दैनिक कुराकानी","नमस्ते, धन्यवाद र अति आवश्यक दैनिक वाक्य",[
    ["안녕하세요","नमस्ते / नमस्कार","आन्न्योङ हासेयो"],
    ["감사합니다","धन्यवाद","खामसा हाम्निदा"],
    ["죄송합니다","माफ गर्नुहोस्","छेसोङ हाम्निदा"],
    ["괜찮아요","ठीकै छ / केही फरक पर्दैन","ख्बेन्छानायो"],
    ["네","हजुर / हो","ने"],
    ["아니요","होइन / अहँ","आनियो"],
    ["잘 지내세요?","सन्चै हुनुहुन्छ?","छाल छिनेसयो?"],
    ["저는 네팔 사람입니다","म नेपाली नागरिक हुँ","छनुन नेफाल सारामिम्निदा"],
    ["한국어를 배워요","म कोरियन भाषा सिक्दैछु","हान्गुगरुल फेवयो"],
    ["도와주세요","कृपया मलाई सहयोग गर्नुहोस्","थोवा जुसेयो"]
  ]],
  ["work","🏭","कारखाना र काम (EPS)","कार्यस्थल, औजार र सुरक्षा सम्बन्धी शब्दहरू",[
    ["공장","कारखाना","खोङजाङ"],
    ["작업","काम / कार्य","छागप"],
    ["반장님","इन्चार्ज / क्याप्टेन","फान्जाङनिम"],
    ["월급","मासिक तलब","वल्गुप"],
    ["안전모","सुरक्षा हेलमेट","आन्जनमो"],
    ["장갑","पञ्जा","छाङ्गाप"],
    ["기계","मेसिन / उपकरण","खिगे"],
    ["스위치","स्विच","सुविछी"],
    ["조심하세요","सावधानी अपनाउनुहोस्","छोसिमहासेयो"],
    ["끝났어요","काम सकियो","कुन्नास्सयो"]
  ]],
  ["rest","🍜","खाना र रेस्टुरेन्ट","खाना अर्डर, मेन्यू र स्वादका शब्दहरू",[
    ["메뉴판","मेन्यू कार्ड","मेन्युफान"],
    ["주문","अर्डर","छुमुन"],
    ["물 주세요","कृपया पानी दिनुहोस्","मुल छुसेयो"],
    ["밥","भात","बाप"],
    ["김치","किम्छी (अचार)","खिमछी"],
    ["맛있어요","धेरै स्वादिष्ट छ","मासिससयो"],
    ["더 주세요","थप दिनुहोस्","थो छुसेयो"],
    ["계산서","बिल / हिसाब","खेसान्सो"],
    ["얼마예요?","कति रुपैयाँ हो?","ओलमायेयो?"]
  ]],
  ["hosp","🏥","अस्पताल र स्वास्थ्य","बिरामी हुँदा, डाक्टर र औषधिका कुरा",[
    ["병원","अस्पताल","फ्योङवन"],
    ["약국","औषधि पसल","याकुक"],
    ["아파요","दुखेको छ / बिरामी छु","आफायो"],
    ["감기","रुघाखोकी","खामगी"],
    ["두통","टाउको दुखाइ","थुथोङ"],
    ["배가 아파요","पेट दुखेको छ","फेगा आफायो"],
    ["열이 나요","ज्वरो आएको छ","योरी नायो"],
    ["약","औषधि","याक"],
    ["주사","सुई","छुसा"]
  ]],
  ["go","🚇","यातायात र बाटो","बस, रेल, सबवे र बाटो सोध्ने",[
    ["지하철","सबवे (भूमिगत रेल)","छिहाछोल"],
    ["버스","बस","फसु"],
    ["택시","ट्याक्सी","थ्याक्सी"],
    ["정류장","बस बिसौनी","छोङ्र्युजाङ"],
    ["역","स्टेशन","यक"],
    ["어디예요?","कहाँ छ?","अदियेयो?"],
    ["오른쪽","दायाँ","ओरुनच्चोक"],
    ["왼쪽","बायाँ","वेनच्चोक"],
    ["직진","सिधा अगाडि","छिक्चिन"]
  ]],
  ["days","📅","हप्ताका ७ दिन","आइतबारदेखि शनिबारसम्म",[
    ["월요일","सोमबार","वर्योइल"],
    ["화요일","मङ्गलबार","ह्वायोइल"],
    ["수요일","बुधबार","सुयोइल"],
    ["목요일","बिहीबार","मोग्योइल"],
    ["금요일","शुक्रबार","खिम्योइल"],
    ["토요일","शनिबार","थोयोइल"],
    ["일요일","आइतबार","इर्योइल"]
  ]]
];

const GRAMMAR = [
  {
    title: "१. वाक्य संरचना (SOV Structure)",
    desc: "नेपाली र कोरियन भाषाको वाक्य संरचना १००% मिल्छ: कर्ता (Subject) + कर्म (Object) + क्रिया (Verb)!",
    ex: [
      { ko: "저는 한국어를 배워요.", ne: "म (S) कोरियन भाषा (O) सिक्छु (V)।" },
      { ko: "민수는 밥을 먹어요.", ne: "मिन्सु (S) भात (O) खान्छ (V)।" }
    ]
  },
  {
    title: "२. व्याकरणका विभक्तिहरू (조사 - Particles)",
    desc: "कोरियन नामयोगी विभक्तिहरू ठ्याक्कै नेपाली व्याकरणका 'ले', 'लाई', 'मा', 'बाट' सँग दाँज्न सकिन्छ।",
    ex: [
      { ko: "은 / 는 (त / चाहिं)", ne: "저는 = म चाहिं (नाम पद पछाडि जोडिने मुख्य विषयक चिह्न)" },
      { ko: "이 / 가 (ले - कर्ता कारक)", ne: "비가 와요 = पानी (ले) पर्दैछ।" },
      { ko: "을 / 를 (लाई - कर्म कारक)", ne: "사과를 먹어요 = स्याउ (लाई) खान्छु।" },
      { ko: "에 / 에서 (मा / बाट)", ne: "नेपालमा = 네팔에 / कोरियाबाट = 한국에서" }
    ]
  },
  {
    title: "३. आदरार्थी तह (Honorific Levels)",
    desc: "नेपालीमा 'तँ', 'तिमी', 'तपाईं' भएजस्तै कोरियनमा ३ प्रमुख आदरार्थी तहहरू हुन्छन्।",
    ex: [
      { ko: "하십시오체 (उच्च आदर): ~습니다 / ~습니까?", ne: "गर्नुहुन्छ / खानुहुन्छ (अति औपचारिक, कार्यालय, अन्तर्वार्ता)" },
      { ko: "해요체 (सामान्य आदर): ~아요 / ~어요", ne: "गर्नुहुन्छ / गर्छु (दैनिक बोलीचालीको सभ्य आदर)" },
      { ko: "반말 (अनादर/साथीभाइ): ~아 / ~어", ne: "गर्छस् / गर् (तँ/घनिष्ठ साथीभाइसँग मात्र)" }
    ]
  },
  {
    title: "४. उच्चारण परिवर्तनका ५ सुनौला नियम (Sound Shift Rules)",
    desc: "कोरियन भाषामा लेखाइ र बोलाइमा फरक पर्ने प्रमुख वैज्ञानिक नियमहरू:",
    ex: [
      { ko: "연음 (सरेर जोडिने नियम): 한국어 -> [हन्गुग]", ne: "तलको व्यञ्जन पछिल्लो स्वरसँग जोडिन्छ (हन्-गुक्-अ नभएर हान्गुग)।" },
      { ko: "비음화 (नासिक्यीकरण): 감사합니다 -> [खामसाम्निदा]", ne: "ㅂ को पछाडि ㄴ आउँदा ㅂ को उच्चारण 'म' बन्दछ।" },
      { ko: "격음화 (ह सँग जोडिँदा महाप्राण): 축하 -> [छुखा]", ne: "ㄱ + ㅎ मिलेर कडा 'ख' (ㅋ) बन्दछ।" },
      { ko: "경음화 (कडा हुने नियम): 학교 -> [हाक्क्यो]", ne: "दुई व्यञ्जन जुध्दा पछिल्लो व्यञ्जन कडा (ㄲ) उच्चारण हुन्छ।" }
    ]
  }
];

/* State Machine */
let TAB = "home";
let LR = { c: "ㄱ", v: "ㅏ" };
let BR = { c: "ㄱ", v: "ㅏ", f: "ㄱ" };
let NUM_K = "numS";
let NUM_I = 0;
let W_CAT = "talk";
let EXAM = { score: 0, total: 10, current: 0, items: [], locked: false };
let DRAW_TARGET = "가";

const app = document.getElementById("app");
const nav = document.getElementById("nav");

const syl = (c, v) => String.fromCharCode(0xAC00 + (CI.indexOf(c) * 21 + VI.indexOf(v)) * 28);
const syl3 = (c, v, f) => String.fromCharCode(0xAC00 + (CI.indexOf(c) * 21 + VI.indexOf(v)) * 28 + FI.indexOf(f));

/* Audio Engine */
let _audio = null;
function say(txt) {
  try {
    if ("speechSynthesis" in window && window.SpeechSynthesisUtterance) {
      const vs = speechSynthesis.getVoices();
      const kv = vs.find(x => x.lang === "ko-KR" || x.lang === "ko_KR" || /^ko/i.test(x.lang));
      const u = new SpeechSynthesisUtterance(txt);
      u.lang = "ko-KR";
      u.rate = 0.85;
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
      }, 600);
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

/* Render Navigation */
function renderNav() {
  const items = [
    { id: "home", label: "गृहपृष्ठ", icon: '<path d="M3 10.5L12 3l9 7.5v9.5a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>' },
    { id: "learn", label: "वर्णमाला", icon: '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M6 6h10M6 10h10"/>' },
    { id: "words", label: "शब्दार्थ", icon: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>' },
    { id: "grammar", label: "व्याकरण", icon: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>' },
    { id: "exam", label: "परीक्षा", icon: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>' }
  ];
  nav.innerHTML = items.map(it => `
    <button class="${TAB === it.id ? 'on' : ''}" onclick="setTab('${it.id}')">
      <svg viewBox="0 0 24 24">${it.icon}</svg>
      <span>${it.label}</span>
    </button>
  `).join("");
}

function setTab(tab) {
  TAB = tab;
  window.scrollTo({ top: 0, behavior: "smooth" });
  render();
}

/* Views */
function viewHome() {
  return `
    <div class="title">नेपालीमा <em>हाङ्गुल</em> <span>सिक्नुहोस्</span></div>
    <div class="hero">
      <small>नेपालीबाट कोरियन</small>
      <div class="hv">१००% मिल्ने भाषा</div>
      <p>वाक्य संरचना (SOV), कारक विभक्ति र उच्चारण — नेपाली र कोरियनमा हुबहु मिल्छ।</p>
    </div>

    <div class="head">प्रमुख सिकाइ खण्डहरू <small>आफ्नो रोजाइ छान्नुहोस्</small></div>
    <div class="list">
      <button class="lrow" onclick="setTab('learn')">
        <span class="ln ko">가</span>
        <span class="lt"><b>हाङ्गुल वर्णमाला र अक्षर निर्माण</b><small>स्वर, व्यञ्जन, फाछिम (받침) र अक्षर संयोजन</small></span>
        <span class="lg">›</span>
      </button>
      <button class="lrow" onclick="setTab('write')">
        <span class="ln ko">쓰</span>
        <span class="lt"><b>हातले लेख्ने अभ्यास (Writing Studio)</b><small>स्ट्रोक अर्डर हेरेर स्क्रिनमा हातले लेख्नुहोस्</small></span>
        <span class="lg">›</span>
      </button>
      <button class="lrow" onclick="setTab('numbers')">
        <span class="ln ko">일</span>
        <span class="lt"><b>कोरियन गन्ती र पैसा (Won)</b><small>सिनो, मौलिक कोरियन संख्या र नेपाली तुलना</small></span>
        <span class="lg">›</span>
      </button>
      <button class="lrow" onclick="setTab('words')">
        <span class="ln ko">단</span>
        <span class="lt"><b>दैनिक तथा EPS शब्दभण्डार</b><small>काम, कारखाना, खाना, अस्पताल र यातायात</small></span>
        <span class="lg">›</span>
      </button>
      <button class="lrow" onclick="setTab('grammar')">
        <span class="ln ko">문</span>
        <span class="lt"><b>नेपाली-कोरियन व्याकरण सेतु</b><small>विभक्ति, आदरार्थी रूप र उच्चारण नियम</small></span>
        <span class="lg">›</span>
      </button>
      <button class="lrow" onclick="setTab('exam')">
        <span class="ln ko">퀴</span>
        <span class="lt"><b>क्विज तथा आत्ममूल्याङ्कन परीक्षा</b><small>ध्वनि सुनेर अक्षर र अर्थ चिन्ने अभ्यास</small></span>
        <span class="lg">›</span>
      </button>
    </div>
  `;
}

function viewLearn() {
  const cs = L.filter(x => CI.includes(x[0]) && x[3]);
  const vs = L.filter(x => VI.includes(x[0]) && x[3]);
  const c = L.find(x => x[0] === LR.c) || cs[0];
  const v = L.find(x => x[0] === LR.v) || vs[0];
  const sy = syl(c[0], v[0]);

  return `
    <div class="title">हाङ्गुल <em>वर्णमाला</em></div>
    <div class="hero" style="text-align:center">
      <small>${c[0]} (${c[1]}) + ${v[0]} (${v[1]})</small>
      <div class="glyph ko">${sy}</div>
      <div class="roman">${c[2]} + ${v[2]}</div>
      <button class="spk" onclick="say('${sy}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a9 9 0 0 1 0 14"/></svg>
      </button>
    </div>

    <div class="seg">
      <button class="on">अक्षर निर्माण (Consonant + Vowel)</button>
      <button onclick="setTab('batchim')">फाछिम (Final Consonant)</button>
    </div>

    <div class="head">व्यञ्जन छान्नुहोस् (Consonants)</div>
    <div class="chips">
      ${cs.map(x => `<button class="chip ko ${x[0] === LR.c ? 'on' : ''}" onclick="LR.c='${x[0]}';render()">${x[0]}</button>`).join("")}
    </div>

    <div class="head">स्वर छान्नुहोस् (Vowels)</div>
    <div class="chips">
      ${vs.map(x => `<button class="chip ko ${x[0] === LR.v ? 'on' : ''}" onclick="LR.v='${x[0]}';render()">${x[0]}</button>`).join("")}
    </div>

    <div class="head">अक्षरको नेपाली विश्लेषण</div>
    <div class="tile">
      <p>व्यञ्जनवर्ण: <b>${c[0]}</b> (${c[1]}) — ${c[4] || ''}</p>
      <p>स्वरवर्ण: <b>${v[0]}</b> (${v[1]}) — ${v[5] || ''}</p>
      <p style="margin:10px 0 0;color:var(--text);font-weight:600">संयुक्त उच्चारण: <b>${sy}</b> — नेपालीमा उच्चारण सुन्न माथिको माइक थिच्नुहोस्</p>
    </div>

    <div style="margin-top:16px">
      <button class="primary" onclick="DRAW_TARGET='${sy}';setTab('write')">यो अक्षर हातले लेख्ने अभ्यास गर्नुहोस्</button>
    </div>
  `;
}

function viewBatchim() {
  const cs = L.filter(x => CI.includes(x[0]) && x[3]);
  const vs = L.filter(x => VI.includes(x[0]) && x[3]);
  const c = L.find(x => x[0] === BR.c) || cs[0];
  const v = L.find(x => x[0] === BR.v) || vs[0];
  const f = FIN.find(x => x[0] === BR.f) || FIN[0];
  const sy = syl3(c[0], v[0], f[0]);

  return `
    <div class="title">फाछिम <em>(받침)</em> नियम</div>
    <div class="hero" style="text-align:center">
      <small>${c[0]} + ${v[0]} + ${f[0]} (तल्लो व्यञ्जन)</small>
      <div class="glyph ko">${sy}</div>
      <div class="roman">${f[2]}</div>
      <button class="spk" onclick="say('${sy}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <div class="seg">
      <button onclick="setTab('learn')">सामान्य अक्षर</button>
      <button class="on">फाछिम (अन्तिम व्यञ्जन)</button>
    </div>

    <p class="tip"><b>फाछिम के हो?</b> कोरियन अक्षरको तल्लो भागमा झुण्डिएर आउने व्यञ्जनलाई फाछिम (받침) भनिन्छ। जम्मा २७ वटा व्यञ्जनहरू फाछिम भएर आए तापनि उच्चारण हुँदा केवल <b>७ वटा मुख्य ध्वनि</b> मा सीमित हुन्छन्।</p>

    <div class="head">७ मुख्य फाछिम ध्वनिहरू छान्नुहोस्</div>
    <div class="chips">
      ${FIN.map(x => `<button class="chip ko ${x[0] === BR.f ? 'on' : ''}" onclick="BR.f='${x[0]}';render()">${x[0]} (${x[1]})</button>`).join("")}
    </div>

    <div class="tile" style="margin-top:14px">
      <p style="color:var(--text);font-weight:600">${f[0]} फाछिमको नियम: ${f[2]}</p>
      <p style="font-size:15px;margin:4px 0">${f[3]}</p>
    </div>
  `;
}

function viewNumbers() {
  const d = NUM[NUM_K];
  const cur = d.it[NUM_I] || d.it[0];

  return `
    <div class="title">कोरियन <em>गन्ती</em></div>
    <div class="seg">
      <button class="${NUM_K === 'numS' ? 'on' : ''}" onclick="NUM_K='numS';NUM_I=0;render()">सिनो (일·이·삼)</button>
      <button class="${NUM_K === 'numN' ? 'on' : ''}" onclick="NUM_K='numN';NUM_I=0;render()">मौलिक (하나·둘)</button>
      <button class="${NUM_K === 'won' ? 'on' : ''}" onclick="NUM_K='won';NUM_I=0;render()">पैसा (Won)</button>
    </div>

    <div class="hero" style="text-align:center;margin-top:14px">
      <small>${d.n}</small>
      <div class="glyph ko">${cur[1]}</div>
      <div class="roman">${cur[0]} = ${cur[3]}</div>
      <button class="spk" onclick="say('${cur[1]}')" aria-label="सुन्नुहोस्">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>
      </button>
    </div>

    <p class="tip">${d.d}</p>

    <div class="head">संख्या छान्नुहोस् र उच्चारण सुन्नुहोस्</div>
    <div class="sg">
      ${d.it.map((it, idx) => `
        <button class="sc ${idx === NUM_I ? 'on' : ''}" onclick="NUM_I=${idx};render();say('${it[1]}')">
          <span class="ko">${it[1]}</span>
          <small>${it[0]}</small>
        </button>
      `).join("")}
    </div>
  `;
}

function viewWords() {
  const cat = WORDS.find(x => x[0] === W_CAT) || WORDS[0];

  return `
    <div class="title">दैनिक <em>शब्दार्थ</em></div>
    <div class="seg scroll">
      ${WORDS.map(c => `
        <button class="${W_CAT === c[0] ? 'on' : ''}" onclick="W_CAT='${c[0]}';render()">${c[2]}</button>
      `).join("")}
    </div>

    <div class="head">${cat[2]} <small>${cat[3]}</small></div>
    <div class="list">
      ${cat[4].map(w => `
        <div class="lrow" onclick="say('${w[0]}')">
          <span class="ln"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a9 9 0 0 1 0 14"/></svg></span>
          <span class="lt">
            <b class="ko" style="font-size:19px">${w[0]}</b>
            <small style="font-size:14px;color:var(--text);margin-top:2px">${w[1]}</small>
            <small>[${w[2]}]</small>
          </span>
        </div>
      `).join("")}
    </div>
  `;
}

function viewGrammar() {
  return `
    <div class="title">नेपाली-कोरियन <em>व्याकरण</em></div>
    <p class="sub" style="color:var(--sub);margin:0 0 14px">नेपाली मातृभाषा हुनेहरूका लागि कोरियन व्याकरण संसारकै सबैभन्दा सजिलो व्याकरण मानिन्छ।</p>
    ${GRAMMAR.map(g => `
      <div class="gcard">
        <h3>${g.title}</h3>
        <p>${g.desc}</p>
        ${g.ex.map(e => `
          <div class="gex">
            <div class="ko">${e.ko}</div>
            <div class="ne">${e.ne}</div>
          </div>
        `).join("")}
      </div>
    `).join("")}
  `;
}

function viewWrite() {
  setTimeout(initCanvas, 50);
  return `
    <div class="title">हातले <em>लेख्ने</em> अभ्यास</div>
    <p class="sub" style="color:var(--sub);margin:0 0 10px">कोरियन वर्ण वा अक्षरलाई स्क्रिनमा औंला वा माउसले लेख्नुहोस्:</p>
    
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:10px 0">
      <span style="font-size:16px;font-weight:600">अभ्यास अक्षर:</span>
      <b class="ko" style="font-size:28px">${DRAW_TARGET}</b>
      <button class="chip" onclick="say('${DRAW_TARGET}')">सुन्नुहोस्</button>
    </div>

    <div class="canvas-wrap">
      <div class="canvas-ghost ko" id="ghostChar">${DRAW_TARGET}</div>
      <canvas id="drawPad" width="320" height="320"></canvas>
    </div>

    <div class="draw-tools">
      <button onclick="clearCanvas()">मेटाउनुहोस् (Clear)</button>
      <button onclick="changeDrawTarget()">अर्को अक्षर (Next)</button>
    </div>

    <div class="head">वर्ण छान्नुहोस्</div>
    <div class="chips">
      ${["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅇ","ㅈ","ㅎ","가","나","다","라","마","바","사","아","자","하"].map(ch => `
        <button class="chip ko ${DRAW_TARGET === ch ? 'on' : ''}" onclick="DRAW_TARGET='${ch}';render()">${ch}</button>
      `).join("")}
    </div>
  `;
}

let isDrawing = false;
let canvasCtx = null;
function initCanvas() {
  const cvs = document.getElementById("drawPad");
  if (!cvs) return;
  canvasCtx = cvs.getContext("2d");
  const ink = getComputedStyle(document.documentElement).getPropertyValue("--text").trim();
  canvasCtx.strokeStyle = ink || "#141414";
  canvasCtx.lineWidth = 10;
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
  if (cvs && canvasCtx) {
    canvasCtx.clearRect(0, 0, cvs.width, cvs.height);
  }
}
function changeDrawTarget() {
  const chars = ["가","나","다","라","마","바","사","아","자","차","카","타","파","하","한","글","밥","물","산","강"];
  const next = chars[Math.floor(Math.random() * chars.length)];
  DRAW_TARGET = next;
  render();
}

function viewExam() {
  if (EXAM.items.length === 0) startExam();
  const q = EXAM.items[EXAM.current];
  const progress = Math.round((EXAM.current / EXAM.total) * 100);

  return `
    <div class="title">क्विज तथा <em>परीक्षा</em></div>
    <div class="hero">
      <small>प्रश्नोत्तर परीक्षा (${EXAM.current + 1} / ${EXAM.total})</small>
      <div class="hv">${EXAM.score} अंक</div>
      <div class="meter">
        <div><i style="width:${progress}%"></i></div>
        <b>${progress}%</b>
      </div>
    </div>

    <div style="text-align:center;margin:24px 0 12px">
      <p style="font-size:16px;color:var(--sub);margin:0">आवाज सुन्नुहोस् र सही अक्षर पत्ता लगाउनुहोस्:</p>
      <button class="primary" style="margin:12px auto;width:auto;padding:12px 24px" onclick="say('${q.answer}')">
        उच्चारण सुन्नुहोस्
      </button>
    </div>

    <div class="grid">
      ${q.options.map(opt => `
        <button class="opt ko" onclick="checkExamAnswer(this, '${opt}', '${q.answer}')">
          ${opt}
        </button>
      `).join("")}
    </div>
  `;
}

function startExam() {
  const samplePool = L.filter(x => x[3]).map(x => x[0]);
  EXAM.items = [];
  EXAM.score = 0;
  EXAM.current = 0;
  EXAM.total = 10;
  EXAM.locked = false;

  for (let i = 0; i < EXAM.total; i++) {
    const ans = samplePool[Math.floor(Math.random() * samplePool.length)];
    const opts = [ans];
    while (opts.length < 3) {
      const r = samplePool[Math.floor(Math.random() * samplePool.length)];
      if (!opts.includes(r)) opts.push(r);
    }
    opts.sort(() => Math.random() - 0.5);
    EXAM.items.push({ answer: ans, options: opts });
  }
}

function checkExamAnswer(btn, selected, correct) {
  if (EXAM.locked) return;
  EXAM.locked = true;

  if (selected === correct) {
    btn.classList.add("ok");
    EXAM.score += 10;
  } else {
    btn.classList.add("bad");
  }

  setTimeout(() => {
    EXAM.current++;
    EXAM.locked = false;
    if (EXAM.current >= EXAM.total) {
      alert("परीक्षा सम्पन्न भयो! तपाईंको कूल प्राप्तांक: " + EXAM.score + " / 100");
      startExam();
    }
    render();
  }, 900);
}

/* Render Dispatcher */
function render() {
  renderNav();
  if (TAB === "home") app.innerHTML = viewHome();
  else if (TAB === "learn") app.innerHTML = viewLearn();
  else if (TAB === "batchim") app.innerHTML = viewBatchim();
  else if (TAB === "numbers") app.innerHTML = viewNumbers();
  else if (TAB === "words") app.innerHTML = viewWords();
  else if (TAB === "grammar") app.innerHTML = viewGrammar();
  else if (TAB === "write") app.innerHTML = viewWrite();
  else if (TAB === "exam") app.innerHTML = viewExam();
}

// Initial Boot
render();
</script>
</body>
</html>
'''

with open('/home/manish/projects/nepalihangul/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated /home/manish/projects/nepalihangul/index.html")
