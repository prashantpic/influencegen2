```bash
#!/bin/bash

# Script to deploy a specific environment using Terraform and Ansible

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

echo "Deploying environment: $ENV_NAME"

# --- Terraform Provisioning ---
echo "--- Running Terraform to provision infrastructure ---"
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

# Initialize Terraform
echo "Running terraform init..."
terraform init -upgrade -backend=true -reconfigure

# Validate Terraform configuration
echo "Running terraform validate..."
terraform validate

# Plan Terraform changes
echo "Running terraform plan..."
terraform plan -out="${ENV_NAME}.tfplan" -var-file="$TFVARS_FILE"

# Apply Terraform changes
# Add confirmation for staging/production
if [ "$ENV_NAME" = "staging" ] || [ "$ENV_NAME" = "production" ]; then
  read -r -p "Review the plan above. Are you sure you want to apply these changes to ${ENV_NAME}? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled."
    exit 0
  fi
fi

echo "Running terraform apply..."
terraform apply -auto-approve "${ENV_NAME}.tfplan"

# Capture Terraform outputs for Ansible inventory
echo "Capturing Terraform outputs..."
# Using json output and jq to parse
if ! command -v jq &> /dev/null; then
    echo "Warning: jq is not installed. Cannot automatically generate Ansible inventory."
    echo "Please install jq (e.g., sudo apt-get install jq) or manually update the inventory."
    # Exit if jq is mandatory for your dynamic inventory script
    # exit 1
else
    # Example: Assuming outputs are 'odoo_instance_ips', 'n8n_instance_ip', 'ai_server_ips'
    # Adjust jq queries based on actual output structure
    ODDO_IPS=$(terraform output -json odoo_instance_ips | jq -r '.[]')
    N8N_IP=$(terraform output -json n8n_instance_ip | jq -r '.')
    AI_IPS=$(terraform output -json ai_server_ips | jq -r '.[]')
    DB_ENDPOINT=$(terraform output -json db_endpoint | jq -r '.')
    DB_PORT=$(terraform output -json db_port | jq -r '.')
    DB_NAME=$(terraform output -json db_name | jq -r '.')
    # Capture secret ARNs to pass to Ansible (securely!)
    ODDO_DB_USER_SECRET_ARN=$(terraform output -json db_user_secret_arn | jq -r '.')
    ODDO_DB_PASSWORD_SECRET_ARN=$(terraform output -json db_password_secret_arn | jq -r '.')
    N8N_DB_USER_SECRET_ARN=$(terraform output -json n8n_db_user_secret_arn | jq -r '.')
    N8N_DB_PASSWORD_SECRET_ARN=$(terraform output -json n8n_db_password_secret_arn | jq -r '.')
    N8N_ENCRYPTION_KEY_SECRET_ARN=$(terraform output -json n8n_encryption_key_secret_arn | jq -r '.')
    ODDO_ADMIN_PASSWORD_SECRET_ARN=$(terraform output -json odoo_admin_password_secret_arn | jq -r '.')


    # --- Generate Ansible Inventory (Simple .ini example) ---
    echo "Generating Ansible inventory file..."
    ANSIBLE_INVENTORY_DIR="../../ansible/inventories/${ENV_NAME}"
    ANSIBLE_INVENTORY_FILE="${ANSIBLE_INVENTORY_DIR}/hosts.ini"

    mkdir -p "$ANSIBLE_INVENTORY_DIR"

    {
      echo "# Generated inventory for ${ENV_NAME} environment"
      echo "# Created by deploy_environment.sh script"
      echo ""
      echo "[odoo_servers]"
      for ip in $ODDO_IPS; do
        echo "$ip"
      done
      echo ""
      echo "[n8n_servers]"
      echo "$N8N_IP"
      echo ""
      echo "[ai_servers]"
      for ip in $AI_IPS; do
        echo "$ip"
      done
      echo ""
      # Add database host if not fully managed like RDS and needs Ansible config
      # echo "[db_servers]"
      # echo "$DB_ENDPOINT"
      # echo ""
    } > "$ANSIBLE_INVENTORY_FILE"

    echo "Ansible inventory generated at $ANSIBLE_INVENTORY_FILE"

fi # End jq check/inventory generation


# Return to the script's starting directory (InfluenceGen.Infrastructure.IaC root)
cd - > /dev/null || exit 1

# --- Ansible Configuration ---
echo "--- Running Ansible to configure servers ---"
ANSIBLE_DIR="./ansible"
ANSIBLE_PLAYBOOK="${ANSIBLE_DIR}/playbooks/site.yml"
# Inventory path is now relative to ansible.cfg which specifies 'inventories/'
ANSIBLE_INVENTORY_SUB_PATH="inventories/${ENV_NAME}/hosts.ini"
ANSIBLE_GROUP_VARS_FILE="${ANSIBLE_DIR}/group_vars/${ENV_NAME}.yml" # Assuming group_vars are named by env

if [ ! -d "$ANSIBLE_DIR" ]; then
  echo "Error: Ansible directory not found: $ANSIBLE_DIR"
  exit 1
fi

if [ ! -f "$ANSIBLE_PLAYBOOK" ]; then
  echo "Error: Ansible playbook not found: $ANSIBLE_PLAYBOOK"
  exit 1
fi

if [ ! -f "${ANSIBLE_DIR}/${ANSIBLE_INVENTORY_SUB_PATH}" ]; then
    echo "Error: Ansible inventory file not found: ${ANSIBLE_DIR}/${ANSIBLE_INVENTORY_SUB_PATH}. Cannot run Ansible."
    echo "Please ensure Terraform output was successful or manually create it."
    exit 1
fi

cd "$ANSIBLE_DIR" || exit 1

# Run the main Ansible playbook
# Pass environment-specific vars and secrets (SECRETS MUST BE HANDLED SECURELY, e.g. VAULT)
# Example using extra-vars. Sensitive variables should be passed securely (e.g., via vault-password-file, environment variables, or lookup plugins in vars files)
# For this example, we'll just reference the files and variables.
echo "Running ansible-playbook..."

# Note on secrets: Database credentials and other secrets obtained from Terraform outputs (ARNs)
# should NOT be passed directly as --extra-vars on the command line in a non-secure manner.
# A common approach:
# 1. Have Ansible use lookup plugins (e.g., community.aws.aws_secret) directly in roles/vars files, referencing the ARNs.
#    The EC2 instances running Ansible (or the CI/CD agent) need IAM permissions to access Secrets Manager.
# 2. Fetch secrets in this script *then* encrypt them with Ansible Vault ad-hoc *then* pass the vaulted strings.
# 3. Pass the vault password securely to the `ansible-playbook` command.

# Recommended example using lookup plugins in Ansible vars:
# Ensure group_vars/<env>.yml references the Secret ARNs using lookup plugins.
# Ensure the executing user/role has Secrets Manager read permissions.
# You still need to pass environment name if roles depend on it.

# Pass necessary variables for playbook to reference using group_vars/<env_name>.yml
# Also passing Terraform outputs that might be used by roles directly, or help locate secrets.
# IMPORTANT: For PRODUCTION, ensure `ansible-playbook` is run with `--vault-password-file`
# or another secure method for Ansible Vault.
VAULT_PASSWORD_FILE_PATH="~/.vault_password" # Default, can be overridden by env var ANSIBLE_VAULT_PASSWORD_FILE

if [ -z "$ANSIBLE_VAULT_PASSWORD_FILE" ] && [ ! -f "$VAULT_PASSWORD_FILE_PATH" ]; then
    echo "Warning: Ansible Vault password file not found at $VAULT_PASSWORD_FILE_PATH and ANSIBLE_VAULT_PASSWORD_FILE is not set."
    echo "Ansible may prompt for vault password or fail if vaulted variables are used without a password source."
fi

ansible-playbook -i "$ANSIBLE_INVENTORY_SUB_PATH" "playbooks/site.yml" \
  -e "env_name=${ENV_NAME}" \
  -e "db_endpoint=${DB_ENDPOINT}" \
  -e "db_port=${DB_PORT}" \
  -e "db_name=${DB_NAME}" \
  -e "odoo_db_user_secret_arn=${ODDO_DB_USER_SECRET_ARN}" \
  -e "odoo_db_password_secret_arn=${ODDO_DB_PASSWORD_SECRET_ARN}" \
  -e "n8n_db_user_secret_arn=${N8N_DB_USER_SECRET_ARN}" \
  -e "n8n_db_password_secret_arn=${N8N_DB_PASSWORD_SECRET_ARN}" \
  -e "n8n_encryption_key_secret_arn=${N8N_ENCRYPTION_KEY_SECRET_ARN}" \
  -e "odoo_admin_password_secret_arn=${ODDO_ADMIN_PASSWORD_SECRET_ARN}" \
  ${ANSIBLE_VAULT_PASSWORD_FILE:+--vault-password-file "$ANSIBLE_VAULT_PASSWORD_FILE"} # Use env var if set
  # If ANSIBLE_VAULT_PASSWORD_FILE is not set, Ansible will try default methods (prompt, ~/.vault_password file if exists)


# Return to the script's starting directory
cd - > /dev/null || exit 1

echo "Deployment of environment '$ENV_NAME' finished."
```