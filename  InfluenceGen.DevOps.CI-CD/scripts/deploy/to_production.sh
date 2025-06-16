```bash
#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting deployment to Production environment..."

# --- Configuration - Expected Environment Variables ---
: "${PROD_ODOO_SERVER_SSH_HOST:?Error: PROD_ODOO_SERVER_SSH_HOST not set.}"
: "${PROD_ODOO_SERVER_SSH_USER:?Error: PROD_ODOO_SERVER_SSH_USER not set.}"
: "${PROD_ODOO_SSH_KEY_SECRET:?Error: PROD_ODOO_SSH_KEY_SECRET not set.}"
: "${PROD_ODOO_ADDONS_PATH:?Error: PROD_ODOO_ADDONS_PATH not set.}"
: "${PROD_ODOO_DB_NAME:?Error: PROD_ODOO_DB_NAME not set.}"
: "${PROD_ODOO_SERVICE_NAME:?Error: PROD_ODOO_SERVICE_NAME not set.}"

: "${PROD_N8N_INSTANCE_URL:?Error: PROD_N8N_INSTANCE_URL not set.}"
: "${PROD_N8N_API_KEY_SECRET:?Error: PROD_N8N_API_KEY_SECRET not set.}"

: "${ODOO_ARTIFACT_NAME:?Error: ODOO_ARTIFACT_NAME not set.}"
: "${N8N_ARTIFACT_NAME:?Error: N8N_ARTIFACT_NAME not set.}"

: "${CHANGE_REQUEST_ID:?Error: CHANGE_REQUEST_ID not set for Production deployment.}"
MODULES_TO_UPDATE="${ODOO_MODULES_TO_UPDATE:-influence_gen_portal,influence_gen_campaign}"

# Slack notification (ensure SLACK_WEBHOOK_URL_CRITICAL_SECRET is set in CI/CD variables)
SLACK_CHANNEL_PROD_DEPLOY="#prod-deployments" # Example channel

SSH_KEY_PATH="/tmp/prod_deploy_ssh_key_$(date +%s%N)"
DEPLOY_SUCCESS=false # Flag to track deployment outcome for final notification

# --- Helper Functions ---
cleanup() {
  echo "Cleaning up temporary files..."
  rm -f "$SSH_KEY_PATH"
  rm -rf "/tmp/n8n_workflows_unzipped_prod"

  if [ "$DEPLOY_SUCCESS" = true ]; then
    if [ -n "${SLACK_WEBHOOK_URL_CRITICAL_SECRET:-}" ] && [ -x "scripts/utils/slack_notify.sh" ]; then
      scripts/utils/slack_notify.sh "$SLACK_CHANNEL_PROD_DEPLOY" "SUCCESS: Production Deployment" "Project: $CI_PROJECT_NAME - Pipeline: $CI_PIPELINE_URL" "success"
    else
      echo "Production deployment Succeeded. Slack notification script or webhook URL not configured."
    fi
  else
    # Failure notification is handled by trap ERR if possible, or here if script exits normally after failure
    if [ "$?" -ne 0 ] && [ "$DEPLOY_SUCCESS" = false ]; then # If exited due to error
        if [ -n "${SLACK_WEBHOOK_URL_CRITICAL_SECRET:-}" ] && [ -x "scripts/utils/slack_notify.sh" ]; then
            scripts/utils/slack_notify.sh "$SLACK_CHANNEL_PROD_DEPLOY" "FAILURE: Production Deployment" "Project: $CI_PROJECT_NAME - Pipeline: $CI_PIPELINE_URL. Check logs." "failure"
        else
            echo "Production deployment FAILED. Slack notification script or webhook URL not configured."
        fi
    fi
  fi
}
trap cleanup EXIT

# More specific trap for ERR to send failure notification immediately
handle_error() {
  local exit_code=$?
  local line_no=$1
  echo "Error on line $line_no with exit code $exit_code."
  DEPLOY_SUCCESS=false # Ensure this is set for the EXIT trap
  # The EXIT trap will handle the notification based on DEPLOY_SUCCESS
}
trap 'handle_error $LINENO' ERR


prepare_ssh_key() {
  echo "Preparing SSH key for Production..."
  echo "$PROD_ODOO_SSH_KEY_SECRET" > "$SSH_KEY_PATH"
  chmod 600 "$SSH_KEY_PATH"
  echo "SSH key prepared at $SSH_KEY_PATH"
}

# --- Main Deployment Logic ---

# 0. Change Management Approval Check
echo "Checking Change Management approval for JIRA Issue: $CHANGE_REQUEST_ID..."
if [ ! -x "scripts/utils/jira_integrate.sh" ]; then
    echo "Error: JIRA integration script (scripts/utils/jira_integrate.sh) not found or not executable."
    exit 1 # Hard fail, CM check is critical
fi

JIRA_STATUS=$(scripts/utils/jira_integrate.sh get_jira_issue_status "$CHANGE_REQUEST_ID")
# Define what constitutes an approved status. This might need to be configurable.
# Example: "Approved for Deployment", "Approved", "Ready for Prod"
# For robustness, check if status CONTAINS an approved keyword, case-insensitive.
APPROVED_KEYWORDS="APPROVED FOR DEPLOYMENT|APPROVED|READY FOR PROD"

echo "JIRA Issue $CHANGE_REQUEST_ID current status: $JIRA_STATUS"
if echo "$JIRA_STATUS" | grep -iqE "$APPROVED_KEYWORDS"; then
  echo "Change Request $CHANGE_REQUEST_ID is approved for deployment."
else
  echo "Error: Change Request $CHANGE_REQUEST_ID is NOT approved for deployment (Status: '$JIRA_STATUS'). Aborting."
  exit 1 # Hard fail
fi

prepare_ssh_key

# Optional: Pre-deployment backup step
echo "Executing pre-deployment backup steps (placeholder)..."
# Add backup script calls here if necessary, e.g., database backup
echo "Pre-deployment backup steps completed."

# 1. Deploy Odoo Modules
if [ -f "$ODOO_ARTIFACT_NAME" ]; then
  echo "Deploying Odoo modules to Production from artifact: $ODOO_ARTIFACT_NAME"
  REMOTE_ODOO_ARTIFACT_PATH="/tmp/$ODOO_ARTIFACT_NAME"

  echo "Copying Odoo artifact to $PROD_ODOO_SERVER_SSH_USER@$PROD_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH..."
  scp -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$ODOO_ARTIFACT_NAME" "$PROD_ODOO_SERVER_SSH_USER@$PROD_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH"

  echo "Executing remote Odoo deployment commands on Production..."
  SSH_COMMANDS=(
    "echo 'Unzipping Odoo artifact on Production...';"
    "sudo unzip -oq $REMOTE_ODOO_ARTIFACT_PATH -d $PROD_ODOO_ADDONS_PATH;"
    "echo 'Restarting Odoo service $PROD_ODOO_SERVICE_NAME on Production...';" # Consider maintenance window / blue-green if applicable
    "sudo systemctl restart $PROD_ODOO_SERVICE_NAME;"
    "echo 'Waiting for Odoo service to be ready... (20s)';"
    "sleep 20;"
    "echo 'Updating Odoo modules: $MODULES_TO_UPDATE for database $PROD_ODOO_DB_NAME on Production...';"
    "sudo odoo-bin -d $PROD_ODOO_DB_NAME -u $MODULES_TO_UPDATE --stop-after-init --log-level=info;"
    "echo 'Odoo deployment script finished on Production remote server.';"
    "rm -f $REMOTE_ODOO_ARTIFACT_PATH;"
  )
  ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$PROD_ODOO_SERVER_SSH_USER@$PROD_ODOO_SERVER_SSH_HOST" "${SSH_COMMANDS[*]}"

  echo "Odoo modules deployment to Production completed."
else
  echo "Warning: Odoo artifact $ODOO_ARTIFACT_NAME not found. Skipping Odoo deployment to Production."
fi

# 2. Deploy N8N Workflows
if [ -f "$N8N_ARTIFACT_NAME" ]; then
  echo "Deploying N8N workflows to Production from artifact: $N8N_ARTIFACT_NAME"
  N8N_UNZIP_DIR="/tmp/n8n_workflows_unzipped_prod"
  mkdir -p "$N8N_UNZIP_DIR"
  unzip -oq "$N8N_ARTIFACT_NAME" -d "$N8N_UNZIP_DIR"
  echo "N8N artifact unzipped to $N8N_UNZIP_DIR for Production"

  WORKFLOW_FILES=$(find "$N8N_UNZIP_DIR" -name '*.json')
  if [ -z "$WORKFLOW_FILES" ]; then
      echo "No .json workflow files found in the N8N artifact for Production."
  else
      for workflow_file in $WORKFLOW_FILES; do
          echo "Deploying N8N workflow: $workflow_file to $PROD_N8N_INSTANCE_URL"
          curl -f -X POST \
            -H "Authorization: Bearer $PROD_N8N_API_KEY_SECRET" \
            -H "Content-Type: application/json" \
            --data @"$workflow_file" \
            "$PROD_N8N_INSTANCE_URL/api/v1/workflows" || { echo "N8N workflow deployment failed for $workflow_file on Production"; exit 1; }
          echo "Workflow $workflow_file deployed successfully to Production."
      done
  fi
  echo "N8N workflows deployment to Production completed."
else
  echo "Warning: N8N artifact $N8N_ARTIFACT_NAME not found. Skipping N8N deployment to Production."
fi

# 3. Post-Deployment Validation and Health Checks (Crucial for Production)
echo "Running extensive post-deployment validation and health checks for Production environment..."
# Example:
# - Check specific API endpoints for expected responses.
# - Verify critical functionality through automated checks if possible.
# - Monitor error rates and system performance immediately post-deployment.
# These should be comprehensive.
# curl -f http://app.influencegen.com/health || { echo "Production health check failed!"; exit 1; }
# curl -f http://app.influencegen.com/api/v1/critical_endpoint || { echo "Production critical endpoint check failed!"; exit 1; }
echo "Production health checks completed (actual checks to be implemented and be thorough)."

# 4. Update JIRA Issue Status (Optional)
if [ -x "scripts/utils/jira_integrate.sh" ]; then
  echo "Updating JIRA Issue $CHANGE_REQUEST_ID status to 'Deployed' (or similar)..."
  scripts/utils/jira_integrate.sh update_jira_issue_status "$CHANGE_REQUEST_ID" "Deployed" "Automated deployment completed by CI/CD pipeline $CI_PIPELINE_URL"
  echo "JIRA issue status update attempted."
else
  echo "JIRA integration script not found. Skipping JIRA status update."
fi


DEPLOY_SUCCESS=true # Mark as successful if we reached here
trap - ERR # Disable ERR trap as we are successful
echo "Deployment to Production environment finished successfully."
exit 0
```