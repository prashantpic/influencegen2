```bash
#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting deployment of training materials..."

# --- Configuration - Expected Environment Variables ---
: "${TRAINING_MATERIALS_ARTIFACT_PATH:?Error: TRAINING_MATERIALS_ARTIFACT_PATH not set.}"
: "${TRAINING_PORTAL_TARGET_TYPE:?Error: TRAINING_PORTAL_TARGET_TYPE (e.g., S3, WEBSERVER_SSH) not set.}"

UNZIPPED_MATERIALS_DIR="/tmp/training_materials_unzipped_$(date +%s%N)"
SSH_KEY_PATH="/tmp/training_deploy_ssh_key_$(date +%s%N)" # Only used for WEBSERVER_SSH

cleanup() {
  echo "Cleaning up temporary training material files..."
  rm -rf "$UNZIPPED_MATERIALS_DIR"
  if [ "$TRAINING_PORTAL_TARGET_TYPE" == "WEBSERVER_SSH" ]; then
    rm -f "$SSH_KEY_PATH"
  fi
}
trap cleanup EXIT

# Validate artifact existence
if [ ! -f "$TRAINING_MATERIALS_ARTIFACT_PATH" ]; then
  echo "Error: Training materials artifact '$TRAINING_MATERIALS_ARTIFACT_PATH' not found."
  exit 1
fi

echo "Unzipping training materials artifact: $TRAINING_MATERIALS_ARTIFACT_PATH"
mkdir -p "$UNZIPPED_MATERIALS_DIR"
if ! unzip -oq "$TRAINING_MATERIALS_ARTIFACT_PATH" -d "$UNZIPPED_MATERIALS_DIR"; then
  echo "Error: Failed to unzip training materials artifact."
  exit 1
fi
echo "Training materials unzipped to $UNZIPPED_MATERIALS_DIR"

# --- Deployment Logic based on Target Type ---

if [ "$TRAINING_PORTAL_TARGET_TYPE" == "WEBSERVER_SSH" ]; then
  echo "Deploying training materials to Webserver via SSH..."
  : "${TRAINING_PORTAL_SSH_HOST:?Error: TRAINING_PORTAL_SSH_HOST not set for WEBSERVER_SSH target.}"
  : "${TRAINING_PORTAL_SSH_USER:?Error: TRAINING_PORTAL_SSH_USER not set for WEBSERVER_SSH target.}"
  : "${TRAINING_PORTAL_SSH_KEY_SECRET:?Error: TRAINING_PORTAL_SSH_KEY_SECRET not set for WEBSERVER_SSH target.}"
  : "${TRAINING_PORTAL_TARGET_DIR:?Error: TRAINING_PORTAL_TARGET_DIR not set for WEBSERVER_SSH target.}"

  echo "Preparing SSH key for training materials deployment..."
  echo "$TRAINING_PORTAL_SSH_KEY_SECRET" > "$SSH_KEY_PATH"
  chmod 600 "$SSH_KEY_PATH"
  echo "SSH key prepared at $SSH_KEY_PATH"

  echo "Using rsync to transfer files to $TRAINING_PORTAL_SSH_USER@$TRAINING_PORTAL_SSH_HOST:$TRAINING_PORTAL_TARGET_DIR/"
  # -a: archive mode (recursive, preserves permissions, etc.)
  # -v: verbose
  # -z: compress file data during the transfer
  # --delete: delete extraneous files from destination dirs
  if rsync -avz --delete -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
     "$UNZIPPED_MATERIALS_DIR/" "$TRAINING_PORTAL_SSH_USER@$TRAINING_PORTAL_SSH_HOST:$TRAINING_PORTAL_TARGET_DIR/"; then
    echo "Training materials successfully deployed via SSH using rsync."
  else
    echo "Error: Failed to deploy training materials via SSH using rsync."
    exit 1
  fi

elif [ "$TRAINING_PORTAL_TARGET_TYPE" == "S3" ]; then
  echo "Deploying training materials to S3..."
  : "${TRAINING_S3_BUCKET_URL:?Error: TRAINING_S3_BUCKET_URL (e.g., s3://my-bucket/path) not set for S3 target.}"
  # AWS CLI will use AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION from CI/CD variables.
  # Ensure these are set in the GitLab CI/CD job environment.
  if ! command -v aws &> /dev/null; then
      echo "Error: AWS CLI (aws) could not be found. It's required for S3 deployment."
      exit 1
  fi
  : "${AWS_ACCESS_KEY_ID:?Error: AWS_ACCESS_KEY_ID not set for S3 deployment.}"
  : "${AWS_SECRET_ACCESS_KEY:?Error: AWS_SECRET_ACCESS_KEY not set for S3 deployment.}"
  : "${AWS_DEFAULT_REGION:?Error: AWS_DEFAULT_REGION not set for S3 deployment.}"


  echo "Using AWS S3 sync to transfer files to $TRAINING_S3_BUCKET_URL"
  # --delete: Files that exist in the destination but not in the source are deleted during sync.
  if aws s3 sync "$UNZIPPED_MATERIALS_DIR/" "$TRAINING_S3_BUCKET_URL/" --delete; then
    echo "Training materials successfully synced to S3 bucket $TRAINING_S3_BUCKET_URL."
  else
    echo "Error: Failed to sync training materials to S3 bucket."
    exit 1
  fi

else
  echo "Error: Unknown TRAINING_PORTAL_TARGET_TYPE '$TRAINING_PORTAL_TARGET_TYPE'. Supported types are 'S3', 'WEBSERVER_SSH'."
  exit 1
fi

echo "Training materials deployment finished successfully."
exit 0
```