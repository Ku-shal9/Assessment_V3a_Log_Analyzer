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


def generate_standard_log():
    timestamp = (
        datetime.utcnow() -
        timedelta(seconds=random.randint(0, 100000))
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        f"{timestamp} {random_ip()} {random.choice(methods)} "
        f"{random.choice(paths)} {random.choice(status_codes)} "
        f"{random.randint(50, 2000)}ms"
    )


def generate_json_log():
    return json.dumps({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ip": random_ip(),
        "method": random.choice(methods),
        "path": random.choice(paths),
        "status": random.choice(status_codes),
        "response_time": f"{random.randint(50, 2000)}ms"
    })


def main():
    logs = []

    # normal logs
    for _ in range(50):
        logs.append(generate_standard_log())

    # json logs
    for _ in range(20):
        logs.append(generate_json_log())

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