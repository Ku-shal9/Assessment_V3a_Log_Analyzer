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

# fields after the timestamp (timestamp may span multiple tokens)
rest_pattern = re.compile(
    r"^(?P<ip>\S+)\s+"
    r"(?P<method>GET|POST|PUT|DELETE|PATCH)?\s*"
    r"(?P<path>/\S+)?\s*"
    r"(?P<status>\d{3}|-)\s*"
    r"(?P<response>[\d\.]+(?:ms|s)?)"
)

# max tokens to join when probing multi-token timestamps (e.g. "15-Mar-2024 14:23:01")
MAX_TIMESTAMP_TOKENS = 6

def extract_timestamp_prefix(line):
    tokens = line.split()
    if not tokens:
        return None, None

    for i in range(1, min(len(tokens), MAX_TIMESTAMP_TOKENS) + 1):
        candidate = " ".join(tokens[:i])
        timestamp = parse_timestamp(candidate)
        if timestamp is not None:
            rest = " ".join(tokens[i:])
            return timestamp, rest

    return None, None

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

    status = data.get("status")
    if status not in (None, "-"):
        try:
            status = int(status)
        except (TypeError, ValueError):
            status = None
    else:
        status = None

    raw_response = data.get("response_time")
    response_time = (
        parse_response_time(str(raw_response))
        if raw_response is not None
        else None
    )

    return {
        "timestamp": parse_timestamp(str(data.get("timestamp", ""))),
        "ip": data.get("ip"),
        "method": data.get("method"),
        "path": data.get("path"),
        "status": status,
        "response_time": response_time,
        "source": "json"
    }

# standard log format using regex
def parse_standard_log(line):

    timestamp, rest = extract_timestamp_prefix(line)

    if timestamp is None or not rest:
        return None

    # match from start; extra tokens after response time (e.g. user-agent) are ignored
    match = rest_pattern.match(rest)

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
