from collections import Counter, defaultdict

# status code analysis
def count_status_codes(logs):
    stats = [log["status"] for log in logs]
    return Counter(stats)

# endpoint frequency analysis
def count_endpoints(logs):
    endpoints = [log["path"] for log in logs]
    return Counter(endpoints)

# slow request analysis
def find_slow_requests(logs, threshold=500):

    slow = []

    for log in logs:

        response_time = log.get("response_time")

        if response_time is None:
            continue

        if response_time > threshold:
            slow.append(log)

    return slow

def top_ips(logs, limit=5):
    ips = [log["ip"] for log in logs]

    return Counter(ips).most_common(limit)