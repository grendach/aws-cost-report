#!/usr/bin/env python3
"""AWS Cost Explorer CLI — python cost_report.py --days 30 --group service"""
import argparse, boto3
from datetime import datetime, timedelta

def parse_args():
    p = argparse.ArgumentParser(description="AWS cost report")
    p.add_argument("--days",    type=int,  default=30,        help="lookback days")
    p.add_argument("--group",   choices=["service","region","account"],
                                           default="service")
    p.add_argument("--granularity", choices=["DAILY","MONTHLY"], default="MONTHLY")
    p.add_argument("--profile", default=None,          help="AWS profile name")
    p.add_argument("--top",     type=int,  default=10,       help="show top N")
    return p.parse_args()

def get_costs(args):
    session = boto3.Session(profile_name=args.profile)
    client  = session.client('ce', region_name='eu-west-1')

    dim_map = {"service": "SERVICE", "region": "REGION", "account": "LINKED_ACCOUNT"}
    end   = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=args.days)).strftime('%Y-%m-%d')

    resp = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity=args.granularity,
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': dim_map[args.group]}]
    )

    costs = {}
    for period in resp['ResultsByTime']:
        for g in period['Groups']:
            k = g['Keys'][0]
            v = float(g['Metrics']['UnblendedCost']['Amount'])
            costs[k] = costs.get(k, 0) + v
    return costs, start, end

def main():
    args  = parse_args()
    costs, start, end = get_costs(args)
    top   = sorted(costs.items(), key=lambda x: x[1], reverse=True)[:args.top]
    total = sum(costs.values())

    print(f"\n AWS Cost Report: {start} → {end}\n")
    print(f"  {'Name':<45} {'USD':>10}")
    print("  " + "-"*57)
    for name, amt in top:
        bar = "█" * int(amt / total * 30)
        print(f"  {name:<45} ${amt:>8.2f}  {bar}")
    print(f"\n  Total: ${total:.2f}\n")

if __name__ == "__main__":
    main()
