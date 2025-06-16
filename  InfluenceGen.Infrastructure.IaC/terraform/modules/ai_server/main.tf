```hcl
resource "aws_instance" "ai_server" {
  count               = var.instance_count
  ami                 = var.ami_id
  instance_type       = var.instance_type # Ensure this is a GPU instance type (e.g., g4dn.xlarge)
  key_name            = var.key_name
  vpc_security_group_ids = [var.ai_server_sg_id]
  subnet_id           = var.subnet_ids[count.index % length(var.subnet_ids)]
  user_data_base64    = var.user_data_ai_server_setup_script
  # associate_public_ip_address = true # Set to true if in public subnet

  root_block_device {
    volume_size = 100 # Example size for OS, adjust as needed
    volume_type = "gp2"
  }

  # Additional volume for models
  ebs_block_device {
    device_name = "/dev/sdh" # Or appropriate device name based on AMI
    volume_size = var.ebs_volume_size_gb
    volume_type = "gp3" # Faster/cheaper
    delete_on_termination = true
  }

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-ai-server-${count.index + 1}"
    Environment = var.environment_name
    Role        = "AIServing"
  })
}

# Note: Additional resources like Load Balancer, Target Group, Auto Scaling Group
# would be added here for HA/scaling if needed.
```