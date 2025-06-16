```hcl
# Example production environment variables

# VPC
vpc_cidr_block = "10.20.0.0/16"
public_subnet_cidrs = ["10.20.1.0/24", "10.20.2.0/24", "10.20.3.0/24"] # Minimum 3 AZs for Prod HA
private_subnet_cidrs = ["10.20.11.0/24", "10.20.12.0/24", "10.20.13.0/24"] # Minimum 3 AZs for Prod HA
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"] # Example AZs

# RDS PostgreSQL (Production-grade)
db_instance_class    = "db.m6g.large" # Production-grade size
db_allocated_storage = 100          # Production-grade allocation
db_engine_version    = "15.4"       # Specify desired PG version
db_name              = "influencegenprod"
db_username_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/rds/master_username-XXXXXX" # REPLACE
db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/rds/master_password-YYYYYY" # REPLACE

# Odoo App (Production-grade, scaled)
odoo_ami_id       = "ami-0abcdef1234567890" # REPLACE with Production OS AMI ID
odoo_instance_type = "c6g.xlarge"        # Production-grade size
odoo_instance_count = 4                  # Example: 4 instances for HA/scale (adjust based on load)
odoo_key_name      = "influencegen-prod-key" # REPLACE with your key pair name
odoo_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/odoo/db_user-ZZZZZZ" # REPLACE
odoo_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/odoo/db_password-AAAAAA" # REPLACE
odoo_admin_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/odoo/admin_password-BBBBBB" # REPLACE

# N8N App (Production-grade)
n8n_ami_id       = "ami-0abcdef1234567890" # REPLACE with Production OS AMI ID
n8n_instance_type = "c6g.large"           # Production-grade size
n8n_key_name      = "influencegen-prod-key" # REPLACE
n8n_db_type       = "postgres"            # Use RDS
# n8n_db_host and n8n_db_port will be automatically set from RDS output
n8n_db_name       = "influencegenprod" # Same DB as Odoo
n8n_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/n8n/db_user-CCCCCC" # REPLACE
n8n_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/n8n/db_password-DDDDDD" # REPLACE
n8n_encryption_key_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/prod/n8n/encryption_key-EEEEEE" # REPLACE

# AI Server (Production-grade, GPU, scaled)
ai_ami_id       = "ami-0abcdef1234567890" # REPLACE with Production GPU AMI ID
ai_instance_type = "g5.2xlarge"         # Production-grade GPU instance type (24GB+ VRAM)
ai_instance_count = 2                   # Example: 2 instances for processing load/HA (adjust based on load)
ai_key_name      = "influencegen-prod-key" # REPLACE
ai_ebs_volume_size_gb = 500             # Volume size for production models
```