```bash
#!/bin/bash

# Script to destroy a specific environment using Terraform

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to display usage
usage() {
  echo "Usage: $0 <environment>"
  echo "Environments: dev, staging, production"
  exit 1
}

# Check for environment argument
if [ "$#" -ne 1 ]; then
  usage
fi

ENV_NAME="$1"

# Validate environment name
if [ "$ENV_NAME" != "dev" ] && [ "$ENV_NAME" != "staging" ] && [ "$ENV_NAME" != "production" ]; then
  echo "Error: Invalid environment name '$ENV_NAME'."
  usage
fi

echo "Destroying environment: $ENV_NAME"

# --- Terraform Destruction ---
echo "--- Running Terraform to destroy infrastructure ---"
TERRAFORM_DIR="./terraform/environments/${ENV_NAME}"
TFVARS_FILE="${ENV_NAME}.tfvars" # Terraform searches for this file in current dir

if [ ! -d "$TERRAFORM_DIR" ]; then
  echo "Error: Terraform environment directory not found: $TERRAFORM_DIR"
  exit 1
fi

TFVARS_FILE_PATH="${TERRAFORM_DIR}/${TFVARS_FILE}"
if [ ! -f "$TFVARS_FILE_PATH" ]; then
  echo "Error: Terraform variables file not found: $TFVARS_FILE_PATH"
  exit 1
fi

cd "$TERRAFORM_DIR" || exit 1

# Crucial: Add a confirmation prompt, especially for production
if [ "$ENV_NAME" = "staging" ] || [ "$ENV_NAME" = "production" ]; then
  echo "WARNING: This will destroy ALL infrastructure for the '${ENV_NAME}' environment!"
  read -r -p "Are you absolutely sure you want to proceed? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Destruction cancelled."
    exit 0
  fi
  read -r -p "To confirm, type the environment name ('${ENV_NAME}') again: " confirm_name
  if [ "$confirm_name" != "$ENV_NAME" ]; then
      echo "Environment name mismatch. Destruction cancelled."
      exit 1
  fi
  echo "Confirmation received. Proceeding with destruction..."
fi


# Initialize Terraform (needed to load backend state for destroy)
echo "Running terraform init..."
terraform init -upgrade -backend=true -reconfigure

# Run terraform destroy
echo "Running terraform destroy..."
# Use -auto-approve for automation, but interactive confirmation is safer for manual runs
# The script already has manual confirmation steps for staging/prod
terraform destroy -auto-approve -var-file="$TFVARS_FILE"

# Return to the script's starting directory
cd - > /dev/null || exit 1

echo "Destruction of environment '$ENV_NAME' finished."
```