# sample log: 2024-03-15T14:23:01Z 192.168.1.42 GET /api/users 200 142ms
# contains timestamp, ip, method, path, status, and response time

def parsed_line(line): 
    # removing whitspaces first
    line = line.strip()

    # handling missing line
    if not line:
        return None
    
    try:
        #tokenization
        args = line.split()

        # Extract fields
        parsed_data = {
            "timestamp": args[0],
            "ip": args[1],
            "method": args[2],
            "path": args[3],
            "status": int(args[4]) if args[4] != "-" else None,
            "response_time": args[5]
        }

        return parsed_data

    except Exception:
        # If anything fails, return None instead of crashing
        return None
