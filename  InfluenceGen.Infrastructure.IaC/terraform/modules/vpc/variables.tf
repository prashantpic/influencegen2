variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC."
  type        = string
}

variable "public_subnet_cidrs" {
  description = "A list of CIDR blocks for the public subnets."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "A list of CIDR blocks for the private subnets."
  type        = list(string)
}

variable "availability_zones" {
  description = "A list of availability zones to deploy resources into."
  type        = list(string)
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
  description = "Additional tags to apply to VPC resources."
  type        = map(string)
  default     = {}
}