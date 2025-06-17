# Software Design Specification: InfluenceGen.Infrastructure.IaC

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Infrastructure.IaC` repository. This repository is responsible for managing Infrastructure as Code (IaC) scripts using Terraform and Ansible to provision and configure all necessary cloud and hosting environments for the InfluenceGen platform. This includes environments for Odoo 18, N8N, the AI Model Serving Infrastructure, and PostgreSQL databases.

The primary objectives are to ensure consistent, repeatable, version-controlled, and automated setup of Development, Staging/UAT, and Production environments, achieving parity between Staging and Production where specified.

**Requirements Addressed:**
*   `REQ-DDSI-008`: Utilize IaC practices (Terraform, Ansible) for provisioning and managing all target environments. Scripts must be version-controlled and part of an automated deployment process.
*   `REQ-DI-TENV-001`: Establish distinct, fully functional Development, Staging/UAT, and Production environments for Odoo, N8N, and AI model serving infrastructure.
*   `REQ-DI-CM-001`: Implement robust configuration management to ensure consistency across environments, manage environment-specific parameters securely, and automate configuration deployments.
*   `REQ-DI-AISERV-001`: The AI model serving infrastructure must be provisioned with GPU-enabled servers capable of running Flux LoRA models efficiently, including necessary VRAM (e.g., 16GB+, preferably 24GB+ per GPU).
*   `REQ-DI-CM-002`: The Staging/UAT environment must aim for parity with the Production environment in terms of infrastructure, software versions, and configurations to ensure accurate testing and minimize deployment risks.

## 2. System Architecture Overview

The IaC repository employs a layered approach:
1.  **Terraform Layer**: Responsible for provisioning core infrastructure resources on the chosen cloud provider (e.g., AWS, Azure, GCP - assumed AWS for detailed examples unless specified otherwise). This includes networking (VPCs, subnets), compute instances (EC2), managed databases (RDS), and security configurations.
2.  **Ansible Layer**: Responsible for configuring the provisioned infrastructure. This includes installing software (Odoo, N8N, Docker, AI serving applications, dependencies), deploying application code/modules, and managing service configurations.
3.  **Docker Layer**: Defines container images for Odoo and the AI Model Serving application to ensure consistent runtime environments.
4.  **Orchestration Scripts Layer**: Provides scripts to automate the end-to-end deployment and destruction of environments.

All code and configuration will be version-controlled in Git. Secrets management will rely on environment variables passed securely to Terraform/Ansible or integration with a dedicated secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault). For this SDS, we'll assume variables can be securely injected or referenced from a secrets management solution.

## 3. General Principles

*   **Modularity**: Terraform and Ansible code will be organized into reusable modules and roles, respectively.
*   **Idempotency**: Ansible playbooks and roles will be designed to be idempotent.
*   **Parameterization**: Configurations will be parameterized to support different environments (Dev, Staging, Prod) using variable files (`.tfvars` for Terraform, group/host vars for Ansible).
*   **Security**: Adherence to the principle of least privilege for network access (security groups) and IAM roles. Secure handling of secrets.
*   **Version Control**: All IaC scripts, Dockerfiles, and configuration files will be stored in a Git repository.
*   **Automation**: Deployment and configuration processes will be automated via shell scripts and CI/CD pipelines (CI/CD pipeline setup is outside this repository's scope but scripts should support it).
*   **Environment Parity**: Staging environment configurations will mirror production as closely as possible (REQ-DI-CM-002).

## 4. Terraform Infrastructure Provisioning

Terraform will be used to define and provision all cloud infrastructure components.

### 4.1. Common Terraform Configurations
   Located in `terraform/environments/common/`.

   *   **`providers.tf`**:
        *   **Purpose**: Declares and configures Terraform providers (e.g., AWS).
        *   **Content**:
            *   Provider blocks (e.g., `aws`) specifying source, version, and region.
            *   Region can be a variable to allow flexibility.
            *   Required provider versions to ensure consistency.
        *   **Example (AWS)**:
            hcl
            terraform {
              required_providers {
                aws = {
                  source  = "hashicorp/aws"
                  version = "~> 5.0" // Specify appropriate version
                }
              }
              required_version = ">= 1.8.0" // Specify Terraform version
            }

            provider "aws" {
              region = var.aws_region
              // Assume credentials configured via environment variables or IAM roles
            }
            

   *   **`variables.tf`**:
        *   **Purpose**: Defines common input variables used across environments.
        *   **Content**:
            *   `variable "aws_region"`: AWS region for deployment.
            *   `variable "project_name"`: Project name for tagging (e.g., "influencegen").
            *   `variable "default_tags"`: Map of default tags to apply to all resources.
            *   Other shared variables (e.g., common AMI IDs if applicable, though usually environment/region specific).
        *   **Example**:
            hcl
            variable "aws_region" {
              description = "The AWS region to deploy resources in."
              type        = string
              default     = "us-east-1"
            }

            variable "project_name" {
              description = "The name of the project for tagging resources."
              type        = string
              default     = "influencegen"
            }

            variable "default_tags" {
              description = "Default tags to apply to all resources."
              type        = map(string)
              default = {
                Project   = "InfluenceGen"
                ManagedBy = "Terraform"
              }
            }
            

### 4.2. Terraform Modules
   Located in `terraform/modules/`. Each module will have `main.tf`, `variables.tf`, and `outputs.tf`.

   *   **Module: `vpc`**
        *   **Path**: `terraform/modules/vpc/`
        *   **Purpose**: Provisions network foundation (VPC, subnets, gateways, route tables).
        *   **`main.tf`**:
            *   Resources: `aws_vpc`, `aws_subnet` (public and private per AZ), `aws_internet_gateway`, `aws_eip` (for NAT Gateway), `aws_nat_gateway`, `aws_route_table`, `aws_route_table_association`.
            *   Logic: Create VPC, multiple public/private subnets across specified AZs. Setup IGW for public subnets. Setup NAT Gateways in public subnets for private subnet outbound access. Define route tables.
        *   **`variables.tf`**: `vpc_cidr_block`, `public_subnet_cidrs` (list), `private_subnet_cidrs` (list), `availability_zones` (list), `environment_name`, `tags`.
        *   **`outputs.tf`**: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`, `default_security_group_id`.

   *   **Module: `security_groups`**
        *   **Path**: `terraform/modules/security_groups/`
        *   **Purpose**: Defines application-specific security groups.
        *   **`main.tf`**:
            *   Resources: `aws_security_group`, `aws_security_group_rule`.
            *   Logic: Create security groups for Odoo (web, app internal), N8N, AI Server, PostgreSQL, allowing configurable ingress/egress rules.
        *   **`variables.tf`**: `vpc_id`, `security_group_definitions` (list of objects, each defining a group with name, description, and list of ingress/egress rules with port, protocol, cidr_blocks/source_security_group_id).
        *   **`outputs.tf`**: Map of security group IDs (e.g., `odoo_web_sg_id`, `db_sg_id`).

   *   **Module: `rds_postgres`**
        *   **Path**: `terraform/modules/rds_postgres/`
        *   **Purpose**: Provisions managed PostgreSQL database.
        *   **`main.tf`**:
            *   Resources: `aws_db_subnet_group`, `aws_db_instance` (or `aws_rds_cluster` for Aurora).
            *   Logic: Create DB subnet group, provision RDS instance with specified parameters. Use secrets manager for master credentials.
        *   **`variables.tf`**: `db_name`, `engine_version`, `instance_class`, `allocated_storage`, `vpc_security_group_ids`, `db_subnet_group_name` (or subnet_ids to create one), `username_secret_arn`, `password_secret_arn`, `multi_az`, `backup_retention_period`, `tags`, `environment_name`.
        *   **`outputs.tf`**: `db_instance_endpoint`, `db_instance_port`, `db_instance_name`.

   *   **Module: `ec2_instance`** (Generic Compute Instance)
        *   **Path**: `terraform/modules/ec2_instance/`
        *   **Purpose**: Provisions generic EC2 instances.
        *   **`main.tf`**:
            *   Resources: `aws_instance`, `aws_iam_instance_profile` (optional).
            *   Logic: Create EC2 instance with specified AMI, type, key pair, SGs, subnet, user data.
        *   **`variables.tf`**: `instance_name_prefix`, `ami_id`, `instance_type`, `key_name`, `vpc_security_group_ids`, `subnet_id`, `user_data_script` (base64 encoded), `root_block_device_size`, `iam_instance_profile_name` (optional), `tags`.
        *   **`outputs.tf`**: `instance_id`, `public_ip`, `private_ip`.

   *   **Module: `odoo_app`**
        *   **Path**: `terraform/modules/odoo_app/`
        *   **Purpose**: Provisions Odoo application server infrastructure.
        *   **`main.tf`**:
            *   Instantiates `ec2_instance` module for Odoo servers.
            *   Optionally: `aws_lb`, `aws_lb_target_group`, `aws_autoscaling_group` if HA/scaling is required.
            *   Uses security group IDs from `security_groups` module outputs.
        *   **`variables.tf`**: `environment_name`, `instance_count`, `ami_id`, `instance_type`, `key_name`, `odoo_sg_id`, `subnet_ids` (list for ASG/multiple instances), `user_data_odoo_setup` (script name or content), `db_endpoint`, `db_port`, `db_name`, `db_user_secret_arn`, `db_password_secret_arn`, `tags`.
        *   **`outputs.tf`**: `odoo_instance_ids_ips` (map or list of objects).

   *   **Module: `n8n_app`**
        *   **Path**: `terraform/modules/n8n_app/`
        *   **Purpose**: Provisions N8N server infrastructure.
        *   **`main.tf`**:
            *   Instantiates `ec2_instance` module for N8N server (or ECS/EKS resources if containerized).
            *   Uses security group IDs from `security_groups` module outputs.
        *   **`variables.tf`**: `environment_name`, `ami_id`, `instance_type`, `key_name`, `n8n_sg_id`, `subnet_id`, `user_data_n8n_setup`, `n8n_db_type`, `n8n_db_host` (can be RDS endpoint), `n8n_db_port`, `n8n_db_user_secret_arn`, `n8n_db_password_secret_arn`, `n8n_db_name`, `n8n_encryption_key_secret_arn`, `tags`.
        *   **`outputs.tf`**: `n8n_instance_ip`.

   *   **Module: `ai_server`**
        *   **Path**: `terraform/modules/ai_server/`
        *   **Purpose**: Provisions GPU-enabled AI model serving infrastructure. (REQ-DI-AISERV-001)
        *   **`main.tf`**:
            *   Instantiates `ec2_instance` module, specifying GPU instance types (e.g., `g4dn.xlarge`, `p3.2xlarge`).
            *   Uses security group IDs from `security_groups` module outputs.
        *   **`variables.tf`**: `environment_name`, `instance_count`, `ami_id` (GPU-ready AMI), `instance_type` (GPU instance type), `key_name`, `ai_server_sg_id`, `subnet_ids`, `user_data_ai_server_setup`, `ebs_volume_size_gb` (for models), `tags`. (Ensure `instance_type` list includes options with 16GB+ VRAM).
        *   **`outputs.tf`**: `ai_server_instance_ids_ips`.

### 4.3. Environment-Specific Terraform Configurations
   Located in `terraform/environments/`. Each environment (`dev`, `staging`, `production`) will have:

   *   **`main.tf`**:
        *   **Purpose**: Root configuration for the environment, orchestrating module calls.
        *   **Content**:
            *   `terraform` block with remote state backend configuration (e.g., S3 bucket specific to environment).
            *   `provider` block (can inherit from common or specify overrides).
            *   `module` blocks for `vpc`, `security_groups`, `rds_postgres`, `odoo_app`, `n8n_app`, `ai_server`, passing environment-specific variables sourced from its `.tfvars` file and outputs from other modules.
        *   **REQ-DDSI-008, REQ-DI-TENV-001, REQ-DI-CM-001, REQ-DI-AISERV-001, REQ-DI-CM-002** are primarily implemented here by instantiating and parameterizing the modules.

   *   **`variables.tf`** (optional, if root-level variables specific to an environment structure are needed, otherwise variables are defined in modules and common).

   *   **`outputs.tf`** (optional, to output key information like load balancer DNS, application URLs for the specific environment).

   *   **`<env_name>.tfvars`** (e.g., `dev.tfvars`, `staging.tfvars`, `production.tfvars`):
        *   **Purpose**: Provides specific values for variables for that environment.
        *   **Content**: Assignments for variables defined in modules.
            *   `dev.tfvars`: Smaller instance sizes, lower replica counts, dev-specific tags, dev DB credentials (secrets ARNs).
            *   `staging.tfvars`: Aims for production parity in instance types and software versions, potentially smaller scale. Test DB credentials (secrets ARNs). (REQ-DI-CM-002)
            *   `production.tfvars`: Production-grade instance sizes, HA configurations, higher replica counts, production DB credentials (secrets ARNs). (REQ-DI-CM-002 implies it's the reference for staging).

## 5. Ansible Configuration Management

Ansible will be used to configure the software on the infrastructure provisioned by Terraform.

### 5.1. Ansible Core Configuration

   *   **`ansible/ansible.cfg`**:
        *   **Purpose**: Global Ansible settings.
        *   **Content**: `inventory` path (e.g., `inventories/`), `roles_path` (e.g., `roles/`), `remote_user`, `private_key_file` (path, often managed by SSH agent or environment), `host_key_checking = False` (for initial dev/test, stricter in prod), `deprecation_warnings = False`. Privilege escalation settings (`become`, `become_method`, `become_user`).

### 5.2. Ansible Inventories
   Located in `ansible/inventories/`.

   *   **`<env_name>/hosts.ini`** (e.g., `dev/hosts.ini`, `staging/hosts.ini`, `production/hosts.ini`):
        *   **Purpose**: Defines target hosts for Ansible playbooks.
        *   **Content**:
            *   Static entries or, preferably, configured to use a dynamic inventory script/plugin (e.g., `ansible.builtin.terraform` or a custom script) that reads from Terraform state outputs to get host IPs/DNS names.
            *   Host groups: `[odoo_servers]`, `[n8n_servers]`, `[ai_servers]`, `[db_servers]` (if not fully managed RDS and needs OS config).
            *   Variables specific to hosts or groups can be defined here or in corresponding `group_vars`/`host_vars`.

### 5.3. Ansible Roles
   Located in `ansible/roles/`. Each role will have `tasks/main.yml`, `templates/` (if needed), `handlers/main.yml` (if needed), `vars/main.yml` (default vars), `defaults/main.yml`.

   *   **Role: `common`**
        *   **Path**: `ansible/roles/common/`
        *   **Purpose**: Base OS configuration for all servers.
        *   **`tasks/main.yml`**: Update package cache, install common utilities (htop, curl, wget, git, python3-pip), set timezone, configure NTP, create common users/groups, basic security hardening (e.g., disable password auth if using keys, setup basic firewall rules if not fully managed by SGs).

   *   **Role: `docker`**
        *   **Path**: `ansible/roles/docker/`
        *   **Purpose**: Installs Docker Engine and Docker Compose.
        *   **`tasks/main.yml`**: Add Docker GPG key and repository, install `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-compose-plugin`. Start and enable Docker service. Add `ansible_user` to `docker` group.

   *   **Role: `odoo_setup`**
        *   **Path**: `ansible/roles/odoo_setup/`
        *   **Purpose**: Installs and configures Odoo 18 and InfluenceGen custom modules.
        *   **`tasks/main.yml`**:
            *   Install Odoo system dependencies (Python libs, PostgreSQL client, wkhtmltopdf, Node.js, npm, less).
            *   Create Odoo system user.
            *   Clone Odoo 18 source from Git (specific branch/tag) or install from package.
            *   Install Python dependencies for Odoo (`requirements.txt`).
            *   Create Odoo log and data directories.
            *   Deploy `odoo.conf` from template (`odoo.conf.j2`).
            *   Clone/copy InfluenceGen custom modules to addons path.
            *   Initialize Odoo database (if not done manually or by Odoo itself on first run with new DB).
            *   Set up Odoo as a systemd service and ensure it starts.
        *   **`templates/odoo.conf.j2`**:
            *   Parameters: `admin_passwd = {{ odoo_admin_passwd_var }}`, `db_host = {{ odoo_db_host_var }}`, `db_port = {{ odoo_db_port_var }}`, `db_user = {{ odoo_db_user_var }}`, `db_password = {{ odoo_db_password_var }}`, `addons_path`, `logfile`, `limit_time_cpu`, `limit_time_real`, `proxy_mode = True` (if behind a reverse proxy), `csv_internal_sep`. Securely sourced sensitive variables (e.g., from Ansible Vault or environment).
        *   **`vars/main.yml`**: Define default paths, Odoo version, etc.

   *   **Role: `n8n_setup`**
        *   **Path**: `ansible/roles/n8n_setup/`
        *   **Purpose**: Deploys and configures N8N.
        *   **`tasks/main.yml`**:
            *   Ensure 'docker' role is a dependency or tasks are included.
            *   Create N8N data directory.
            *   Deploy `docker-compose.yml` for N8N (from template or file).
                *   Image: `n8nio/n8n` (latest stable or specific version).
                *   Environment variables: `DB_TYPE={{ n8n_db_type_var }}`, `DB_POSTGRESDB_HOST={{ n8n_db_host_var }}`, `DB_POSTGRESDB_DATABASE={{ n8n_db_name_var }}`, `DB_POSTGRESDB_USER={{ n8n_db_user_var }}`, `DB_POSTGRESDB_PASSWORD={{ n8n_db_password_var }}`, `N8N_ENCRYPTION_KEY={{ n8n_encryption_key_var }}`, `WEBHOOK_URL` (N8N's public URL), Odoo callback URLs, other necessary N8N settings. Variables for secrets should be sourced securely.
            *   Use `community.docker.docker_compose` module to start N8N services.

   *   **Role: `ai_server_setup`**
        *   **Path**: `ansible/roles/ai_server_setup/`
        *   **Purpose**: Sets up AI model serving environment. (REQ-DI-AISERV-001)
        *   **`tasks/main.yml`**:
            *   Install NVIDIA drivers, CUDA toolkit.
            *   Ensure 'docker' role is a dependency (if serving models via Docker).
            *   Install Python, pip, and specific ML libraries (PyTorch, diffusers, transformers, accelerate).
            *   Clone/copy AI model serving application code (e.g., FastAPI app) or pull pre-built Docker image (defined in `docker/ai_model_server/Dockerfile`).
            *   Configure the serving application: model paths (potentially on a separate EBS volume provisioned by Terraform), API keys (if any for internal use), listening port.
            *   If using Docker, deploy `docker-compose.yml` or run `docker run` command for the AI server image.
            *   Set up as a systemd service for non-containerized deployment.
        *   **Note**: Ensure VRAM requirements (16GB+, preferably 24GB+) are met by Terraform-provisioned instances. Ansible role focuses on software.

### 5.4. Ansible Playbooks
   Located in `ansible/playbooks/`.

   *   **`site.yml`**:
        *   **Purpose**: Master playbook orchestrating configuration for the entire environment.
        *   **Content**:
            yaml
            ---
            - name: Apply common configuration to all hosts
              hosts: all
              roles:
                - common

            - name: Setup Docker on applicable hosts
              hosts: n8n_servers:ai_servers # Or specific groups requiring Docker
              roles:
                - docker

            - name: Setup Odoo Application Servers
              hosts: odoo_servers
              roles:
                - odoo_setup

            - name: Setup N8N Servers
              hosts: n8n_servers
              roles:
                - n8n_setup

            - name: Setup AI Model Serving Servers
              hosts: ai_servers
              roles:
                - ai_server_setup
            
   *   Other playbooks for specific tasks can be created if needed (e.g., `update_odoo_modules.yml`).

### 5.5. Ansible Group Variables
   Located in `ansible/group_vars/`.

   *   **`all/main.yml`**:
        *   **Purpose**: Defines variables applicable to all hosts.
        *   **Content**: Common paths, default Python version, `ansible_user`, etc.

   *   **`<env_name>.yml`** (e.g., `dev.yml`, `staging.yml`, `production.yml`):
        *   **Purpose**: Defines environment-specific variables. These files are typically named after groups defined in the inventory, or a common group like `all` and then environment-specific inventory files select which hosts belong to which environment. Alternatively, pass extra vars to playbook runs.
        *   **Content**:
            *   `odoo_db_host_var`, `odoo_db_user_var`, `odoo_db_password_var` (using Ansible Vault for sensitive data), `odoo_admin_passwd_var`.
            *   `n8n_db_type_var`, `n8n_db_host_var`, `n8n_db_name_var`, etc.
            *   Environment-specific URLs, API keys (vaulted).
            *   Paths to specific versions of software or custom modules if they differ by environment.
        *   **REQ-DI-CM-001, REQ-DI-CM-002** are supported by this structure.

## 6. Docker Image Definitions

Located in `docker/`.

### 6.1. Odoo Dockerfile
   *   **Path**: `docker/odoo/Dockerfile`
   *   **Purpose**: Builds a custom Odoo 18 image with InfluenceGen modules.
   *   **Content**:
        dockerfile
        ARG ODOO_VERSION=18.0
        FROM odoo:${ODOO_VERSION}

        USER root # Temporarily switch to root for installations

        # Install system dependencies for Odoo and custom modules if any
        # RUN apt-get update && apt-get install -y --no-install-recommends \
        #     package1 package2 \
        #     && rm -rf /var/lib/apt/lists/*

        USER odoo

        # Copy custom InfluenceGen addons
        COPY ./influence_gen_addons/ /mnt/extra-addons/influence_gen_addons/
        # Add other custom addons if they are part of this build context

        # Ensure odoo.conf is picked up or specific env vars are set for addons path
        # ENV ODOO_RC=/etc/odoo/odoo.conf (if odoo.conf is part of the image)
        # Or ensure entrypoint script correctly sets --addons-path

        # Optional: Install Python dependencies for custom modules
        # COPY ./influence_gen_addons/requirements.txt /tmp/requirements.txt
        # RUN pip install --no-cache-dir -r /tmp/requirements.txt
        
   *   **Note**: Actual custom modules are typically mounted as volumes in a Docker Compose setup managed by Ansible, rather than being baked into the image, to allow easier updates. If baking in, ensure paths are correct. The Ansible `odoo_setup` role might handle this layer if not using Docker for Odoo. If Odoo is run directly on EC2, this Dockerfile might be for an alternative deployment strategy or for dev/test. The current Ansible roles suggest Odoo is installed directly on EC2s. This Dockerfile provides an *alternative* or *component* for such.

### 6.2. AI Model Server Dockerfile
   *   **Path**: `docker/ai_model_server/Dockerfile`
   *   **Purpose**: Builds the AI Model Serving application with Flux LoRA support. (REQ-DI-AISERV-001)
   *   **Content**:
        dockerfile
        ARG CUDA_VERSION=12.1.0 # Example, choose based on driver and PyTorch compatibility
        ARG CUDNN_VERSION=8
        ARG UBUNTU_VERSION=22.04
        FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-devel-ubuntu${UBUNTU_VERSION}

        ENV DEBIAN_FRONTEND=noninteractive
        RUN apt-get update && apt-get install -y --no-install-recommends \
            python3-pip \
            git \
            curl \
            # Other dependencies for the AI serving app
            && rm -rf /var/lib/apt/lists/*

        RUN pip3 install --no-cache-dir \
            torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
            # Choose PyTorch version compatible with CUDA version
            diffusers transformers accelerate fastapi uvicorn[standard] \
            # Other Python libraries for Flux LoRA and serving app

        WORKDIR /app

        COPY ./ai_app_code/ /app/ # Copy model serving application code
        # COPY ./models/ /app/models/ # Or use a volume for models
        # Or include script to download models on startup / first run

        EXPOSE 8000 # Or whatever port the serving app uses

        # CMD ["python3", "main.py"] or ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        CMD ["sh", "-c", "echo 'AI Server Starting...' && uvicorn main:app --host 0.0.0.0 --port 8000"]
        
   *   **Note**: Model files themselves are usually large and are better mounted as volumes or downloaded at runtime into a persistent volume, rather than being baked into the image, especially for development iterations.

## 7. Orchestration Scripts

Located in `scripts/`.

### 7.1. `deploy_environment.sh`
   *   **Purpose**: Automates full environment provisioning (Terraform) and configuration (Ansible). (REQ-DDSI-008)
   *   **Logic**:
        1.  Accept environment name (`dev`, `staging`, `prod`) as an argument. Validate input.
        2.  Navigate to `terraform/environments/${ENV_NAME}/`.
        3.  Run `terraform init -upgrade`.
        4.  Run `terraform validate`.
        5.  Run `terraform plan -out=${ENV_NAME}.tfplan -var-file=${ENV_NAME}.tfvars`. (Store plan for review).
        6.  (Optional: Add approval step here for production).
        7.  Run `terraform apply -auto-approve ${ENV_NAME}.tfplan`.
        8.  Extract necessary outputs from Terraform (e.g., IPs of servers) using `terraform output -json`.
        9.  Generate or update Ansible inventory file `ansible/inventories/${ENV_NAME}/hosts.ini` using the Terraform outputs.
        10. Navigate to `ansible/`.
        11. Run `ansible-playbook -i inventories/${ENV_NAME}/hosts.ini playbooks/site.yml --extra-vars "env_name=${ENV_NAME}"` (pass relevant environment variables, especially for vault password if not using agent).
        12. Error handling and logging throughout the script.

### 7.2. `destroy_environment.sh`
   *   **Purpose**: Automates the destruction of an environment's infrastructure. (REQ-DDSI-008)
   *   **Logic**:
        1.  Accept environment name (`dev`, `staging`, `prod`) as an argument. Validate input.
        2.  (Crucial: Add confirmation prompt, especially for `prod`).
        3.  Navigate to `terraform/environments/${ENV_NAME}/`.
        4.  Run `terraform destroy -auto-approve -var-file=${ENV_NAME}.tfvars`.
        5.  Error handling and logging.

## 8. Secrets Management

*   **Terraform**: Database master passwords for RDS and other sensitive variables should be sourced from a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault). Terraform configurations will reference these secrets by ARN or path.
*   **Ansible**: Sensitive data like API keys, database passwords for application configuration (`odoo.conf`, N8N env vars) should be encrypted using Ansible Vault. Vault passwords should be provided securely to Ansible during playbook execution (e.g., via environment variable, CI/CD secret, or prompt).
*   No secrets will be hardcoded in any scripts or configuration files committed to version control.

## 9. Data Residency
*   Terraform configurations, particularly the `aws_region` variable in `providers.tf` and environment-specific `.tfvars` files, will allow specifying the deployment region.
*   If multiple regions are required for data residency for different parts of the data or for DR, the Terraform structure would need to be extended to support multi-region deployments, potentially with separate state files or workspaces per region. This SDS assumes a primary deployment region per environment for now.

## 10. Testing and Validation

*   **Terraform**:
    *   `terraform validate` for syntax and basic consistency.
    *   `terraform plan` for reviewing changes before application.
    *   Manual inspection of provisioned resources in the cloud console post-apply.
*   **Ansible**:
    *   `ansible-lint` for playbook and role quality.
    *   Dry-runs (`--check` mode) before applying configurations.
    *   Manual verification of server configurations and application deployment status.
*   **Scripts**: Manual testing in non-production environments.
*   **Overall**: End-to-end deployment tests for each environment to ensure all components are provisioned and configured correctly and are operational. (REQ-DI-CM-001, REQ-DI-TENV-001)

This SDS provides a comprehensive plan for the IaC repository, enabling the automated and consistent setup of the InfluenceGen platform's infrastructure across different environments.