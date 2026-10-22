#!/usr/bin/env bash
# Usage: slack-notify.sh <title> <message> [<button label>=<url> ...]
#
# Posts a message to the Slack channel behind the SLACK_WEBHOOK_URL secret:
# <title> as the heading, <message> in Slack markdown (*bold*, <url|text>) and
# one link button per <label>=<url> argument (empty URLs are left out).
# A missing secret or a Slack error only gives a warning: a notification
# must never fail the deploy.
set -euo pipefail

title="$1"
message="$2"
shift 2

if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  echo "::warning::SLACK_WEBHOOK_URL secret is not set, no Slack notification sent"
  exit 0
fi

buttons="[]"
for button in "$@"; do
  label="${button%%=*}"
  url="${button#*=}"
  if [ -n "$url" ]; then
    buttons=$(jq -c --arg label "$label" --arg url "$url" \
      '. + [{type: "button", text: {type: "plain_text", text: $label}, url: $url}]' <<< "$buttons")
  fi
done

payload=$(jq -n --arg title "$title" --arg message "$message" --argjson buttons "$buttons" '{
  text: $title,
  blocks: (
    [
      {type: "header", text: {type: "plain_text", text: $title}},
      {type: "section", text: {type: "mrkdwn", text: $message}}
    ]
    + (if ($buttons | length) > 0 then [{type: "actions", elements: $buttons}] else [] end)
  )
}')

if ! curl -fsS --max-time 30 -H "Content-type: application/json" --data "$payload" "$SLACK_WEBHOOK_URL"; then
  echo "::warning::Slack notification could not be sent"
fi
echo
