import re
import json
from datetime import datetime

# sample log: 2024-03-15T14:23:01Z 192.168.1.42 GET /api/users 200 142ms
# contains timestamp, ip, method, path, status, and response time

# for different timestamps
timestamps_format = [
    "%Y-%m-%dT%H:%M:%SZ", #ISO 8601 
    "%Y/%m/%d %H:%M:%S",
    "%d-%b-%Y %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f%z", #RFC 3339
    "%b %d %H:%M:%S", #traditional syslog
    "[%d/%b/%Y:%H:%M:%S %z]" #CLF
]

# regex pattern for common fields
log_pattern = re.compile(
    r"^(?P<timestamp>.+?)\s+"
    r"(?P<ip>\S+)\s+"
    r"(?P<method>GET|POST|PUT|DELETE|PATCH)?\s*"
    r"(?P<path>/\S+)?\s*"
    r"(?P<status>\d{3}|-)\s*"
    r"(?P<response>[\d\.]+(?:ms|s)?)"
)

# parsing the timestamp
def parse_timestamp(timestamp):

    timestamp = timestamp.strip()

    # standard formats mentioned in list above
    for fmt in timestamps_format:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            pass

    # unix timestamp
    if timestamp.isdigit():
        try:
            return datetime.fromtimestamp(int(timestamp))
        except Exception:
            pass

    return None

# handling the ms conversion and parsing
def parse_response_time(response):

    response = response.strip()

    try:

        if response.endswith("ms"):
        # provided that it is already in ms
            return float(response[:-2])

        elif response.endswith("s"):
        # provided that it is in seconds
            return float(response[:-1]) * 1000
        
        else:
        # no unit than assume already in ms
            return float(response)

    except ValueError:
        return None
    
# handling JSON line
def parse_json_log(line):

    data = json.loads(line)

    return {
        "timestamp": parse_timestamp(str(data.get("timestamp", ""))),
        "ip": data.get("ip"),
        "method": data.get("method"),
        "path": data.get("path"),
        "status": (
            int(data["status"])
            if data.get("status") not in [None, "-"]
            else None
        ),
        "response_time": parse_response_time(
            str(data.get("response_time", "0"))
        ),
        "source": "json"
    }

# standard log format using regex
def parse_standard_log(line):

    match = log_pattern.search(line)

    if not match:
        return None

    groups = match.groupdict()

    # validate status
    status = groups.get("status")

    try:
        status = int(status) if status and status != "-" else None
    except ValueError:
        return None

    # validate response time
    response_time = parse_response_time(
        groups.get("response", "0")
    )

    if response_time is None:
        return None

    # validate timestamp
    timestamp = parse_timestamp(groups.get("timestamp", ""))

    return {
        "timestamp": timestamp,
        "ip": groups.get("ip"),
        "method": groups.get("method"),
        "path": groups.get("path"),
        "status": status,
        "response_time": response_time,
        "source": "standard"
    }

def parsed_line(line):

    # remove whitespace
    line = line.strip()

    # empty line protection
    if not line:
        return None

    try:

        # JSON log
        if line.startswith("{"):
            return parse_json_log(line)

        # standard regex log
        return parse_standard_log(line)

    except Exception:
        return None
