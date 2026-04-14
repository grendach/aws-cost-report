output "lambda_function_name" {
  description = "Created Lambda function name"
  value       = module.cost_report_lambda.lambda_function_name
}

output "lambda_function_arn" {
  description = "Created Lambda function ARN"
  value       = module.cost_report_lambda.lambda_function_arn
}

output "sns_topic_arn" {
  description = "SNS topic that sends the email report"
  value       = module.cost_report_lambda.sns_topic_arn
}

output "schedule_expression" {
  description = "Daily execution schedule"
  value       = module.cost_report_lambda.schedule_expression
}
