#!/usr/bin/env bash
# Slack notification wrapper.
# Usage: bash scripts/notify.sh "<message>"
#        bash scripts/notify.sh --json '<slack payload json>'
# Falls back to DAILY-SUMMARY.md if credentials are missing; always exits 0.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
FALLBACK="$ROOT/DAILY-SUMMARY.md"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

json_mode=0
if [[ "${1:-}" == "--json" ]]; then
  json_mode=1
  shift
fi

if [[ $# -gt 0 ]]; then
  msg="$*"
else
  msg="$(cat)"
fi

if [[ -z "${msg// /}" ]]; then
  echo "usage: bash scripts/notify.sh \"<message>\"" >&2
  exit 1
fi

stamp="$(date '+%Y-%m-%d %H:%M %Z')"

if [[ -z "${SLACK_WEBHOOK_URL:-}" ]]; then
  if [[ "$json_mode" -eq 1 ]]; then
    text="$(python3 -c "
import json, sys
payload = json.loads(sys.argv[1])
print(payload.get('text') or json.dumps(payload))
" "$msg")"
  else
    text="$msg"
  fi
  printf "\n---\n## %s (fallback — Slack not configured)\n%s\n" "$stamp" "$text" >> "$FALLBACK"
  echo "[notify fallback] appended to DAILY-SUMMARY.md"
  exit 0
fi

if [[ "$json_mode" -eq 1 ]]; then
  payload="$msg"
else
  payload="$(python3 -c "
import json, sys
print(json.dumps({'text': sys.argv[1]}))
" "$msg")"
fi

curl -fsS -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$payload"

echo
