from parser import parsed_line

# graceful handling
valid_lines = 0
malformed_lines = 0

with open("../tests/sample.log", "r") as file:
    for line in file:
        parsed = parsed_line(line)

        # on the basis of whether it can be parsed or not
        if parsed:
            valid_lines += 1
            print(parsed)
        
        else:
            malformed_lines += 1

print("\nSummary")
print("Valid lines:", valid_lines)
print("Malformed lines:", malformed_lines)