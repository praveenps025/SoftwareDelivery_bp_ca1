#!/usr/bin/env bash
# Usage: health-check.sh <site-url> <expected-version>
#
# Waits until the live site reports <expected-version> in its X-App-Version
# header (App Service keeps serving the old container while the new one starts),
# then checks that the main pages work. Fails if that version is not live and
# healthy within HEALTH_CHECK_TRIES x 10 seconds (default 30 = 5 minutes).
set -euo pipefail

url="${1%/}"
expected="$2"
tries="${HEALTH_CHECK_TRIES:-30}"
live=""

for i in $(seq 1 "$tries"); do
  live=$(curl -fsS -o /dev/null -D - --max-time 30 "$url/" 2>/dev/null \
    | awk 'tolower($1) == "x-app-version:" { print $2 }' | tr -d '\r' || true)
  if [ "$live" = "$expected" ]; then
    break
  fi
  echo "Attempt $i/$tries: live version is '${live:-no response}', waiting for $expected"
  sleep 10
done

if [ "$live" != "$expected" ]; then
  echo "::error::Version $expected did not go live at $url (still '${live:-no response}')"
  exit 1
fi

page=$(curl -fsS --max-time 30 "$url/")
if ! grep -q "Ideal Blood Pressure" <<< "$page"; then
  echo "::error::Home page does not show the calculator"
  exit 1
fi
curl -fsS -o /dev/null --max-time 30 "$url/Privacy"

echo "Version $expected is live at $url and serving pages"
