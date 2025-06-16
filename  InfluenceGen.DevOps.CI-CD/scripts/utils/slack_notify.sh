#!/bin/bash

# Utility script to send notifications to Slack channels.
#
# Requirements:
# - curl command installed.
# - Environment variables for Slack webhook URLs (e.g., SLACK_WEBHOOK_URL_INFO, SLACK_WEBHOOK_URL_CRITICAL).
#
# Parameters:
# $1 (status): 'success', 'failure', or 'info'. Determines color and potentially webhook.
# $2 (message_title): The main title of the Slack message.
# $3 (message_body): The detailed body of the message. Markdown is supported by Slack.
# $4 (channel) (Optional): Specific Slack channel (e.g., #devops-alerts). If not provided, relies on webhook's default channel.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration & Parameters ---
STATUS="${1}"
MESSAGE_TITLE="${2}"
MESSAGE_BODY="${3}"
CHANNEL="${4:-}" # Optional channel override

# --- Validate Inputs ---
if [[ -z "$STATUS" ]] || [[ -z "$MESSAGE_TITLE" ]] || [[ -z "$MESSAGE_BODY" ]]; then
  echo "Usage: $0 <success|failure|info> \"<message_title>\" \"<message_body>\" [channel_override]"
  echo "Error: Missing required arguments."
  exit 1
fi

# --- Determine Webhook URL and Color based on Status ---
SLACK_WEBHOOK_URL=""
COLOR=""

case "$STATUS" in
  success)
    SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL_INFO_SECRET:-$SLACK_WEBHOOK_URL_SUCCESS_SECRET}" # Prefer _INFO if _SUCCESS is not defined
    COLOR="good" # Green
    ;;
  failure)
    SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL_CRITICAL_SECRET:-$SLACK_WEBHOOK_URL_FAILURE_SECRET}" # Prefer _CRITICAL
    COLOR="danger" # Red
    ;;
  info)
    SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL_INFO_SECRET}"
    COLOR="#439FE0" # Blue
    ;;
  *)
    echo "Error: Invalid status '$STATUS'. Must be 'success', 'failure', or 'info'."
    exit 1
    ;;
esac

if [[ -z "$SLACK_WEBHOOK_URL" ]]; then
  echo "Error: Slack webhook URL for status '$STATUS' is not configured. Please set appropriate SLACK_WEBHOOK_URL_*_SECRET environment variable."
  exit 1
fi

# --- Construct Slack Message Payload ---
PIPELINE_INFO=""
if [[ -n "$CI_PROJECT_URL" && -n "$CI_PIPELINE_ID" ]]; then
  PIPELINE_INFO=" | <$CI_PROJECT_URL/-/pipelines/$CI_PIPELINE_ID|View Pipeline>"
elif [[ -n "$CI_JOB_URL" ]]; then
  PIPELINE_INFO=" | <$CI_JOB_URL|View Job>"
fi

# Sanitize message body for JSON
# Simple sanitization, consider more robust methods if complex inputs are expected
JSON_MESSAGE_BODY=$(echo "$MESSAGE_BODY" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
JSON_MESSAGE_TITLE=$(echo "$MESSAGE_TITLE" | sed 's/"/\\"/g')

PAYLOAD_JSON=$(cat <<EOF
{
  "channel": "${CHANNEL}",
  "attachments": [
    {
      "fallback": "${JSON_MESSAGE_TITLE} - Status: ${STATUS}",
      "color": "${COLOR}",
      "title": "${JSON_MESSAGE_TITLE}${PIPELINE_INFO}",
      "text": "${JSON_MESSAGE_BODY}",
      "ts": $(date +%s),
      "fields": [
        {
          "title": "Project",
          "value": "${CI_PROJECT_NAME:-N/A}",
          "short": true
        },
        {
          "title": "Branch/Tag",
          "value": "${CI_COMMIT_REF_NAME:-N/A}",
          "short": true
        },
        {
          "title": "Status",
          "value": "${STATUS}",
          "short": true
        },
        {
          "title": "Triggered By",
          "value": "${GITLAB_USER_NAME:-${GITLAB_USER_LOGIN:-System}}",
          "short": true
        }
      ],
      "footer": "InfluenceGen CI/CD Notification",
      "footer_icon": "https://gitlab.com/favicon.ico"
    }
  ]
}
EOF
)

# If channel is not specified, remove it from payload so webhook default is used
if [[ -z "$CHANNEL" ]]; then
  PAYLOAD_JSON=$(echo "$PAYLOAD_JSON" | sed 's/"channel": "",//g')
fi


# --- Send Notification ---
echo "Sending Slack notification..."
RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H 'Content-type: application/json' --data "$PAYLOAD_JSON" "$SLACK_WEBHOOK_URL")

if [[ "$RESPONSE_CODE" -eq 200 ]]; then
  echo "Slack notification sent successfully (HTTP $RESPONSE_CODE)."
  exit 0
else
  echo "Error: Failed to send Slack notification. HTTP Response Code: $RESPONSE_CODE"
  # curl -X POST -H 'Content-type: application/json' --data "$PAYLOAD_JSON" "$SLACK_WEBHOOK_URL" # Print actual response for debugging
  exit 1
fi