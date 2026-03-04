#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <github-username-or-org> <repo-name> [private:true|false]"
  exit 1
fi

OWNER="$1"
REPO="$2"
PRIVATE="${3:-true}"
TOKEN="${GITHUB_PAT:-}"

if [[ -z "$TOKEN" ]]; then
  echo "Error: GITHUB_PAT not set. Export a PAT with 'repo' scope."
  exit 1
fi

API="https://api.github.com/user/repos"

RESP_CODE=$(curl -sS -o /tmp/repo_create.json -w "%{http_code}" \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -X POST "$API" \
  -d "{\"name\":\"${REPO}\",\"private\":${PRIVATE},\"description\":\"Personal Strategic News Intelligence System\"}")

echo "HTTP ${RESP_CODE}"
if [[ "${RESP_CODE}" -ge 200 && "${RESP_CODE}" -lt 300 ]]; then
  cat /tmp/repo_create.json | jq .
  CLONE_URL=$(jq -r '.clone_url' /tmp/repo_create.json)
  git remote remove origin 2>/dev/null || true
  git remote add origin "$CLONE_URL"
  echo "Added 'origin' remote: $CLONE_URL"
else
  echo "Create failed:"
  head -c 2000 /tmp/repo_create.json
  exit 1
fi

