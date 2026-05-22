import random
import json
from datetime import datetime, timedelta
import os


# ensure correct output path (tests folder)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "tests", "sample.log")


methods = ["GET", "POST", "PUT", "DELETE"]
paths = [
    "/api/users",
    "/api/login",
    "/api/products",
    "/api/orders",
    "/api/search"
]

status_codes = [200, 201, 400, 401, 404, 500]

bad_logs = [
    "BROKEN LOG ENTRY",
    "INVALID_TIMESTAMP 192.168.1.1 GET /api/test 200 100ms",
    "2024-03-15T14:23:01Z BAD_IP GET /api/users 200 100ms",
    "2024-03-15T14:23:01Z 192.168.1.1 GET",
    "MISSING_FIELDS",
    ""
]


def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def _random_dt():
    return datetime.utcnow() - timedelta(seconds=random.randint(0, 100000))


def _format_timestamp(dt):
    """Mix single- and multi-token timestamp shapes for parser testing."""
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",       # 2024-03-15T14:23:01Z
        "%Y/%m/%d %H:%M:%S",        # 2024/03/15 14:23:01
        "%d-%b-%Y %H:%M:%S",        # 15-Mar-2024 14:23:01
        "%b %d %H:%M:%S",           # Mar 15 14:23:01
        "[%d/%b/%Y:%H:%M:%S %z]",   # [15/Mar/2024:14:23:01 +0000]
    ]
    fmt = random.choice(formats)
    if fmt.endswith("%z"):
        return dt.strftime(fmt)
    return dt.strftime(fmt)


def generate_standard_log(multi_token_only=False):
    dt = _random_dt()
    if multi_token_only:
        fmt = random.choice([
            "%Y/%m/%d %H:%M:%S",
            "%d-%b-%Y %H:%M:%S",
            "%b %d %H:%M:%S",
        ])
        timestamp = dt.strftime(fmt)
    else:
        timestamp = _format_timestamp(dt)

    return (
        f"{timestamp} {random_ip()} {random.choice(methods)} "
        f"{random.choice(paths)} {random.choice(status_codes)} "
        f"{random.randint(50, 2000)}ms"
    )


def generate_json_log(multi_token_timestamp=False):
    dt = _random_dt()
    if multi_token_timestamp:
        ts = dt.strftime(random.choice([
            "%Y/%m/%d %H:%M:%S",
            "%d-%b-%Y %H:%M:%S",
        ]))
    else:
        ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    return json.dumps({
        "timestamp": ts,
        "ip": random_ip(),
        "method": random.choice(methods),
        "path": random.choice(paths),
        "status": random.choice(status_codes),
        "response_time": f"{random.randint(50, 2000)}ms"
    })


def main():
    logs = []

    # normal logs (mixed timestamp formats)
    for _ in range(40):
        logs.append(generate_standard_log())

    # multi-token timestamp logs
    for _ in range(15):
        logs.append(generate_standard_log(multi_token_only=True))

    # json logs
    for _ in range(15):
        logs.append(generate_json_log())

    # json logs with multi-token timestamps
    for _ in range(5):
        logs.append(generate_json_log(multi_token_timestamp=True))

    # malformed logs
    logs.extend(bad_logs)

    random.shuffle(logs)

    # IMPORTANT: ensure tests folder exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        for log in logs:
            f.write(log + "\n")

    print(f"Generated {len(logs)} logs at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()