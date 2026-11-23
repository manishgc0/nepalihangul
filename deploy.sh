#!/usr/bin/env bash
# One command to ship: build, gate, commit, deploy.
#
# Every gate here exists because its failure shipped once:
#   --verify   a word rendered fine but had no clip, so say() fell to /api/tts
#              (absent on a static host), then to speechSynthesis (no Korean
#              voice on Linux), and the screen was simply silent.
#   node --check  the generated JS is one 750 KB blob; a syntax error there is a
#              white page, not a stack trace.
#
# Usage:
#   ./deploy.sh                 build, gate, deploy to Vercel
#   ./deploy.sh -m "message"    ...with a commit message
#   ./deploy.sh --check         gates only, deploy nothing
set -euo pipefail

cd "$(dirname "$0")"
export PATH="$PATH:$HOME/.local/bin"

MSG=""
CHECK_ONLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    -m|--message) MSG="$2"; shift 2 ;;
    --check) CHECK_ONLY=1; shift ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

step() { printf '\n\033[1m%s\033[0m\n' "$1"; }

step "1/5  build"
python3 build_bilingual.py

step "2/5  syntax gates"
python3 - <<'PY'
import os, re
os.makedirs("/tmp/opencode", exist_ok=True)
html = open("index.html", encoding="utf-8").read()
bodies = re.findall(r"<script>(.*?)</script>", html, re.S)
open("/tmp/opencode/_deploy_app.js", "w", encoding="utf-8").write("\n".join(bodies))
PY
node --check /tmp/opencode/_deploy_app.js
node --check sw.js
echo "JS OK · SW OK · $(grep -o 'VERSION = "v[0-9]*"' sw.js)"

step "3/5  audio coverage"
python3 gen_audio.py --verify

if [ "$CHECK_ONLY" = "1" ]; then
  step "gates only — nothing deployed"
  exit 0
fi

step "4/5  git"
if [ -z "$(git status --porcelain)" ]; then
  echo "working tree clean — nothing to commit"
else
  [ -n "$MSG" ] || MSG="Update $(date +%Y-%m-%d\ %H:%M)"
  git add -A
  git commit -q -m "$MSG"
  git log --oneline -1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git push origin HEAD 2>&1 | tail -2 || echo "push failed — is the GitHub remote authenticated?"
else
  echo "no origin remote yet — push skipped"
fi

step "5/5  deploy"
vercel --prod --yes 2>&1 | grep -o '"message": "[^"]*"' | tail -1 || true
