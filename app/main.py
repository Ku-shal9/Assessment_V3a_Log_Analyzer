from parser import parsed_line

from analyzer import (
    count_status_codes,
    count_endpoints,
    find_slow_requests,
    top_ips
)

# graceful handling
valid_lines = 0
malformed_lines = 0

# storing the valid logs
logs = []

with open("../tests/sample.log", "r") as file:
    for line in file:
        parsed = parsed_line(line)

        # on the basis of whether it can be parsed or not
        if parsed:
            valid_lines += 1
            logs.append(parsed)
        
        else:
            malformed_lines += 1

print("\nSummary")
print("Valid lines:", valid_lines)
print("Malformed lines:", malformed_lines)
print(count_status_codes(logs))
print(count_endpoints(logs).most_common(5))

print("\nSlow Request")
slow_requests = find_slow_requests(logs, threshold=500)

for request in slow_requests:
    print(request)

print(top_ips(logs))