from parser import parsed_line

from analyzer import (
    count_status_codes,
    count_endpoints,
    find_slow_requests,
    top_ips
)
from report import generate_csv_report

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

report_file = generate_csv_report(logs)

print("\nCSV report generated:")
print(report_file)