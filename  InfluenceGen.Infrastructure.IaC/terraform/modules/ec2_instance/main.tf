resource "aws_instance" "this" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  vpc_security_group_ids      = var.vpc_security_group_ids
  subnet_id                   = var.subnet_id
  user_data_base64            = var.user_data_script # user_data expects base64
  iam_instance_profile        = var.iam_instance_profile_name # Use name directly
  associate_public_ip_address = true # Assume public subnet if public IP is needed

  root_block_device {
    volume_size = var.root_block_device_size
    volume_type = "gp2" # General Purpose SSD
  }

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.instance_name_prefix}-${var.environment_name}"
    Environment = var.environment_name
  })
}