output "vpc_id" {
  description = "The ID of the VPC."
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "A list of public subnet IDs."
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "A list of private subnet IDs."
  value       = aws_subnet.private[*].id
}

output "default_security_group_id" {
  description = "The ID of the default security group of the VPC."
  value       = aws_vpc.this.default_security_group_id
}