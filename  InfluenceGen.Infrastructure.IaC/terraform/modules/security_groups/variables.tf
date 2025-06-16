variable "vpc_id" {
  description = "The ID of the VPC to create security groups in."
  type        = string
}

variable "security_group_definitions" {
  description = "A map of security group definitions."
  type = map(object({
    description = string
    ingress = list(object({
      protocol                 = string
      from_port                = number
      to_port                  = number
      cidr_blocks              = list(string)
      source_security_group_id = string # Use string type, can be null
      description              = string
    }))
    egress = list(object({
      protocol    = string
      from_port   = number
      to_port     = number
      cidr_blocks = list(string)
      description = string
    }))
  }))
  default = {}
}

variable "environment_name" {
  description = "The name of the environment (e.g., dev, staging, production)."
  type        = string
}

variable "project_name" {
  description = "The name of the project for tagging resources."
  type        = string
}

variable "default_tags" {
  description = "Default tags to apply to all resources."
  type        = map(string)
}

variable "tags" {
  description = "Additional tags to apply to security group resources."
  type        = map(string)
  default     = {}
}