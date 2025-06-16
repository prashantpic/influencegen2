terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" // Specify appropriate version
    }
  }
  required_version = ">= 1.8.0" // Specify Terraform version
}

provider "aws" {
  region = var.aws_region
  // Assume credentials configured via environment variables or IAM roles
}