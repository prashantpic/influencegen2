```bash
#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting deployment to Staging environment..."

# --- Configuration - Expected Environment Variables ---
: "${STAGING_ODOO_SERVER_SSH_HOST:?Error: STAGING_ODOO_SERVER_SSH_HOST not set.}"
: "${STAGING_ODOO_SERVER_SSH_USER:?Error: STAGING_ODOO_SERVER_SSH_USER not set.}"
: "${STAGING_ODOO_SSH_KEY_SECRET:?Error: STAGING_ODOO_SSH_KEY_SECRET not set.}"
: "${STAGING_ODOO_ADDONS_PATH:?Error: STAGING_ODOO_ADDONS_PATH not set.}"
: "${STAGING_ODOO_DB_NAME:?Error: STAGING_ODOO_DB_NAME not set.}"
: "${STAGING_ODOO_SERVICE_NAME:?Error: STAGING_ODOO_SERVICE_NAME not set.}"

: "${STAGING_N8N_INSTANCE_URL:?Error: STAGING_N8N_INSTANCE_URL not set.}"
: "${STAGING_N8N_API_KEY_SECRET:?Error: STAGING_N8N_API_KEY_SECRET not set.}"

: "${ODOO_ARTIFACT_NAME:?Error: ODOO_ARTIFACT_NAME not set.}"
: "${N8N_ARTIFACT_NAME:?Error: N8N_ARTIFACT_NAME not set.}"

MODULES_TO_UPDATE="${ODOO_MODULES_TO_UPDATE:-influence_gen_portal,influence_gen_campaign}"

SSH_KEY_PATH="/tmp/staging_deploy_ssh_key_$(date +%s%N)"

# --- Helper Functions ---
cleanup() {
  echo "Cleaning up temporary files..."
  rm -f "$SSH_KEY_PATH"
  rm -rf "/tmp/n8n_workflows_unzipped_staging"
}
trap cleanup EXIT

prepare_ssh_key() {
  echo "Preparing SSH key for Staging..."
  echo "$STAGING_ODOO_SSH_KEY_SECRET" > "$SSH_KEY_PATH"
  chmod 600 "$SSH_KEY_PATH"
  echo "SSH key prepared at $SSH_KEY_PATH"
}

# --- Main Deployment Logic ---

prepare_ssh_key

# 1. Deploy Odoo Modules
if [ -f "$ODOO_ARTIFACT_NAME" ]; then
  echo "Deploying Odoo modules to Staging from artifact: $ODOO_ARTIFACT_NAME"
  REMOTE_ODOO_ARTIFACT_PATH="/tmp/$ODOO_ARTIFACT_NAME"

  echo "Copying Odoo artifact to $STAGING_ODOO_SERVER_SSH_USER@$STAGING_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH..."
  scp -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$ODOO_ARTIFACT_NAME" "$STAGING_ODOO_SERVER_SSH_USER@$STAGING_ODOO_SERVER_SSH_HOST:$REMOTE_ODOO_ARTIFACT_PATH"

  echo "Executing remote Odoo deployment commands on Staging..."
  SSH_COMMANDS=(
    "echo 'Unzipping Odoo artifact on Staging...';"
    "sudo unzip -oq $REMOTE_ODOO_ARTIFACT_PATH -d $STAGING_ODOO_ADDONS_PATH;"
    "echo 'Restarting Odoo service $STAGING_ODOO_SERVICE_NAME on Staging...';"
    "sudo systemctl restart $STAGING_ODOO_SERVICE_NAME;"
    "echo 'Waiting for Odoo service to be ready... (15s)';"
    "sleep 15;"
    "echo 'Updating Odoo modules: $MODULES_TO_UPDATE for database $STAGING_ODOO_DB_NAME on Staging...';"
    "sudo odoo-bin -d $STAGING_ODOO_DB_NAME -u $MODULES_TO_UPDATE --stop-after-init --log-level=info;"
    "echo 'Odoo deployment script finished on Staging remote server.';"
    "rm -f $REMOTE_ODOO_ARTIFACT_PATH;"
  )
  
  ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      "$STAGING_ODOO_SERVER_SSH_USER@$STAGING_ODOO_SERVER_SSH_HOST" "${SSH_COMMANDS[*]}"

  echo "Odoo modules deployment to Staging completed."
else
  echo "Warning: Odoo artifact $ODOO_ARTIFACT_NAME not found. Skipping Odoo deployment to Staging."
fi

# 2. Deploy N8N Workflows
if [ -f "$N8N_ARTIFACT_NAME" ]; then
  echo "Deploying N8N workflows to Staging from artifact: $N8N_ARTIFACT_NAME"
  N8N_UNZIP_DIR="/tmp/n8n_workflows_unzipped_staging"
  mkdir -p "$N8N_UNZIP_DIR"
  unzip -oq "$N8N_ARTIFACT_NAME" -d "$N8N_UNZIP_DIR"
  echo "N8N artifact unzipped to $N8N_UNZIP_DIR for Staging"

  WORKFLOW_FILES=$(find "$N8N_UNZIP_DIR" -name '*.json')
  if [ -z "$WORKFLOW_FILES" ]; then
      echo "No .json workflow files found in the N8N artifact for Staging."
  else
      for workflow_file in $WORKFLOW_FILES; do
          echo "Deploying N8N workflow: $workflow_file to $STAGING_N8N_INSTANCE_URL"
          curl -f -X POST \
            -H "Authorization: Bearer $STAGING_N8N_API_KEY_SECRET" \
            -H "Content-Type: application/json" \
            --data @"$workflow_file" \
            "$STAGING_N8N_INSTANCE_URL/api/v1/workflows" || { echo "N8N workflow deployment failed for $workflow_file on Staging"; exit 1; }
          echo "Workflow $workflow_file deployed successfully to Staging."
      done
  fi
  echo "N8N workflows deployment to Staging completed."
else
  echo "Warning: N8N artifact $N8N_ARTIFACT_NAME not found. Skipping N8N deployment to Staging."
fi

# 3. Post-Deployment Health Checks for Staging
echo "Running post-deployment health checks for Staging environment..."
# Example: curl -f http://staging-app.influencegen.com/health
# These should be more rigorous than dev.
echo "Staging health checks completed (actual checks to be implemented)."

echo "Deployment to Staging environment finished successfully."
exit 0
```