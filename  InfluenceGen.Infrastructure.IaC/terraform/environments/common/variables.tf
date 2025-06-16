variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project for tagging resources."
  type        = string
  default     = "influencegen"
}

variable "default_tags" {
  description = "Default tags to apply to all resources."
  type        = map(string)
  default = {
    Project   = "InfluenceGen"
    ManagedBy = "Terraform"
  }
}