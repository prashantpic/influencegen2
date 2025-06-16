```bash
#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting deployment to Development environment..."

# --- Configuration - Expected Environment Variables ---
: "${DEV_ODOO_SERVER_SSH_HOST:?Error: DEV_ODOO_SERVER_SSH_HOST not set.}"
: "${DEV_ODOO_SERVER_SSH_USER:?Error: DEV_ODOO_SERVER_SSH_USER not set.}"
: "${DEV_ODOO_SSH_KEY_SECRET:?Error: DEV_ODOO_SSH_KEY_SECRET not set.}" # This is the key content
: "${DEV_ODOO_ADDONS_PATH:?Error: DEV_ODOO_ADDONS_PATH not set.}"
: "${DEV_ODOO_DB_NAME:?Error: DEV_ODOO_DB_NAME not set.}"
: "${DEV_ODOO_SERVICE_NAME:?Error: DEV_ODOO_SERVICE_NAME not set.}"

: "${DEV_N8N_INSTANCE_URL:?Error: DEV_N8N_INSTANCE_URL not set.}"
# DEV_N8N_API_KEY_SECRET is expected to be the actual API key
: "${DEV_N8N_API_KEY_SECRET:?Error: DEV_N8N_API_KEY_SECRET not set.}"

: "${ODOO_ARTIFACT_NAME:?Error: ODOO_ARTIFACT_NAME (e.g., odoo_addons.zip) not set.}"
: "${N8N_ARTIFACT_NAME:?Error: N8N_ARTIFACT_NAME (e.g., n8n_workflows.zip) not set.}"

MODULES_TO_UPDATE="${ODOO_MODULES_TO_UPDATE:-influence_gen_portal,influence_gen_campaign}" # Default or from CI var

SSH_KEY_PATH="/tmp/dev_deploy_ssh_key_$(date +%s%N)"

# --- Helper Functions ---
cleanup() {
  echo "Cleaning up temporary files..."
  rm -f "$SSH_KEY_PATH"
  rm -rf "/tmp/n8n_workflows_unzipped_dev"
}
trap cleanup EXIT

prepare_ssh_key() {
  echo "Preparing SSH key..."
  echo "$DEV_ODOO_SSH_KEY_SECRET" > "$SSH_KEY_PATH"
  chmod 600 "$SSH_KEY_PATH"
  echo "SSH key prepared at $SSH_KEY_PATH"
}

# --- Main Deployment Logic ---

prepare_ssh_key

# 1. Deploy Odoo Modules
if [ -f "$ODOO_ARTIFACT_NAME" ]; then
  echo "Deploying Odoo modules from artifact: $ODOO_ARTIFACT_NAME"
  REMOTE_ODOO_ARTIFACT_PATH="/tmp/$ODOO_ARTIFACT_NAME"

  echo "Copying Odoo artifact to $DEV_ODOO_SERVER_SSH_USER@$DEV_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH..."
  scp -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$ODOO_ARTIFACT_NAME" "$DEV_ODOO_SERVER_SSH_USER@$DEV_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH"

  echo "Executing remote Odoo deployment commands..."
  # -o: overwrite files without prompting
  # -q: quiet mode for unzip
  # Ensure DEV_ODOO_ADDONS_PATH exists on the remote server.
  # The user running odoo-bin needs permissions to update modules. Using sudo if odoo-bin isn't run by odoo user or similar.
  # Adjust sudo usage based on server setup.
  SSH_COMMANDS=(
    "echo 'Unzipping Odoo artifact...';"
    "sudo unzip -oq $REMOTE_ODOO_ARTIFACT_PATH -d $DEV_ODOO_ADDONS_PATH;"
    "echo 'Restarting Odoo service $DEV_ODOO_SERVICE_NAME...';"
    "sudo systemctl restart $DEV_ODOO_SERVICE_NAME;"
    "echo 'Waiting for Odoo service to be ready... (10s)';"
    "sleep 10;" # Give Odoo some time to restart
    "echo 'Updating Odoo modules: $MODULES_TO_UPDATE for database $DEV_ODOO_DB_NAME...';"
    # Run odoo-bin as the odoo user if possible, or ensure correct permissions.
    # Example: sudo -u odoo odoo-bin ... or ensure the SSH user can run odoo-bin correctly.
    "sudo odoo-bin -d $DEV_ODOO_DB_NAME -u $MODULES_TO_UPDATE --stop-after-init --log-level=info;"
    "echo 'Odoo deployment script finished on remote server.';"
    "rm -f $REMOTE_ODOO_ARTIFACT_PATH;"
  )
  
  ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$DEV_ODOO_SERVER_SSH_USER@$DEV_ODOO_SERVER_SSH_HOST" "${SSH_COMMANDS[*]}"
  
  echo "Odoo modules deployment to Dev completed."
else
  echo "Warning: Odoo artifact $ODOO_ARTIFACT_NAME not found. Skipping Odoo deployment."
fi

# 2. Deploy N8N Workflows
if [ -f "$N8N_ARTIFACT_NAME" ]; then
  echo "Deploying N8N workflows from artifact: $N8N_ARTIFACT_NAME"
  N8N_UNZIP_DIR="/tmp/n8n_workflows_unzipped_dev"
  mkdir -p "$N8N_UNZIP_DIR"
  unzip -oq "$N8N_ARTIFACT_NAME" -d "$N8N_UNZIP_DIR"
  echo "N8N artifact unzipped to $N8N_UNZIP_DIR"

  WORKFLOW_FILES=$(find "$N8N_UNZIP_DIR" -name '*.json')
  if [ -z "$WORKFLOW_FILES" ]; then
      echo "No .json workflow files found in the N8N artifact."
  else
      for workflow_file in $WORKFLOW_FILES; do
          echo "Deploying N8N workflow: $workflow_file to $DEV_N8N_INSTANCE_URL"
          # N8N API: POST to /rest/workflows to create or update if ID exists in JSON and matches.
          # The exact API endpoint and method (POST/PUT) might vary based on N8N version or setup.
          # This assumes POST can create or update.
          API_RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
              -X POST \
              -H "Authorization: Bearer $DEV_N8N_API_KEY_SECRET" \
              -H "Content-Type: application/json" \
              --data @"$workflow_file" \
              "$DEV_N8N_INSTANCE_URL/api/v1/workflows") # Ensure this is the correct endpoint

          if [ "$API_RESPONSE_CODE" -ge 200 ] && [ "$API_RESPONSE_CODE" -lt 300 ]; then
              echo "Workflow $workflow_file deployed successfully (HTTP $API_RESPONSE_CODE)."
          else
              echo "Error deploying workflow $workflow_file (HTTP $API_RESPONSE_CODE)."
              # Optionally, retrieve and print response body for debugging:
              # curl -v -X POST ... to see full details.
              # For now, just report error code.
              # Consider if one failed workflow should stop the entire deployment. 'set -e' will handle this if curl exits non-zero on HTTP error.
              # `curl -f` can make curl exit non-zero on HTTP errors.
              # Let's add -f for safer error handling.
              curl -f -X POST \
                -H "Authorization: Bearer $DEV_N8N_API_KEY_SECRET" \
                -H "Content-Type: application/json" \
                --data @"$workflow_file" \
                "$DEV_N8N_INSTANCE_URL/api/v1/workflows" || { echo "N8N workflow deployment failed for $workflow_file"; exit 1; }
          fi
      done
  fi
  echo "N8N workflows deployment to Dev completed."
else
  echo "Warning: N8N artifact $N8N_ARTIFACT_NAME not found. Skipping N8N deployment."
fi

# 3. Post-Deployment Health Checks (Placeholder)
echo "Running post-deployment health checks for Dev environment..."
# Example: curl -f http://dev-some-service.influencegen.com/health
echo "Health checks completed (actual checks to be implemented)."

echo "Deployment to Development environment finished successfully."
exit 0
```