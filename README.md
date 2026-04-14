# aws-cost-report
AWS cost report
```bash
python cost_report.py --days 7 --group service --top 5
python cost_report.py --days 30 --group region --profile staging
```
## Deployment 
For deployemnt steps check `terraform/README.md`. The Lambda function runs every Sunday at 21:00 UTC and sends a report for the last 7 days.
