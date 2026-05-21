# sample log: 2024-03-15T14:23:01Z 192.168.1.42 GET /api/users 200 142ms
# contains timestamp, ip, method, path, status, and response time

def parsed_line(line): #tokenization
    args = line.split()

    parsed_data = {
        "timestamp": args[0],
        "ip": args[1],
        "method": args[2],
        "path": args[3],
        "status": int(args[4]),
        "response_time": args[5]
    }
    return parsed_data