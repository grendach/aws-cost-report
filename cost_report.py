#!/usr/bin/env python3
"""AWS Cost Explorer CLI and Lambda email reporter."""

import argparse
import os
from datetime import datetime, timedelta

import boto3

CE_REGION = os.getenv("AWS_COST_REGION", "eu-central-1")


def parse_args():
    p = argparse.ArgumentParser(description="AWS cost report")
    p.add_argument("--days", type=int, default=7, help="lookback days")
    p.add_argument("--group", choices=["service", "region", "account"], default="service")
    p.add_argument("--granularity", choices=["DAILY", "MONTHLY"], default="MONTHLY")
    p.add_argument("--profile", default=None, help="AWS profile name")
    p.add_argument("--top", type=int, default=10, help="show top N")
    p.add_argument("--send-email", action="store_true", help="publish the report to SNS")
    return p.parse_args()


def get_costs(days=7, group="service", granularity="MONTHLY", profile=None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    client = session.client("ce", region_name=CE_REGION)  # Cost Explorer supports eu-central-1 and us-east-1

    dim_map = {"service": "SERVICE", "region": "REGION", "account": "LINKED_ACCOUNT"}
    end = datetime.today().strftime("%Y-%m-%d")
    start = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    resp = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity=granularity,
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": dim_map[group]}],
    )

    costs = {}
    for period in resp["ResultsByTime"]:
        for cost_group in period["Groups"]:
            key = cost_group["Keys"][0]
            value = float(cost_group["Metrics"]["UnblendedCost"]["Amount"])
            costs[key] = costs.get(key, 0) + value
    return costs, start, end


def format_report(costs, start, end, top_n=10):
    top = sorted(costs.items(), key=lambda item: item[1], reverse=True)[:top_n]
    total = sum(costs.values())
    name_width = 52

    def fit_name(name):
        return name if len(name) <= name_width else name[: name_width - 3] + "..."

    lines = [
        f"AWS Cost Report: {start} → {end}",
        "",
        f"  {'Name':<{name_width}} {'USD':>10}",
        "  " + "-" * (name_width + 12),
    ]

    for name, amount in top:
        lines.append(f"  {fit_name(name):<{name_width}} ${amount:>8.2f}")

    lines.extend([
        "",
        f"  Total: ${total:.2f}",
    ])
    return "\n".join(lines)


def publish_report(report_text, subject):
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if not topic_arn:
        return False

    sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", CE_REGION))
    sns.publish(TopicArn=topic_arn, Subject=subject[:100], Message=report_text)
    return True


def lambda_handler(event, context):
    days = int(os.getenv("REPORT_DAYS", "7"))
    group = os.getenv("REPORT_GROUP", "service")
    granularity = os.getenv("REPORT_GRANULARITY", "MONTHLY")
    top_n = int(os.getenv("REPORT_TOP", "10"))

    costs, start, end = get_costs(days=days, group=group, granularity=granularity)
    report = format_report(costs, start, end, top_n=top_n)
    subject = f"AWS Cost Report: {start} → {end}"
    emailed = publish_report(report, subject)

    return {
        "statusCode": 200,
        "emailed": emailed,
        "subject": subject,
        "report": report,
    }


def main():
    args = parse_args()
    costs, start, end = get_costs(
        days=args.days,
        group=args.group,
        granularity=args.granularity,
        profile=args.profile,
    )
    report = format_report(costs, start, end, top_n=args.top)
    print(f"\n{report}")

    if args.send_email:
        subject = f"AWS Cost Report: {start} → {end}"
        if publish_report(report, subject):
            print("Report emailed through SNS.")
        else:
            print("SNS_TOPIC_ARN is not configured; skipped email delivery.")


if __name__ == "__main__":
    main()
