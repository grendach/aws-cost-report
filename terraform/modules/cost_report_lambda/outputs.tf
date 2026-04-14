output "lambda_function_name" {
  value = aws_lambda_function.cost_report.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.cost_report.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.report_topic.arn
}

output "schedule_expression" {
  value = aws_cloudwatch_event_rule.daily_schedule.schedule_expression
}
