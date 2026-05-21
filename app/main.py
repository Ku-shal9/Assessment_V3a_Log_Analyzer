from parser import parsed_line

with open("../tests/sample.log", "r") as file:
    for line in file:
        parsed = parsed_line(line)

        print(parsed)