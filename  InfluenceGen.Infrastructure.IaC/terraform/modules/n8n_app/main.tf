```hcl
resource "aws_instance" "n8n" {
  ami                 = var.ami_id
  instance_type       = var.instance_type
  key_name            = var.key_name
  vpc_security_group_ids = [var.n8n_sg_id]
  subnet_id           = var.subnet_id
  user_data_base64    = var.user_data_n8n_setup_script
  # associate_public_ip_address = true # Set to true if in public subnet

  root_block_device {
    volume_size = 50 # Example size, adjust as needed
    volume_type = "gp2"
  }

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-n8n"
    Environment = var.environment_name
    Role        = "N8N"
  })
}

# Note: Additional resources like Load Balancer, Target Group would be added
# here if N8N is exposed publicly via an LB.
```