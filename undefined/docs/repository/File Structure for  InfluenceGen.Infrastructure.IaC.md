# Specification

# 1. Files

- **Path:** terraform/environments/common/providers.tf  
**Description:** Defines common Terraform provider configurations (e.g., AWS, Azure, GCP) and required versions. Used by all environments.  
**Template:** Terraform Configuration  
**Dependancy Level:** 0  
**Name:** providers  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/common  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized provider configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To declare and configure Terraform providers used across all environments.  
**Logic Description:** Contains provider blocks specifying source and version. For example, an AWS provider block with region configuration read from variables.  
**Documentation:**
    
    - **Summary:** Central Terraform provider definitions.
    
**Namespace:** terraform.environments.common  
**Metadata:**
    
    - **Category:** InfrastructureProvisioning
    
- **Path:** terraform/environments/common/variables.tf  
**Description:** Defines common Terraform variables used across different environments, such as default tags, AMI IDs if shared, or global naming conventions. These can be overridden by environment-specific variables.  
**Template:** Terraform Variables  
**Dependancy Level:** 0  
**Name:** variables  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/common  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared variable definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-CM-001
    
**Purpose:** To declare common input variables for Terraform configurations, promoting consistency.  
**Logic Description:** Contains `variable` blocks with descriptions, types, and optional default values for shared infrastructure parameters.  
**Documentation:**
    
    - **Summary:** Common Terraform input variable declarations.
    
**Namespace:** terraform.environments.common  
**Metadata:**
    
    - **Category:** InfrastructureProvisioning
    
- **Path:** terraform/modules/vpc/main.tf  
**Description:** Terraform module for creating a Virtual Private Cloud (VPC), public and private subnets, Internet Gateway, NAT Gateways, and route tables. This module is reusable across environments.  
**Template:** Terraform Module  
**Dependancy Level:** 1  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/vpc  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - VPC creation
    - Subnet provisioning
    - Network routing
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To define a standardized and reusable network foundation (VPC).  
**Logic Description:** Uses resources like `aws_vpc`, `aws_subnet`, `aws_internet_gateway`, `aws_nat_gateway`, `aws_route_table`. Accepts variables for CIDR blocks, availability zones, and naming.  
**Documentation:**
    
    - **Summary:** Provisions core network infrastructure including VPC and subnets.
    
**Namespace:** terraform.modules.vpc  
**Metadata:**
    
    - **Category:** NetworkProvisioning
    
- **Path:** terraform/modules/vpc/variables.tf  
**Description:** Input variables for the VPC Terraform module (e.g., vpc_cidr, public_subnet_cidrs, private_subnet_cidrs, availability_zones, environment_name).  
**Template:** Terraform Variables  
**Dependancy Level:** 0  
**Name:** variables  
**Type:** IaC Module  
**Relative Path:** terraform/modules/vpc  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - VPC parameterization
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To define configurable inputs for the VPC module.  
**Logic Description:** Contains `variable` blocks for all configurable aspects of the VPC module, allowing customization per environment.  
**Documentation:**
    
    - **Summary:** Input variables for the VPC Terraform module.
    
**Namespace:** terraform.modules.vpc  
**Metadata:**
    
    - **Category:** NetworkProvisioning
    
- **Path:** terraform/modules/vpc/outputs.tf  
**Description:** Output values from the VPC Terraform module (e.g., vpc_id, public_subnet_ids, private_subnet_ids).  
**Template:** Terraform Outputs  
**Dependancy Level:** 0  
**Name:** outputs  
**Type:** IaC Module  
**Relative Path:** terraform/modules/vpc  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Exposing VPC resource IDs
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To export created VPC resource identifiers for use by other modules.  
**Logic Description:** Contains `output` blocks declaring values to be exported from this module after its resources are created.  
**Documentation:**
    
    - **Summary:** Outputs from the VPC Terraform module.
    
**Namespace:** terraform.modules.vpc  
**Metadata:**
    
    - **Category:** NetworkProvisioning
    
- **Path:** terraform/modules/security_groups/main.tf  
**Description:** Terraform module for defining various security groups needed by the application components (e.g., for Odoo web, Odoo app, N8N, AI server, PostgreSQL database).  
**Template:** Terraform Module  
**Dependancy Level:** 1  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/security_groups  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Network access control configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To define and manage firewall rules for different service tiers.  
**Logic Description:** Uses `aws_security_group` and `aws_security_group_rule` resources. Accepts variables for VPC ID and ingress/egress rules based on ports and source/destination CIDRs or security group IDs.  
**Documentation:**
    
    - **Summary:** Provisions security groups with specified ingress/egress rules.
    
**Namespace:** terraform.modules.security_groups  
**Metadata:**
    
    - **Category:** NetworkProvisioning
    
- **Path:** terraform/modules/security_groups/variables.tf  
**Description:** Input variables for the Security Groups module (e.g., vpc_id, rule definitions).  
**Template:** Terraform Variables  
**Dependancy Level:** 0  
**Name:** variables  
**Type:** IaC Module  
**Relative Path:** terraform/modules/security_groups  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Security group parameterization
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To define configurable inputs for the security groups module.  
**Logic Description:** Contains `variable` blocks for VPC ID and a complex type for defining lists of security group rules (protocol, ports, cidr_blocks, source_security_group_id).  
**Documentation:**
    
    - **Summary:** Input variables for the Security Groups Terraform module.
    
**Namespace:** terraform.modules.security_groups  
**Metadata:**
    
    - **Category:** NetworkProvisioning
    
- **Path:** terraform/modules/rds_postgres/main.tf  
**Description:** Terraform module for provisioning an AWS RDS PostgreSQL instance. Includes parameters for instance class, storage, version, security groups, and subnet group.  
**Template:** Terraform Module  
**Dependancy Level:** 1  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/rds_postgres  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Managed PostgreSQL database provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To provide a managed relational database service for Odoo.  
**Logic Description:** Uses `aws_db_instance` or `aws_rds_cluster` resources, `aws_db_subnet_group`. Accepts variables for database credentials (to be sourced from a secrets manager), instance size, storage, PostgreSQL version, etc.  
**Documentation:**
    
    - **Summary:** Provisions an AWS RDS PostgreSQL database instance.
    
**Namespace:** terraform.modules.rds_postgres  
**Metadata:**
    
    - **Category:** DatabaseProvisioning
    
- **Path:** terraform/modules/ec2_instance/main.tf  
**Description:** Generic Terraform module for provisioning EC2 instances. Parameters include AMI ID, instance type, key pair, security groups, subnets, user data for bootstrapping.  
**Template:** Terraform Module  
**Dependancy Level:** 1  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/ec2_instance  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Virtual server provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To provide a reusable component for creating EC2 instances.  
**Logic Description:** Uses `aws_instance` resource. Accepts variables for AMI, instance type, key name, security group IDs, subnet ID, EBS volume configuration, and user data scripts.  
**Documentation:**
    
    - **Summary:** Provisions generic EC2 instances.
    
**Namespace:** terraform.modules.ec2_instance  
**Metadata:**
    
    - **Category:** ComputeProvisioning
    
- **Path:** terraform/modules/odoo_app/main.tf  
**Description:** Terraform module to provision infrastructure for Odoo application servers. This might involve EC2 instances, load balancers, and auto-scaling groups. Depends on VPC and RDS modules.  
**Template:** Terraform Module  
**Dependancy Level:** 2  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/odoo_app  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo application server infrastructure provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To set up the specific infrastructure required to host the Odoo application.  
**Logic Description:** Instantiates `ec2_instance` module for Odoo servers. May include `aws_lb`, `aws_lb_target_group`, `aws_autoscaling_group`. Configures security groups specific to Odoo. Links to RDS instance output.  
**Documentation:**
    
    - **Summary:** Provisions Odoo application server infrastructure.
    
**Namespace:** terraform.modules.odoo_app  
**Metadata:**
    
    - **Category:** ApplicationInfrastructure
    
- **Path:** terraform/modules/n8n_app/main.tf  
**Description:** Terraform module to provision infrastructure for N8N. Typically involves EC2 instances or container services. Depends on VPC module.  
**Template:** Terraform Module  
**Dependancy Level:** 2  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/n8n_app  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N server infrastructure provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To set up the infrastructure for the N8N workflow automation engine.  
**Logic Description:** Instantiates `ec2_instance` module for N8N server or uses container service resources like `aws_ecs_service`. Configures security groups for N8N.  
**Documentation:**
    
    - **Summary:** Provisions N8N server infrastructure.
    
**Namespace:** terraform.modules.n8n_app  
**Metadata:**
    
    - **Category:** ApplicationInfrastructure
    
- **Path:** terraform/modules/ai_server/main.tf  
**Description:** Terraform module for provisioning AI Model Serving Infrastructure. Specifically provisions GPU-enabled EC2 instances suitable for Flux LoRA models. Depends on VPC module.  
**Template:** Terraform Module  
**Dependancy Level:** 2  
**Name:** main  
**Type:** IaC Module  
**Relative Path:** terraform/modules/ai_server  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI model serving infrastructure with GPU support
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-AISERV-001
    - REQ-DI-TENV-001
    
**Purpose:** To provision compute resources with GPUs for AI model inference.  
**Logic Description:** Instantiates `ec2_instance` module, specifying GPU instance types (e.g., g4dn, p3). Configures appropriate security groups and potentially EBS volumes for model storage. User data script may initiate basic setup.  
**Documentation:**
    
    - **Summary:** Provisions GPU-enabled EC2 instances for AI model serving.
    
**Namespace:** terraform.modules.ai_server  
**Metadata:**
    
    - **Category:** AIInfrastructure
    
- **Path:** terraform/environments/dev/main.tf  
**Description:** Main Terraform configuration for the Development environment. Instantiates various modules (VPC, RDS, Odoo App, N8N App, AI Server) using development-specific variables.  
**Template:** Terraform Configuration  
**Dependancy Level:** 3  
**Name:** main-dev  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/dev  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - EnvironmentConfiguration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development environment provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-AISERV-001
    
**Purpose:** To define and orchestrate the creation of all infrastructure for the development environment.  
**Logic Description:** Contains `module` blocks calling shared modules like `vpc`, `rds_postgres`, `odoo_app`, `n8n_app`, `ai_server`. Passes variables from `dev.tfvars` to these modules. Defines backend configuration via `backend.tf`.  
**Documentation:**
    
    - **Summary:** Root Terraform configuration for the development environment.
    
**Namespace:** terraform.environments.dev  
**Metadata:**
    
    - **Category:** EnvironmentOrchestration
    
- **Path:** terraform/environments/dev/dev.tfvars  
**Description:** Terraform variable definitions specific to the Development environment (e.g., instance sizes, replica counts, specific CIDR ranges, dev-specific tags).  
**Template:** Terraform Variables File  
**Dependancy Level:** 2  
**Name:** dev.tfvars  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/dev  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development environment specific parameters
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    
**Purpose:** To provide environment-specific values for Terraform configurations.  
**Logic Description:** Contains assignments for variables defined in module `variables.tf` files or root `variables.tf`, tailored for the development environment.  
**Documentation:**
    
    - **Summary:** Variable values for the development Terraform environment.
    
**Namespace:** terraform.environments.dev  
**Metadata:**
    
    - **Category:** EnvironmentConfiguration
    
- **Path:** terraform/environments/staging/main.tf  
**Description:** Main Terraform configuration for the Staging/UAT environment. Instantiates modules ensuring parity with production where possible.  
**Template:** Terraform Configuration  
**Dependancy Level:** 3  
**Name:** main-staging  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/staging  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - EnvironmentConfiguration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging environment provisioning
    - Environment parity with production
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-AISERV-001
    - REQ-DI-CM-002
    
**Purpose:** To define and orchestrate the creation of all infrastructure for the staging environment.  
**Logic Description:** Similar to dev/main.tf, but uses `staging.tfvars`. Configurations aim for production parity in terms of software versions and infrastructure types, potentially differing in scale.  
**Documentation:**
    
    - **Summary:** Root Terraform configuration for the staging environment.
    
**Namespace:** terraform.environments.staging  
**Metadata:**
    
    - **Category:** EnvironmentOrchestration
    
- **Path:** terraform/environments/staging/staging.tfvars  
**Description:** Terraform variable definitions specific to the Staging/UAT environment.  
**Template:** Terraform Variables File  
**Dependancy Level:** 2  
**Name:** staging.tfvars  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/staging  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging environment specific parameters
    - Environment parity configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-CM-002
    
**Purpose:** To provide environment-specific values for Staging Terraform configurations, aiming for production parity.  
**Logic Description:** Contains assignments tailored for staging, ensuring infrastructure, software versions match production where feasible.  
**Documentation:**
    
    - **Summary:** Variable values for the staging Terraform environment.
    
**Namespace:** terraform.environments.staging  
**Metadata:**
    
    - **Category:** EnvironmentConfiguration
    
- **Path:** terraform/environments/production/main.tf  
**Description:** Main Terraform configuration for the Production environment. Instantiates modules with production-grade settings.  
**Template:** Terraform Configuration  
**Dependancy Level:** 3  
**Name:** main-production  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/production  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - EnvironmentConfiguration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Production environment provisioning
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-AISERV-001
    - REQ-DI-CM-002
    
**Purpose:** To define and orchestrate the creation of all infrastructure for the production environment.  
**Logic Description:** Similar to dev/main.tf and staging/main.tf, but uses `production.tfvars` with production-level scaling, resilience, and security configurations.  
**Documentation:**
    
    - **Summary:** Root Terraform configuration for the production environment.
    
**Namespace:** terraform.environments.production  
**Metadata:**
    
    - **Category:** EnvironmentOrchestration
    
- **Path:** terraform/environments/production/production.tfvars  
**Description:** Terraform variable definitions specific to the Production environment (e.g., larger instance sizes, higher replica counts, production endpoints, stricter security).  
**Template:** Terraform Variables File  
**Dependancy Level:** 2  
**Name:** production.tfvars  
**Type:** IaC Configuration  
**Relative Path:** terraform/environments/production  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Production environment specific parameters
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-CM-002
    
**Purpose:** To provide environment-specific values for Production Terraform configurations.  
**Logic Description:** Contains assignments tailored for production, focusing on performance, reliability, and security.  
**Documentation:**
    
    - **Summary:** Variable values for the production Terraform environment.
    
**Namespace:** terraform.environments.production  
**Metadata:**
    
    - **Category:** EnvironmentConfiguration
    
- **Path:** ansible/ansible.cfg  
**Description:** Ansible configuration file. Defines default settings like inventory path, remote user, private key file, roles path, and plugin configurations.  
**Template:** Ansible Configuration  
**Dependancy Level:** 0  
**Name:** ansible.cfg  
**Type:** IaC Configuration  
**Relative Path:** ansible  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Ansible runtime behavior configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To configure Ansible's execution environment and default behaviors.  
**Logic Description:** Contains sections like `[defaults]` to set `inventory`, `roles_path`, `remote_user`, `private_key_file`, `host_key_checking`, etc. May include `[privilege_escalation]` settings.  
**Documentation:**
    
    - **Summary:** Global Ansible configuration settings.
    
**Namespace:** ansible  
**Metadata:**
    
    - **Category:** ConfigurationManagementTool
    
- **Path:** ansible/inventories/dev/hosts.ini  
**Description:** Ansible inventory file for the Development environment. Lists hosts or groups of hosts managed by Ansible. Can be static or point to a dynamic inventory script using Terraform outputs.  
**Template:** Ansible Inventory  
**Dependancy Level:** 3  
**Name:** hosts-dev.ini  
**Type:** IaC Configuration  
**Relative Path:** ansible/inventories/dev  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development environment host definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    
**Purpose:** To define the target hosts for Ansible playbooks in the development environment.  
**Logic Description:** Contains host entries and group definitions. For example, `[odoo_servers_dev] odoo_server_1_dev ansible_host=IP_OR_DNS`. Could use `ansible.builtin.terraform` inventory plugin or custom script to parse Terraform state/outputs.  
**Documentation:**
    
    - **Summary:** Ansible inventory for the development environment.
    
**Namespace:** ansible.inventories.dev  
**Metadata:**
    
    - **Category:** ConfigurationManagementTool
    
- **Path:** ansible/inventories/staging/hosts.ini  
**Description:** Ansible inventory file for the Staging/UAT environment.  
**Template:** Ansible Inventory  
**Dependancy Level:** 3  
**Name:** hosts-staging.ini  
**Type:** IaC Configuration  
**Relative Path:** ansible/inventories/staging  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging environment host definitions
    - Environment parity configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-CM-002
    
**Purpose:** To define the target hosts for Ansible playbooks in the staging environment.  
**Logic Description:** Similar to dev inventory, but for staging hosts. Values sourced from staging Terraform outputs.  
**Documentation:**
    
    - **Summary:** Ansible inventory for the staging environment.
    
**Namespace:** ansible.inventories.staging  
**Metadata:**
    
    - **Category:** ConfigurationManagementTool
    
- **Path:** ansible/inventories/production/hosts.ini  
**Description:** Ansible inventory file for the Production environment.  
**Template:** Ansible Inventory  
**Dependancy Level:** 3  
**Name:** hosts-production.ini  
**Type:** IaC Configuration  
**Relative Path:** ansible/inventories/production  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Production environment host definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-001
    - REQ-DI-CM-002
    
**Purpose:** To define the target hosts for Ansible playbooks in the production environment.  
**Logic Description:** Similar to dev inventory, but for production hosts. Values sourced from production Terraform outputs. Access to this should be tightly controlled.  
**Documentation:**
    
    - **Summary:** Ansible inventory for the production environment.
    
**Namespace:** ansible.inventories.production  
**Metadata:**
    
    - **Category:** ConfigurationManagementTool
    
- **Path:** ansible/roles/common/tasks/main.yml  
**Description:** Main task file for the 'common' Ansible role. Includes tasks for base OS configuration applicable to all servers, like setting timezone, installing common packages (e.g., curl, wget, python), user creation, and basic security hardening.  
**Template:** Ansible Role Task File  
**Dependancy Level:** 1  
**Name:** main-common-tasks  
**Type:** IaC Role  
**Relative Path:** ansible/roles/common/tasks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base OS configuration
    - Common package installation
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To apply consistent baseline configurations to all managed servers.  
**Logic Description:** Uses Ansible modules like `ansible.builtin.package`, `ansible.builtin.user`, `ansible.builtin.timezone`, `ansible.builtin.lineinfile` for common system setup tasks.  
**Documentation:**
    
    - **Summary:** Tasks for common server setup.
    
**Namespace:** ansible.roles.common  
**Metadata:**
    
    - **Category:** ConfigurationManagement
    
- **Path:** ansible/roles/docker/tasks/main.yml  
**Description:** Main task file for the 'docker' Ansible role. Installs and configures Docker Engine and Docker Compose on target hosts.  
**Template:** Ansible Role Task File  
**Dependancy Level:** 1  
**Name:** main-docker-tasks  
**Type:** IaC Role  
**Relative Path:** ansible/roles/docker/tasks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Docker installation
    - Docker Compose installation
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To ensure Docker is available on hosts that require it (e.g., N8N, AI server).  
**Logic Description:** Uses Ansible modules to add Docker repository, install Docker packages (`docker-ce`, `docker-ce-cli`, `containerd.io`), start and enable Docker service, and install Docker Compose.  
**Documentation:**
    
    - **Summary:** Tasks for installing Docker and Docker Compose.
    
**Namespace:** ansible.roles.docker  
**Metadata:**
    
    - **Category:** ConfigurationManagement
    
- **Path:** ansible/roles/odoo_setup/tasks/main.yml  
**Description:** Main task file for the 'odoo_setup' Ansible role. Handles Odoo 18 installation, dependencies, database setup (if not fully handled by RDS), configuration of odoo.conf, and deployment of InfluenceGen custom modules.  
**Template:** Ansible Role Task File  
**Dependancy Level:** 2  
**Name:** main-odoo_setup-tasks  
**Type:** IaC Role  
**Relative Path:** ansible/roles/odoo_setup/tasks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    - ApplicationDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo 18 installation
    - Odoo configuration
    - Custom module deployment
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To automate the setup and configuration of Odoo application servers.  
**Logic Description:** Installs Odoo dependencies (Python, PostgreSQL client, wkhtmltopdf, etc.). Clones Odoo source or uses packaged version. Sets up system user for Odoo. Configures `odoo.conf` using a template. Initializes Odoo database. Copies custom InfluenceGen modules to addons path. Starts Odoo service.  
**Documentation:**
    
    - **Summary:** Tasks for installing and configuring Odoo 18.
    
**Namespace:** ansible.roles.odoo_setup  
**Metadata:**
    
    - **Category:** ApplicationDeployment
    
- **Path:** ansible/roles/odoo_setup/templates/odoo.conf.j2  
**Description:** Jinja2 template for the Odoo configuration file (odoo.conf). Allows for environment-specific settings like database connection details, addons path, admin password (sourced securely).  
**Template:** Ansible Template  
**Dependancy Level:** 1  
**Name:** odoo.conf.j2  
**Type:** IaC ConfigurationTemplate  
**Relative Path:** ansible/roles/odoo_setup/templates  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dynamic Odoo configuration generation
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-CM-001
    
**Purpose:** To provide a template for generating the `odoo.conf` file with environment-specific values.  
**Logic Description:** Contains standard `odoo.conf` parameters with Jinja2 variables for dynamic values (e.g., `{{ odoo_db_host }}`, `{{ odoo_db_user }}`, `{{ odoo_admin_passwd }}`).  
**Documentation:**
    
    - **Summary:** Template for Odoo server configuration file.
    
**Namespace:** ansible.roles.odoo_setup  
**Metadata:**
    
    - **Category:** ApplicationConfiguration
    
- **Path:** ansible/roles/n8n_setup/tasks/main.yml  
**Description:** Main task file for the 'n8n_setup' Ansible role. Deploys N8N, typically using Docker Compose. Configures N8N environment variables for database connection, Odoo callback URLs, etc.  
**Template:** Ansible Role Task File  
**Dependancy Level:** 2  
**Name:** main-n8n_setup-tasks  
**Type:** IaC Role  
**Relative Path:** ansible/roles/n8n_setup/tasks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    - ApplicationDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N deployment
    - N8N configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To automate the deployment and configuration of N8N instances.  
**Logic Description:** Ensures Docker and Docker Compose are installed (dependency on 'docker' role). Copies a `docker-compose.yml` file for N8N (or generates it from a template). Sets N8N environment variables using Ansible variables (e.g., for database, encryption key, webhook URLs). Starts N8N services using `docker-compose up`.  
**Documentation:**
    
    - **Summary:** Tasks for deploying and configuring N8N.
    
**Namespace:** ansible.roles.n8n_setup  
**Metadata:**
    
    - **Category:** ApplicationDeployment
    
- **Path:** ansible/roles/ai_server_setup/tasks/main.yml  
**Description:** Main task file for the 'ai_server_setup' Ansible role. Sets up the AI model serving environment on GPU instances. Installs CUDA drivers, Docker, Python, specific ML libraries (PyTorch, Transformers), and deploys/configures the AI model serving application (e.g., ComfyUI, Automatic1111, or custom server using Flux LoRA models).  
**Template:** Ansible Role Task File  
**Dependancy Level:** 2  
**Name:** main-ai_server_setup-tasks  
**Type:** IaC Role  
**Relative Path:** ansible/roles/ai_server_setup/tasks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ModularDesign
    - ApplicationDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI model server setup
    - GPU driver installation
    - Flux LoRA model environment setup
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-AISERV-001
    - REQ-DI-TENV-001
    
**Purpose:** To automate the configuration of GPU-enabled servers for AI model inference.  
**Logic Description:** Installs NVIDIA drivers and CUDA toolkit. Installs Docker (if serving via containers). Installs Python and required ML packages (PyTorch, diffusers, accelerate for Flux). Clones or copies AI serving application code/Docker image. Configures application (model paths, API keys). Starts the AI serving application/service.  
**Documentation:**
    
    - **Summary:** Tasks for setting up AI model serving environment with GPU support.
    
**Namespace:** ansible.roles.ai_server_setup  
**Metadata:**
    
    - **Category:** AIInfrastructure
    
- **Path:** ansible/playbooks/site.yml  
**Description:** Master Ansible playbook that orchestrates the provisioning of the entire infrastructure by calling other component-specific playbooks (e.g., setup_odoo_servers.yml, setup_n8n_servers.yml, setup_ai_servers.yml).  
**Template:** Ansible Playbook  
**Dependancy Level:** 3  
**Name:** site.yml  
**Type:** IaC Orchestration  
**Relative Path:** ansible/playbooks  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - Orchestration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Full environment configuration orchestration
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    
**Purpose:** To provide a single entry point for configuring all servers in an environment.  
**Logic Description:** Contains a list of plays, each targeting specific host groups (e.g., `odoo_servers`, `n8n_servers`, `ai_servers`). Each play imports or includes other playbooks or directly applies roles relevant to that host group.  
**Documentation:**
    
    - **Summary:** Master playbook for Ansible configuration runs.
    
**Namespace:** ansible.playbooks  
**Metadata:**
    
    - **Category:** ConfigurationManagement
    
- **Path:** ansible/group_vars/all/main.yml  
**Description:** Ansible group variables file that applies to all hosts in the inventory. Defines common variables like default SSH user, paths, or globally applicable settings.  
**Template:** Ansible Variables File  
**Dependancy Level:** 1  
**Name:** main-group_vars-all  
**Type:** IaC Configuration  
**Relative Path:** ansible/group_vars/all  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Global variable definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-CM-001
    
**Purpose:** To define variables that are common across all managed hosts.  
**Logic Description:** YAML file containing key-value pairs for variables. For example, `ansible_user: ubuntu`, `python_version: 3.10`.  
**Documentation:**
    
    - **Summary:** Common Ansible variables for all hosts.
    
**Namespace:** ansible.group_vars.all  
**Metadata:**
    
    - **Category:** ConfigurationManagement
    
- **Path:** ansible/group_vars/dev.yml  
**Description:** Ansible group variables specific to the Development environment. Overrides or supplements variables from `all.yml` for hosts in the 'dev' group (if inventories are structured this way) or used when targeting the dev environment playbook.  
**Template:** Ansible Variables File  
**Dependancy Level:** 2  
**Name:** dev-group_vars  
**Type:** IaC Configuration  
**Relative Path:** ansible/group_vars  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development environment specific Ansible variables
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-CM-001
    - REQ-DI-TENV-001
    
**Purpose:** To provide development-specific configurations for Ansible roles and playbooks.  
**Logic Description:** YAML file containing key-value pairs tailored for the dev environment, e.g., `odoo_db_name: influencegen_dev`, `n8n_encryption_key_secret_name: n8n_dev_key`.  
**Documentation:**
    
    - **Summary:** Development environment specific Ansible variables.
    
**Namespace:** ansible.group_vars  
**Metadata:**
    
    - **Category:** ConfigurationManagement
    
- **Path:** docker/odoo/Dockerfile  
**Description:** Dockerfile for building a custom Odoo 18 image. Starts from a base Odoo image or a Python image, installs Odoo dependencies, copies InfluenceGen custom modules, and sets up entrypoint.  
**Template:** Dockerfile  
**Dependancy Level:** 0  
**Name:** Dockerfile-odoo  
**Type:** Containerization Definition  
**Relative Path:** docker/odoo  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Odoo Docker image build
    
**Requirement Ids:**
    
    - REQ-DI-TENV-001
    
**Purpose:** To create a standardized Docker image for deploying Odoo with InfluenceGen modules.  
**Logic Description:** Uses `FROM` instruction for base image. `RUN` instructions to install OS packages and Python dependencies. `COPY` instructions to add Odoo custom modules to the `/mnt/extra-addons` directory. `USER odoo`. `ENTRYPOINT` and/or `CMD` to start Odoo.  
**Documentation:**
    
    - **Summary:** Builds a Docker image for Odoo 18 including custom modules.
    
**Namespace:** docker.odoo  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** docker/ai_model_server/Dockerfile  
**Description:** Dockerfile for building the AI Model Serving application. Starts from a base image with CUDA/Python, installs required ML libraries (PyTorch, diffusers, transformers, accelerate), copies model serving code (e.g., FastAPI app) and Flux LoRA models (or scripts to download them), and sets up the entrypoint to start the server.  
**Template:** Dockerfile  
**Dependancy Level:** 0  
**Name:** Dockerfile-ai_model_server  
**Type:** Containerization Definition  
**Relative Path:** docker/ai_model_server  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Server Docker image build
    - Flux LoRA model serving environment
    
**Requirement Ids:**
    
    - REQ-DI-AISERV-001
    - REQ-DI-TENV-001
    
**Purpose:** To create a containerized environment for serving Flux LoRA models.  
**Logic Description:** Uses `FROM nvidia/cuda:X.Y-cudnnZ-devel-ubuntuA.B` or similar. `RUN` apt/pip installs for Python, PyTorch, diffusers, etc. `COPY` application code, model download scripts, or pre-downloaded models (if small). `EXPOSE` port. `CMD` to start the model serving application (e.g., `uvicorn main:app --host 0.0.0.0`).  
**Documentation:**
    
    - **Summary:** Builds a Docker image for the AI Model Serving application with Flux LoRA support.
    
**Namespace:** docker.ai_model_server  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** scripts/deploy_environment.sh  
**Description:** Shell script to orchestrate the deployment of a specified environment. Takes environment name (dev, staging, prod) as an argument. Runs Terraform to provision infrastructure, then runs Ansible to configure software.  
**Template:** Shell Script  
**Dependancy Level:** 4  
**Name:** deploy_environment  
**Type:** IaC Script  
**Relative Path:** scripts  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - Orchestration
    - Automation
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated environment deployment pipeline
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    - REQ-DI-TENV-001
    - REQ-DI-CM-002
    
**Purpose:** To provide an automated way to provision and configure an entire environment.  
**Logic Description:** Parses environment argument. Changes directory to `terraform/environments/$ENV`. Runs `terraform init` and `terraform apply -var-file=$ENV.tfvars`. Extracts Terraform outputs (e.g., IPs) to generate/update Ansible inventory for `$ENV`. Changes directory to `ansible/`. Runs `ansible-playbook -i inventories/$ENV/hosts.ini playbooks/site.yml`.  
**Documentation:**
    
    - **Summary:** Orchestrates Terraform provisioning and Ansible configuration for a given environment.
    
**Namespace:** scripts  
**Metadata:**
    
    - **Category:** DeploymentScript
    
- **Path:** scripts/destroy_environment.sh  
**Description:** Shell script to destroy the infrastructure of a specified environment. Takes environment name as an argument. Primarily runs `terraform destroy`.  
**Template:** Shell Script  
**Dependancy Level:** 4  
**Name:** destroy_environment  
**Type:** IaC Script  
**Relative Path:** scripts  
**Repository Id:** REPO-IGINF-007  
**Pattern Ids:**
    
    - Orchestration
    - Automation
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated environment teardown
    
**Requirement Ids:**
    
    - REQ-DDSI-008
    
**Purpose:** To provide an automated way to tear down an environment's infrastructure.  
**Logic Description:** Parses environment argument. Changes directory to `terraform/environments/$ENV`. Runs `terraform destroy -var-file=$ENV.tfvars -auto-approve` (with caution for production).  
**Documentation:**
    
    - **Summary:** Automates the destruction of an environment's infrastructure using Terraform.
    
**Namespace:** scripts  
**Metadata:**
    
    - **Category:** DeploymentScript
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - db_host_var_terraform
  - db_port_var_terraform
  - db_name_var_terraform
  - db_user_var_terraform
  - db_password_secret_terraform
  - odoo_db_host_ansible_var
  - odoo_db_port_ansible_var
  - odoo_db_user_ansible_var
  - odoo_db_password_ansible_secret_var
  - n8n_db_type_ansible_var
  - n8n_db_host_ansible_var
  - n8n_db_port_ansible_var
  - n8n_db_name_ansible_var
  - n8n_db_user_ansible_var
  - n8n_db_password_ansible_secret_var
  


---

