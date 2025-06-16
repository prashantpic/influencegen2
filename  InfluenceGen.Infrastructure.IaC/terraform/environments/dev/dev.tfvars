```hcl
# Example dev environment variables

# VPC
vpc_cidr_block = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
availability_zones = ["us-east-1a", "us-east-1b"] # Example AZs

# RDS PostgreSQL
db_instance_class    = "db.t3.micro" # Dev-friendly size
db_allocated_storage = 20           # Dev-friendly size
db_engine_version    = "15.4"        # Specify desired PG version
db_name              = "influencegendev"
db_username_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/rds/master_username-XXXXXX" # REPLACE
db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/rds/master_password-YYYYYY" # REPLACE

# Odoo App
odoo_ami_id       = "ami-0abcdef1234567890" # REPLACE with Dev/OS AMI ID
odoo_instance_type = "t3.medium"         # Dev-friendly size
odoo_instance_count = 1                  # Single instance for Dev
odoo_key_name      = "influencegen-dev-key" # REPLACE with your key pair name
odoo_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/odoo/db_user-ZZZZZZ" # REPLACE
odoo_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/odoo/db_password-AAAAAA" # REPLACE
odoo_admin_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/odoo/admin_password-BBBBBB" # REPLACE

# N8N App
n8n_ami_id       = "ami-0abcdef1234567890" # REPLACE with Dev/OS AMI ID
n8n_instance_type = "t3.small"           # Dev-friendly size
n8n_key_name      = "influencegen-dev-key" # REPLACE
n8n_db_type       = "postgres"           # Use RDS
# n8n_db_host and n8n_db_port will be automatically set from RDS output
n8n_db_name       = "influencegendev" # Same DB as Odoo
n8n_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/n8n/db_user-CCCCCC" # REPLACE
n8n_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/n8n/db_password-DDDDDD" # REPLACE
n8n_encryption_key_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/dev/n8n/encryption_key-EEEEEE" # REPLACE

# AI Server
ai_ami_id       = "ami-0abcdef1234567890" # REPLACE with Dev/GPU AMI ID (e.g., Deep Learning AMI)
ai_instance_type = "g4dn.xlarge"        # GPU instance type with 16GB VRAM (lowest req)
ai_instance_count = 1                   # Single instance for Dev
ai_key_name      = "influencegen-dev-key" # REPLACE
ai_ebs_volume_size_gb = 50              # Smaller volume for Dev models
```