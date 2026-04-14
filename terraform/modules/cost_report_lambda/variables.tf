variable "project_name" {
  description = "Lambda and resource name prefix"
  type        = string
}

variable "aws_region" {
  description = "Deployment region"
  type        = string
}

variable "lambda_source_file" {
  description = "Absolute path to the Python source file zipped for Lambda"
  type        = string
}

variable "report_email" {
  description = "Email destination for the report"
  type        = string
}

variable "report_days" {
  description = "Lookback days"
  type        = number
}

variable "report_group" {
  description = "Grouping mode"
  type        = string
}

variable "report_granularity" {
  description = "Cost Explorer granularity"
  type        = string
}

variable "report_top" {
  description = "Top rows count"
  type        = number
}

variable "schedule_expression" {
  description = "EventBridge schedule expression"
  type        = string
}

variable "tags" {
  description = "AWS tags"
  type        = map(string)
  default     = {}
}
