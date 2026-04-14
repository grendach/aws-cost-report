variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name prefix for created resources"
  type        = string
  default     = "aws-cost-report"
}

variable "report_email" {
  description = "Email address that receives the SNS report"
  type        = string
  default     = "grendach@gmail.com"
}

variable "report_days" {
  description = "Lookback period in days for the report"
  type        = number
  default     = 7
}

variable "report_group" {
  description = "Grouping dimension for the AWS cost report"
  type        = string
  default     = "service"

  validation {
    condition     = contains(["service", "region", "account"], var.report_group)
    error_message = "report_group must be one of: service, region, account."
  }
}

variable "report_granularity" {
  description = "Cost Explorer granularity"
  type        = string
  default     = "MONTHLY"

  validation {
    condition     = contains(["DAILY", "MONTHLY"], var.report_granularity)
    error_message = "report_granularity must be DAILY or MONTHLY."
  }
}

variable "report_top" {
  description = "Number of top rows shown in the report"
  type        = number
  default     = 10
}

variable "schedule_expression" {
  description = "EventBridge cron expression for running the Lambda"
  type        = string
  default     = "cron(0 21 ? * SUN *)"
}

variable "tags" {
  description = "Common AWS tags"
  type        = map(string)
  default = {
    Project   = "aws-cost-report"
    ManagedBy = "Terraform"
  }
}
