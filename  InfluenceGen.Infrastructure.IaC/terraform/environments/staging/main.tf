```hcl
terraform {
  backend "s3" {
    bucket = "influencegen-terraform-state-staging" # Replace with actual bucket name
    key    = "staging/terraform.tfstate"
    region = "us-east-1" # Match your chosen region
    encrypt = true
  }
}

# Include common providers and variables
module "common_vars" {
  source = "../common"
}

provider "aws" {
  region = module.common_vars.aws_region
}

# Get default tags from common variables
locals {
  default_tags = module.common_vars.default_tags
  project_name = module.common_vars.project_name
  environment_name = "staging"
}

# Define environment-specific variables (loaded from staging.tfvars)
variable "vpc_cidr_block" {}
variable "public_subnet_cidrs" {}
variable "private_subnet_cidrs" {}
variable "availability_zones" {}
variable "db_instance_class" {}
variable "db_allocated_storage" {}
variable "db_engine_version" {}
variable "db_name" {}
variable "db_username_secret_arn" {}
variable "db_password_secret_arn" {}
variable "odoo_ami_id" {}
variable "odoo_instance_type" {}
variable "odoo_instance_count" {}
variable "odoo_key_name" {}
variable "odoo_db_user_secret_arn" {}
variable "odoo_db_password_secret_arn" {}
variable "odoo_admin_password_secret_arn" {}
variable "n8n_ami_id" {}
variable "n8n_instance_type" {}
variable "n8n_key_name" {}
variable "n8n_db_type" {}
variable "n8n_db_host" {} # Can be RDS endpoint from output
variable "n8n_db_port" {} # Can be RDS port from output
variable "n8n_db_name" {}
variable "n8n_db_user_secret_arn" {}
variable "n8n_db_password_secret_arn" {}
variable "n8n_encryption_key_secret_arn" {}
variable "ai_ami_id" {}
variable "ai_instance_type" {}
variable "ai_instance_count" {}
variable "ai_key_name" {}
variable "ai_ebs_volume_size_gb" {}

# Provision VPC
module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr_block     = var.vpc_cidr_block
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones = var.availability_zones
  environment_name   = local.environment_name
  project_name       = local.project_name
  default_tags       = local.default_tags
}

# Define Security Group Rules (aim for production parity where possible)
locals {
  security_group_definitions = {
    odoo_web_sg = {
      description = "Allow access to Odoo web interface"
      ingress = [
        { protocol = "tcp", from_port = 80, to_port = 80, cidr_blocks = ["0.0.0.0/0"], source_security_group_id = null, description = "Allow HTTP from internet" },
        { protocol = "tcp", from_port = 443, to_port = 443, cidr_blocks = ["0.0.0.0/0"], source_security_group_id = null, description = "Allow HTTPS from internet" },
        // Add ingress from load balancer SG if used (Staging often uses LB)
      ]
      egress = []
    }
    odoo_internal_sg = {
      description = "Internal Odoo app security group"
      ingress = [
         # Allow Odoo instances to talk to each other if using ASG
         // { protocol = "tcp", from_port = 8069, to_port = 8069, source_security_group_id = module.security_groups.security_group_ids["odoo_internal_sg"], cidr_blocks = null, description = "Allow Odoo internal communication" },
         { protocol = "tcp", from_port = var.db_port, to_port = var.db_port, source_security_group_id = module.security_groups.security_group_ids["db_sg"], cidr_blocks = null, description = "Allow Odoo to DB" },
         { protocol = "tcp", from_port = 8000, to_port = 8000, source_security_group_id = module.security_groups.security_group_ids["ai_server_sg"], cidr_blocks = null, description = "Allow Odoo to AI Server" },
         { protocol = "tcp", from_port = 22, to_port = 22, cidr_blocks = ["YOUR_ADMIN_CIDR_BLOCK"], source_security_group_id = null, description = "Allow SSH access" }, # REPLACE
      ]
      egress = []
    }
    n8n_sg = {
      description = "Security group for N8N"
      ingress = [
        { protocol = "tcp", from_port = 5678, to_port = 5678, cidr_blocks = ["0.0.0.0/0"], source_security_group_id = null, description = "Allow N8N web interface (Adjust CIDR for production)" }, # Less strict for staging/uat is ok, or use stricter LB SG
        { protocol = "tcp", from_port = var.db_port, to_port = var.db_port, source_security_group_id = module.security_groups.security_group_ids["db_sg"], cidr_blocks = null, description = "Allow N8N to DB" },
        { protocol = "tcp", from_port = 22, to_port = 22, cidr_blocks = ["YOUR_ADMIN_CIDR_BLOCK"], source_security_group_id = null, description = "Allow SSH access" }, # REPLACE
      ]
       egress = []
    }
    ai_server_sg = {
      description = "Security group for AI Model Serving"
      ingress = [
        { protocol = "tcp", from_port = 8000, to_port = 8000, source_security_group_id = module.security_groups.security_group_ids["odoo_internal_sg"], cidr_blocks = null, description = "Allow Odoo to AI Server" },
         { protocol = "tcp", from_port = 22, to_port = 22, cidr_blocks = ["YOUR_ADMIN_CIDR_BLOCK"], source_security_group_id = null, description = "Allow SSH access" }, # REPLACE
      ]
       egress = []
    }
    db_sg = {
      description = "Security group for PostgreSQL database"
      ingress = [
        { protocol = "tcp", from_port = var.db_port, to_port = var.db_port, source_security_group_id = module.security_groups.security_group_ids["odoo_internal_sg"], cidr_blocks = null, description = "Allow Odoo to DB" },
        { protocol = "tcp", from_port = var.db_port, to_port = var.db_port, source_security_group_id = module.security_groups.security_group_ids["n8n_sg"], cidr_blocks = null, description = "Allow N8N to DB" },
        // Add ingress from admin machines/bastion host if needed
      ]
      egress = []
    }
  }
}


# Provision Security Groups
module "security_groups" {
  source = "../../modules/security_groups"

  vpc_id = module.vpc.vpc_id
  security_group_definitions = local.security_group_definitions
  environment_name = local.environment_name
  project_name     = local.project_name
  default_tags     = local.default_tags
}

# Provision RDS PostgreSQL (Staging should aim for production config parity)
module "rds_postgres" {
  source = "../../modules/rds_postgres"

  db_name                = var.db_name
  engine_version         = var.db_engine_version
  instance_class         = var.db_instance_class         # Should match Prod class or be close
  allocated_storage      = var.db_allocated_storage      # Should match Prod allocation or be close
  vpc_security_group_ids = [module.security_groups.security_group_ids["db_sg"]]
  subnet_ids             = module.vpc.private_subnet_ids
  username_secret_arn    = var.db_username_secret_arn    # Staging specific secret
  password_secret_arn    = var.db_password_secret_arn    # Staging specific secret
  multi_az               = true                          # Match Prod Multi-AZ
  backup_retention_period = 30                          # Match Prod backup retention

  environment_name   = local.environment_name
  project_name       = local.project_name
  default_tags       = local.default_tags
}

# Provision Odoo Application Servers (Staging should aim for production config parity)
module "odoo_app" {
  source = "../../modules/odoo_app"

  instance_count = var.odoo_instance_count # Maybe fewer instances than Prod, but same type
  ami_id         = var.odoo_ami_id       # Should match Prod AMI
  instance_type  = var.odoo_instance_type # Should match Prod instance type
  key_name       = var.odoo_key_name
  odoo_sg_id     = module.security_groups.security_group_ids["odoo_internal_sg"]
  subnet_ids     = module.vpc.private_subnet_ids
  # user_data_odoo_setup_script = base64encode(file("${path.module}/scripts/user-data-odoo-setup.sh")) # Example user data
  db_endpoint = module.rds_postgres.db_instance_endpoint
  db_port     = module.rds_postgres.db_instance_port
  db_name     = module.rds_postgres.db_instance_name
  db_user_secret_arn = var.odoo_db_user_secret_arn       # Staging specific secret
  db_password_secret_arn = var.odoo_db_password_secret_arn # Staging specific secret
  odoo_admin_password_secret_arn = var.odoo_admin_password_secret_arn # Staging specific secret

  environment_name   = local.environment_name
  project_name       = local.project_name
  default_tags       = local.default_tags
}

# Provision N8N Server (Staging should aim for production config parity)
module "n8n_app" {
  source = "../../modules/n8n_app"

  ami_id         = var.n8n_ami_id       # Should match Prod AMI
  instance_type  = var.n8n_instance_type # Should match Prod instance type
  key_name       = var.n8n_key_name
  n8n_sg_id      = module.security_groups.security_group_ids["n8n_sg"]
  subnet_id      = module.vpc.private_subnet_ids[0]
  # user_data_n8n_setup_script = base64encode(file("${path.module}/scripts/user-data-n8n-setup.sh")) # Example user data

  n8n_db_type     = var.n8n_db_type
  n8n_db_host     = var.n8n_db_type == "postgres" ? module.rds_postgres.db_instance_endpoint : null
  n8n_db_port     = var.n8n_db_type == "postgres" ? module.rds_postgres.db_instance_port : null
  n8n_db_name     = var.n8n_db_type == "postgres" ? var.db_name : null
  n8n_db_user_secret_arn = var.n8n_db_user_secret_arn       # Staging specific secret
  n8n_db_password_secret_arn = var.n8n_db_password_secret_arn # Staging specific secret
  n8n_encryption_key_secret_arn = var.n8n_encryption_key_secret_arn # Staging specific secret

  environment_name   = local.environment_name
  project_name       = local.project_name
  default_tags       = local.default_tags
}

# Provision AI Model Serving Servers (Staging should aim for production config parity)
module "ai_server" {
  source = "../../modules/ai_server"

  instance_count = var.ai_instance_count # Maybe fewer instances than Prod, but same type
  ami_id         = var.ai_ami_id       # Should match Prod AMI (GPU-ready)
  instance_type  = var.ai_instance_type # Should match Prod instance type (GPU type, 16GB+ VRAM)
  key_name       = var.ai_key_name
  ai_server_sg_id = module.security_groups.security_group_ids["ai_server_sg"]
  subnet_ids     = module.vpc.private_subnet_ids
  # user_data_ai_server_setup_script = base64encode(file("${path.module}/scripts/user-data-ai-server-setup.sh")) # Example user data
  ebs_volume_size_gb = var.ai_ebs_volume_size_gb # Should match Prod model volume size

  environment_name   = local.environment_name
  project_name       = local.project_name
  default_tags       = local.default_tags
}

# Output instance IPs for Ansible inventory generation
output "odoo_instance_ips" {
  description = "Private IPs of Odoo instances"
  value       = values(module.odoo_app.odoo_instance_ids_ips)
}

output "n8n_instance_ip" {
  description = "Private IP of N8N instance"
  value       = module.n8n_app.n8n_instance_ip
}

output "ai_server_ips" {
  description = "Private IPs of AI server instances"
  value       = values(module.ai_server.ai_server_instance_ids_ips)
}

# Output DB connection details for Ansible
output "db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = module.rds_postgres.db_instance_endpoint
}

output "db_port" {
  description = "RDS PostgreSQL port"
  value       = module.rds_postgres.db_instance_port
}

output "db_name" {
  description = "RDS PostgreSQL database name"
  value       = module.rds_postgres.db_instance_name
}

output "db_user_secret_arn" {
  description = "DB user secret ARN for Odoo"
  value       = var.odoo_db_user_secret_arn
}

output "db_password_secret_arn" {
  description = "DB password secret ARN for Odoo"
  value       = var.odoo_db_password_secret_arn
}

output "n8n_db_user_secret_arn" {
    description = "DB user secret ARN for N8N"
    value = var.n8n_db_user_secret_arn
}

output "n8n_db_password_secret_arn" {
    description = "DB password secret ARN for N8N"
    value = var.n8n_db_password_secret_arn
}

output "n8n_encryption_key_secret_arn" {
    description = "N8N encryption key secret ARN"
    value = var.n8n_encryption_key_secret_arn
}

output "odoo_admin_password_secret_arn" {
    description = "Odoo admin password secret ARN"
    value = var.odoo_admin_password_secret_arn
}
```