aws_region          = "eu-central-1"
project_name        = "aws-cost-report"
report_email        = "grendach@gmail.com"
report_days         = 7
report_group        = "service"
report_granularity  = "MONTHLY"
report_top          = 10
schedule_expression = "cron(0 21 ? * SUN *)"
