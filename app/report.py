import pandas as pd
from analyzer import (
    count_status_codes,
    count_endpoints,
    find_slow_requests,
    top_ips
)


def generate_csv_report(logs, filename="log_report.csv"):

    status_counts = count_status_codes(logs)
    endpoint_counts = count_endpoints(logs)
    slow_requests = find_slow_requests(logs)
    top_ip_list = top_ips(logs)

    report_data = []

    # status codes
    for status, count in status_counts.items():
        report_data.append({
            "category": "status_code",
            "metric": status,
            "value": count
        })

    # endpoints
    for endpoint, count in endpoint_counts.items():
        report_data.append({
            "category": "endpoint",
            "metric": endpoint,
            "value": count
        })

    # slow requests summary
    report_data.append({
        "category": "slow_requests",
        "metric": "count",
        "value": len(slow_requests)
    })

    # top IPs
    for ip, count in top_ip_list:
        report_data.append({
            "category": "top_ip",
            "metric": ip,
            "value": count
        })

    df = pd.DataFrame(report_data)

    df.to_csv(filename, index=False)

    return filename