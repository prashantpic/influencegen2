data "aws_secretsmanager_secret_version" "username" {
  secret_id = var.username_secret_arn
}

data "aws_secretsmanager_secret_version" "password" {
  secret_id = var.password_secret_arn
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-${var.environment_name}-dbsubnetgroup"
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-dbsubnetgroup"
    Environment = var.environment_name
  })
}

resource "aws_db_instance" "this" {
  allocated_storage    = var.allocated_storage
  storage_type         = "gp2" # General Purpose SSD
  engine               = "postgres"
  engine_version       = var.engine_version
  instance_class       = var.instance_class
  name                 = var.db_name
  username             = data.aws_secretsmanager_secret_version.username.secret_string
  password             = data.aws_secretsmanager_secret_version.password.secret_string
  db_subnet_group_name = aws_db_subnet_group.this.name
  vpc_security_group_ids = var.vpc_security_group_ids
  skip_final_snapshot  = var.environment_name == "dev" ? true : false # Don't skip for staging/prod
  final_snapshot_identifier = "${var.project_name}-${var.environment_name}-final-snapshot"
  multi_az             = var.multi_az
  backup_retention_period = var.backup_retention_period
  publicly_accessible  = false

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-rds-pg"
    Environment = var.environment_name
  })
}