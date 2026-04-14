module "cost_report_lambda" {
  source = "./modules/cost_report_lambda"

  project_name        = var.project_name
  aws_region          = var.aws_region
  lambda_source_file  = "${path.module}/../cost_report.py"
  report_email        = var.report_email
  report_days         = var.report_days
  report_group        = var.report_group
  report_granularity  = var.report_granularity
  report_top          = var.report_top
  schedule_expression = var.schedule_expression
  tags                = var.tags
}
