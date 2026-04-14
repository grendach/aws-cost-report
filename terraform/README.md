# Terraform deployment for AWS cost report Lambda

This Terraform project deploys the Python AWS cost report as a Lambda function in the **eu-central-1** region.

## What it creates
- Lambda function running the report code from the parent folder
- SNS topic with email subscription to `grendach@gmail.com`
- EventBridge schedule that runs every **Sunday at 21:00 UTC**
- A weekly report covering the **last 7 days**
- IAM permissions for CloudWatch Logs, Cost Explorer, and SNS publish

## Deploy
```bash
cd terraform
terraform init
terraform apply
```

After apply, AWS will send a subscription confirmation email. The report starts arriving after that confirmation is accepted.

## Manual test
```bash
aws lambda invoke \
  --region eu-central-1 \
  --function-name aws-cost-report \
  /tmp/cost-report.json && cat /tmp/cost-report.json
```
