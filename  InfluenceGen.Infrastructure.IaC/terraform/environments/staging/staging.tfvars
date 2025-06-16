```hcl
# Example staging environment variables

# VPC (Should mirror Prod structure)
vpc_cidr_block = "10.10.0.0/16"
public_subnet_cidrs = ["10.10.1.0/24", "10.10.2.0/24", "10.10.3.0/24"] # Example, match Prod AZ count
private_subnet_cidrs = ["10.10.11.0/24", "10.10.12.0/24", "10.10.13.0/24"] # Example, match Prod AZ count
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"] # Example AZs, match Prod

# RDS PostgreSQL (Aim for Prod config parity)
db_instance_class    = "db.m6g.large" # Should match Prod class
db_allocated_storage = 100          # Should match Prod allocation
db_engine_version    = "15.4"       # Should match Prod version
db_name              = "influencegenstaging"
db_username_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/rds/master_username-XXXXXX" # REPLACE
db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/rds/master_password-YYYYYY" # REPLACE

# Odoo App (Aim for Prod config parity, potentially scaled down)
odoo_ami_id       = "ami-0abcdef1234567890" # REPLACE with Prod/OS AMI ID
odoo_instance_type = "c6g.xlarge"        # Should match Prod instance type
odoo_instance_count = 2                 # Maybe 2 instances for staging vs 4+ for Prod
odoo_key_name      = "influencegen-staging-key" # REPLACE
odoo_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/odoo/db_user-ZZZZZZ" # REPLACE
odoo_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/odoo/db_password-AAAAAA" # REPLACE
odoo_admin_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/odoo/admin_password-BBBBBB" # REPLACE

# N8N App (Aim for Prod config parity)
n8n_ami_id       = "ami-0abcdef1234567890" # REPLACE with Prod/OS AMI ID
n8n_instance_type = "c6g.large"          # Should match Prod instance type
n8n_key_name      = "influencegen-staging-key" # REPLACE
n8n_db_type       = "postgres"           # Should match Prod
# n8n_db_host and n8n_db_port will be automatically set from RDS output
n8n_db_name       = "influencegenstaging" # Same DB as Odoo
n8n_db_user_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/n8n/db_user-CCCCCC" # REPLACE
n8n_db_password_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/n8n/db_password-DDDDDD" # REPLACE
n8n_encryption_key_secret_arn = "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:influencegen/staging/n8n/encryption_key-EEEEEE" # REPLACE

# AI Server (Aim for Prod config parity, potentially scaled down instance count)
ai_ami_id       = "ami-0abcdef1234567890" # REPLACE with Prod/GPU AMI ID
ai_instance_type = "g4dn.xlarge"        # MUST match Prod GPU instance type (16GB+ VRAM, preferably 24GB+ like g5.xlarge)
ai_instance_count = 1                   # Maybe 1 instance for staging vs 2+ for Prod
ai_key_name      = "influencegen-staging-key" # REPLACE
ai_ebs_volume_size_gb = 500             # Should match Prod model volume size
```