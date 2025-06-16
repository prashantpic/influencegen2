#!/bin/bash

# Utility script to interact with JIRA for change management or issue tracking.
#
# Requirements:
# - curl command installed.
# - jq command installed (for parsing JSON responses).
# - Environment variables:
#   - JIRA_BASE_URL: Base URL of the JIRA instance (e.g., https://your-domain.atlassian.net).
#   - JIRA_USERNAME: Username (email) for JIRA API authentication.
#   - JIRA_API_TOKEN_SECRET: JIRA API token (masked and protected CI/CD variable).
#
# Sub-commands:
#   get_jira_issue_status <issue_key>
#     Fetches and prints the status name of the given JIRA issue.
#     Exits 0 if successful, 1 on error.
#
#   update_jira_issue_status <issue_key> <transition_name_or_id> [comment_body]
#     Transitions a JIRA issue to a new status and optionally adds a comment.
#     <transition_name_or_id>: This can be the exact name of the transition (e.g., "Done")
#                              or the transition ID. Finding transition IDs usually requires
#                              a separate API call to /rest/api/2/issue/{issueIdOrKey}/transitions
#     Exits 0 if successful, 1 on error.
#
#   check_approval <issue_key>
#     Specific helper for production deployments. Checks if the issue status indicates approval.
#     Approval statuses are hardcoded for now: "Approved for Deployment", "Approved".
#     Exits 0 if approved, 1 if not approved or on error.

set -e # Exit immediately if a command exits with a non-zero status.
set -o pipefail # Causes a pipeline to return the exit status of the last command in the pipe that failed.

# --- Configuration & Parameters ---
SUB_COMMAND="$1"
ISSUE_KEY="$2"

# --- Validate Base Requirements ---
if [[ -z "$JIRA_BASE_URL" ]] || [[ -z "$JIRA_USERNAME" ]] || [[ -z "$JIRA_API_TOKEN_SECRET" ]]; then
  echo "Error: JIRA_BASE_URL, JIRA_USERNAME, and JIRA_API_TOKEN_SECRET environment variables must be set."
  exit 1
fi

if ! command -v curl &> /dev/null; then
    echo "Error: curl command not found. Please install curl."
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "Error: jq command not found. Please install jq."
    exit 1
fi

# --- Helper Function for API Calls ---
call_jira_api() {
  local method="$1"
  local api_path="$2"
  local data_payload="$3"
  local response_file
  response_file=$(mktemp) # Create a temporary file to store the response

  echo "DEBUG: Calling JIRA API: $method ${JIRA_BASE_URL}/rest/api/2/${api_path}"
  if [[ -n "$data_payload" ]]; then
    echo "DEBUG: Payload: $data_payload"
  fi

  HTTP_RESPONSE_CODE=$(curl -s -o "$response_file" -w "%{http_code}" \
    -u "${JIRA_USERNAME}:${JIRA_API_TOKEN_SECRET}" \
    -X "$method" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    "${JIRA_BASE_URL}/rest/api/2/${api_path}" \
    ${data_payload:+-d "$data_payload"})

  if [[ "$HTTP_RESPONSE_CODE" -lt 200 || "$HTTP_RESPONSE_CODE" -ge 300 ]]; then
    echo "Error: JIRA API call failed with HTTP status $HTTP_RESPONSE_CODE."
    echo "Response:"
    cat "$response_file"
    rm "$response_file"
    return 1
  fi

  cat "$response_file" # Output response body to stdout for further processing by caller
  rm "$response_file"
  return 0
}

# --- Sub-command Logic ---
case "$SUB_COMMAND" in
  get_jira_issue_status)
    if [[ -z "$ISSUE_KEY" ]]; then
      echo "Usage: $0 get_jira_issue_status <issue_key>"
      echo "Error: Missing <issue_key>."
      exit 1
    fi
    echo "Fetching status for JIRA issue: $ISSUE_KEY"
    RESPONSE_BODY=$(call_jira_api "GET" "issue/${ISSUE_KEY}?fields=status")
    if [[ $? -ne 0 ]]; then
      exit 1
    fi
    STATUS_NAME=$(echo "$RESPONSE_BODY" | jq -r '.fields.status.name')
    if [[ -z "$STATUS_NAME" || "$STATUS_NAME" == "null" ]]; then
        echo "Error: Could not extract status name from JIRA response."
        echo "Response: $RESPONSE_BODY"
        exit 1
    fi
    echo "JIRA Issue $ISSUE_KEY current status: $STATUS_NAME"
    echo "$STATUS_NAME" # Output status name for scripting
    ;;

  update_jira_issue_status)
    TRANSITION_ID_OR_NAME="$3" # This is tricky, JIRA API often needs transition ID.
                               # For simplicity, we'll try to find transition by name if it's not numeric.
    COMMENT_BODY="$4"

    if [[ -z "$ISSUE_KEY" ]] || [[ -z "$TRANSITION_ID_OR_NAME" ]]; then
      echo "Usage: $0 update_jira_issue_status <issue_key> <transition_name_or_id> [comment_body]"
      echo "Error: Missing <issue_key> or <transition_name_or_id>."
      exit 1
    fi

    echo "Attempting to update status for JIRA issue: $ISSUE_KEY to $TRANSITION_ID_OR_NAME"

    # Construct payload for transition
    # If TRANSITION_ID_OR_NAME is numeric, assume it's an ID. Otherwise, try to find by name.
    # Note: Finding transition by name directly in the transition POST is not standard.
    # A more robust solution would first fetch available transitions, then use the ID.
    # This simplified version assumes the provided name is somehow directly usable or it's an ID.
    # For a robust solution, one would:
    # 1. GET /rest/api/2/issue/${ISSUE_KEY}/transitions
    # 2. Filter by name to find the ID.
    # 3. Use that ID in the POST below.

    PAYLOAD_OBJECT="{\"transition\": {\"id\": \"${TRANSITION_ID_OR_NAME}\"}}" # Assuming it's an ID for now
    # If it were by name (custom or non-standard JIRA config):
    # PAYLOAD_OBJECT="{\"transition\": {\"name\": \"${TRANSITION_ID_OR_NAME}\"}}"

    if [[ -n "$COMMENT_BODY" ]]; then
      JSON_COMMENT_BODY=$(echo "$COMMENT_BODY" | jq -R -s '.' ) # Safely escape comment for JSON
      PAYLOAD_OBJECT="{\"transition\": {\"id\": \"${TRANSITION_ID_OR_NAME}\"}, \"update\": {\"comment\": [{\"add\": {\"body\": ${JSON_COMMENT_BODY}}}]}}"
    fi

    # API endpoint for transitions is /issue/{issueIdOrKey}/transitions
    RESPONSE_BODY=$(call_jira_api "POST" "issue/${ISSUE_KEY}/transitions" "$PAYLOAD_OBJECT")
    if [[ $? -ne 0 ]]; then
      echo "Failed to update JIRA issue $ISSUE_KEY."
      exit 1
    fi
    echo "JIRA Issue $ISSUE_KEY status updated successfully using transition '$TRANSITION_ID_OR_NAME'."
    ;;

  check_approval)
    if [[ -z "$ISSUE_KEY" ]]; then
      echo "Usage: $0 check_approval <issue_key>"
      echo "Error: Missing <issue_key> for approval check."
      exit 1
    fi
    echo "Checking approval status for JIRA issue: $ISSUE_KEY"
    RESPONSE_BODY=$(call_jira_api "GET" "issue/${ISSUE_KEY}?fields=status")
    if [[ $? -ne 0 ]]; then
      exit 1
    fi
    STATUS_NAME=$(echo "$RESPONSE_BODY" | jq -r '.fields.status.name')

    # Define acceptable approval statuses
    APPROVED_STATUSES=("Approved for Deployment" "Approved" "Deployment Approved") # Add more as needed

    IS_APPROVED=false
    for approved_status in "${APPROVED_STATUSES[@]}"; do
      if [[ "$STATUS_NAME" == "$approved_status" ]]; then
        IS_APPROVED=true
        break
      fi
    done

    if $IS_APPROVED; then
      echo "JIRA Issue $ISSUE_KEY is APPROVED (Status: '$STATUS_NAME'). Proceeding."
      exit 0
    else
      echo "Error: JIRA Issue $ISSUE_KEY is NOT APPROVED for deployment (Current Status: '$STATUS_NAME'). Halting."
      exit 1
    fi
    ;;

  *)
    echo "Error: Invalid sub-command '$SUB_COMMAND'."
    echo "Available sub-commands: get_jira_issue_status, update_jira_issue_status, check_approval"
    exit 1
    ;;
esac

exit 0